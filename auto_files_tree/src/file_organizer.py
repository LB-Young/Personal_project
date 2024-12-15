import os
import shutil
from typing import Dict, List
from .file_analyzer import analyze_file_content
from .classification_rules import create_classification_rules, classify_files_with_llm

def organize_files(input_dir: str, output_dir: str, categories: List[str] = None) -> Dict[str, list]:
    """遍历目录,分析并移动文件"""
    report = {}
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    
    if categories:
        classification_rules = create_classification_rules(categories)
        for filename in files:
            file_path = os.path.join(input_dir, filename)
            category = classify_file(file_path, classification_rules)
            move_file(file_path, output_dir, category, report)
    else:
        classification = classify_files_with_llm(files, lambda f: analyze_file_content(os.path.join(input_dir, f)), 5)
        for category, file_list in classification.items():
            for filename in file_list:
                file_path = os.path.join(input_dir, filename)
                move_file(file_path, output_dir, category, report)
    
    return report

def move_file(file_path: str, output_dir: str, category: str, report: Dict[str, list]):
    """移动文件到指定类别文件夹"""
    category_dir = os.path.join(output_dir, category)
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)
    
    new_file_path = os.path.join(category_dir, os.path.basename(file_path))
    shutil.move(file_path, new_file_path)
    
    if category not in report:
        report[category] = []
    report[category].append(os.path.basename(file_path))

def classify_file(file_path: str, rules: Dict[str, str]) -> str:
    """根据规则分类文件"""
    _, ext = os.path.splitext(file_path)
    return rules.get(ext.lower(), "Other")