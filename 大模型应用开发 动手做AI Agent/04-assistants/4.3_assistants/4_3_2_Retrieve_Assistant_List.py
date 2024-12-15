# 导入环境变量
from dotenv import load_dotenv
load_dotenv()

# 创建Client
from openai import OpenAI
client = OpenAI()

# 检索您之前创建的Assistant
assistant_id = "asst_VLL6Dm8zg9qhMwEJUkUcNlbs" # Young创建的assistant
assistants = client.beta.assistants.list()
print(assistants)