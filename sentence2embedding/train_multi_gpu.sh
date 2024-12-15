torchrun --nproc_per_node 1 train_multi_gpu.py \
    --model_name_or_path "F:\Cmodels\models\bert_base_chinese" \
    --output_dir debug \
    --max_steps 10000 \
    --remove_unused_columns False \
    --learning_rate 5e-5 \
    --logging_steps 10 \
    --save_steps 500 \
    --warmup_ratio 0.0 \
    --per_device_train_batch_size 4 \
    --normalize True

# torchrun：分布式训练命令
# --nproc_per_node 2：每个节点运行的进程数
# train.py：训练脚本
# --model_name_or_path bert-base-uncased：预训练的模型
# --output_dir debug：输出日志
# --max_steps 10000：训练的最大步数
# --remove_unused_columns False：是否从数据中删除未使用的列
# --learning_rate 5e-5：学习率
# --logging_steps 10：日志打印频率
# --save_steps 500：保存频率
# --warmup_ratio 0.0：预热阶段比例（此处0表示没有预热阶段）
# --per_device_train_batch_size 16：批次大小
# --normalize True：是否对数据归一化处理