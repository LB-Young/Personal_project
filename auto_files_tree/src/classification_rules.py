from typing import List, Dict
from collections import defaultdict

DEFAULT_RULES = {
    ".txt": "Text",
    ".pdf": "Document",
    ".doc": "Document",
    ".docx": "Document",
    ".xls": "Spreadsheet",
    ".xlsx": "Spreadsheet",
    ".jpg": "Image",
    ".png": "Image",
    ".mp3": "Audio",
    ".mp4": "Video",
}

def get_classification_rules():
    return DEFAULT_RULES

def add_classification_rule(extension: str, category: str):
    DEFAULT_RULES[extension.lower()] = category

def get_user_defined_categories() -> List[str]:
    """获取用户定义的类别列表"""
    categories = input("请输入文件类别,用逗号分隔(留空则使用LLM动态分类): ").strip()
    if categories:
        return [cat.strip() for cat in categories.split(',')]
    return []

def classify_files_with_llm(files: List[str], analyzer_func, num_categories: int = 5) -> Dict[str, List[str]]:
    """使用LLM动态分析文件并生成分类"""
    classification = defaultdict(list)
    for file in files:
        category = analyzer_func(file, num_categories)
        classification[category].append(file)
    return dict(classification)

def create_classification_rules(categories: List[str]) -> Dict[str, str]:
    """根据用户定义的类别创建分类规则"""
    rules = {}
    for category in categories:
        extensions = input(f"请输入 '{category}' 类别的文件扩展名,用逗号分隔: ").strip()
        for ext in extensions.split(','):
            rules[ext.strip().lower()] = category
    return rules