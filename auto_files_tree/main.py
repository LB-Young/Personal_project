import os
from src.file_organizer import organize_files
from src.classification_rules import get_user_defined_categories
from src.report_generator import generate_report

def main():
    input_dir = r"F:\test_files"
    output_dir = r"F:\test_files_out"
    
    print("请输入5个文件类别,用逗号分隔(留空则使用LLM自动分类):")
    categories_input = input().strip()
    
    if categories_input:
        categories = categories_input.split(',')
        if len(categories) != 5:
            print("错误: 请确保输入了5个类别。")
            return
    else:
        categories = None
    
    results = organize_files(input_dir, output_dir, categories)
    report = generate_report(results)
    
    print(report)
    
    with open(os.path.join(output_dir, "organization_report.txt"), "w") as f:
        f.write(report)

if __name__ == "__main__":
    main()