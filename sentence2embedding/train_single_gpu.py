import logging
import os
import sys
from typing import Dict, List, Tuple, Optional, Any, Union

import torch
from torch import nn
from torch.nn import functional as F

from transformers import AutoConfig, AutoModel, AutoTokenizer
from transformers import (
    HfArgumentParser,
    set_seed,
)

import os
from dataclasses import dataclass, field
from typing import Optional, List
from transformers import TrainingArguments
from transformers import DataCollatorWithPadding
from transformers.trainer import Trainer

import logging
logger = logging.getLogger(__name__)


# Name of the files used for checkpointing
TRAINING_ARGS_NAME = "training_args.bin"
TRAINER_STATE_NAME = "trainer_state.json"
OPTIMIZER_NAME = "optimizer.pt"
SCHEDULER_NAME = "scheduler.pt"
SCALER_NAME = "scaler.pt"


@dataclass
class ModelArguments:
    model_name_or_path: str = field(
        metadata={"help": "Path to pretrained model or model identifier from huggingface.co/models"}
    )
    config_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained config name or path if not the same as model_name"}
    )
    tokenizer_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained tokenizer name or path if not the same as model_name"}
    )
    cache_dir: Optional[str] = field(
        default=None, metadata={"help": "Where do you want to store the pretrained models downloaded from s3"}
    )

    normalize: bool = field(default=False)
    pooling: str = field(default='mean')


@dataclass
class QPCollator(DataCollatorWithPadding):
    """
    Wrapper that does conversion from List[Tuple[encode_qry, encode_psg]] to List[qry], List[psg]
    and pass batch separately to the actual collator.
    Abstract out data detail for the model.
    """
    max_q_len: int = 32
    max_p_len: int = 128

    def __call__(self, features):

        keys = list(features[0].keys())
        collated_batch = {}

        for key in keys:
            if not isinstance(features[0][key], str):
                continue
            text = [f[key] for f in features]
            # print(text)
            text_batch = self.tokenizer(
                text,
                padding='max_length',
                truncation=True,
                max_length=self.max_p_len,
                return_tensors="pt",
            )
            collated_batch[key] = text_batch

        return collated_batch


class AutoModelForSentenceEmbedding(nn.Module):
    def __init__(
        self,
        model_name_or_path,
        tokenizer=None,
        pooling='cls',
        normalize=True,
    ):
        super(AutoModelForSentenceEmbedding, self).__init__()

        self.model = AutoModel.from_pretrained(model_name_or_path)
        # 冻结BERT参数
        for param in self.model.parameters():
            param.requires_grad = False
        self.tokenizer = tokenizer if tokenizer else AutoTokenizer.from_pretrained(model_name_or_path)
        self.pooling = pooling
        self.normalize = normalize
        self.down_dim = True
        if self.down_dim:
            self.down_layer = nn.Linear(768, 128)


    def forward(self, **kwargs):
        model_output = self.model(**kwargs)
        if self.down_dim:
            embeddings = self.down_layer(self.mean_pooling(model_output, kwargs['attention_mask']))
        else:
            embeddings = self.mean_pooling(model_output, kwargs['attention_mask'])
        if self.normalize:
            embeddings = F.normalize(embeddings, p=2, dim=1)

        return embeddings

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def save_pretrained(self, output_path):
        self.model.save_pretrained(output_path)



class EmbeddingTrainer(Trainer):

    def _save(self, output_dir: Optional[str] = None, state_dict=None):
        # If we are executing this function, we are the process zero, so we don't check for that.
        output_dir = output_dir if output_dir is not None else self.args.output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Saving model checkpoint to {output_dir}")
        self.model.save_pretrained(output_dir)

        if self.tokenizer is not None:
            self.tokenizer.save_pretrained(output_dir)

        # Good practice: save your training arguments together with the trained model
        torch.save(self.args, os.path.join(output_dir, TRAINING_ARGS_NAME))
    
    def compute_loss(self, model, inputs, return_outputs=False):

        all_embeddings = {}
        for k in ['question', 'answer']:
            all_embeddings[k] = model(
                input_ids=inputs[k]['input_ids'],
                attention_mask=inputs[k]['attention_mask'],
                token_type_ids=inputs[k]['token_type_ids'],
            )
        embeddings_query = all_embeddings['question']
        embeddings_pos = all_embeddings['answer']
        
        scores = embeddings_query @ embeddings_pos.T
        labels = torch.arange(0, embeddings_query.shape[0], dtype=torch.long, device=embeddings_query.device)
        # 对比学习的方式，所以scores的对角线元素是真值
        self.cross_entropy = torch.nn.CrossEntropyLoss(reduction='mean')
        loss = self.cross_entropy(scores, labels)
        return loss


def main():
    parser = HfArgumentParser((ModelArguments, TrainingArguments))

    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        model_args, training_args = parser.parse_json_file(json_file=os.path.abspath(sys.argv[1]))
    else:
        model_args, training_args = parser.parse_args_into_dataclasses()
        model_args: ModelArguments
        training_args: TrainingArguments

    if (
            os.path.exists(training_args.output_dir)
            and os.listdir(training_args.output_dir)
            and training_args.do_train
            and not training_args.overwrite_output_dir
    ):
        raise ValueError(
            f"Output directory ({training_args.output_dir}) already exists and is not empty. Use --overwrite_output_dir to overcome."
        )

    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO if training_args.local_rank in [-1, 0] else logging.WARN,
    )

    set_seed(training_args.seed)

    tokenizer = AutoTokenizer.from_pretrained(
        model_args.model_name_or_path,
        cache_dir=model_args.cache_dir
    )
    model = AutoModelForSentenceEmbedding(
        model_args.model_name_or_path,
        pooling=model_args.pooling,
        normalize=model_args.normalize,
    )
    from datasets import load_dataset
    wq = load_dataset('F:\Cmodels\datasets\wiki_qa', split='train')
    train_dataset = wq.remove_columns('label')

    data_collator = QPCollator(tokenizer=tokenizer)

    torch.autograd.set_detect_anomaly(True)
    trainer = EmbeddingTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )

    trainer.train()


if __name__ == "__main__":
    main()
