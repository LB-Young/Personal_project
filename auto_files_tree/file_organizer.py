import os
import shutil
from typing import List
import openai  # 假设我们使用OpenAI的API

# 设置OpenAI API密钥
openai.api_key = 'your-api-key-here'

def analyze_file_content(file_path: str) -> str:
    """使用LLM分析文件内容并返回类别"""
    with open(file_path, 'r') as file:
        content = file.read()
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"分析以下文件内容并给出一个类别:\n\n{content}\n\n类别:",
        max_tokens=50
    )
    
    return response.choices[0].text.strip()

def organize_files(directory: str):
    """遍历目录,分析并移动文件"""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            category = analyze_file_content(file_path)
            category_dir = os.path.join(directory, category)
            
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
            
            shutil.move(file_path, os.path.join(category_dir, filename))
            print(f"Moved {filename} to {category}")

if __name__ == "__main__":
    target_directory = "path/to/your/directory"
    organize_files(target_directory)