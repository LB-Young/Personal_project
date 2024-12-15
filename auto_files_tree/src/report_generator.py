from typing import Dict

def generate_report(classification_results: Dict[str, list]) -> str:
    report = "文件整理报告:\n\n"
    
    for category, files in classification_results.items():
        report += f"类别: {category}\n"
        report += f"文件数量: {len(files)}\n"
        report += f"示例文件: {', '.join(files[:3])}\n\n"
    
    return report