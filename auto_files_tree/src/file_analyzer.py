import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_file_content(file_path: str, num_categories: int = 5) -> str:
    """使用LLM分析文件内容并返回类别"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        return "Binary"
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"分析以下文件内容并给出一个类别,总共分为{num_categories}类:\n\n{content[:1000]}\n\n类别:",
            }
        ],
        model="llama3-8b-8192",
    )
    
    return chat_completion.choices[0].message.content.strip()