# 导入环境变量
from dotenv import load_dotenv 
load_dotenv()
# 创建 client
from openai import OpenAI 
client = OpenAI()
# 创建 assistant
assistant = client.beta.assistants.create(
    name=" 鲜花价格计算器 ",
    instructions=" 你能够帮我计算鲜花的价格 ", tools=[{"type": "code_interpreter"}], model="gpt-4-turbo-preview"
    )
# 打印 assistant print(assistant)
print(assistant)

"""
response = Assistant(id='asst_VLL6Dm8zg9qhMwEJUkUcNlbs', created_at=1723968657, description=None, instructions=' 你能够帮我计算鲜花的价格 ', metadata={}, model='gpt-4-turbo-preview', name=' 鲜花价格计算器 ', object='assistant', tools=[CodeInterpreterTool(type='code_interpreter')], response_format='auto', temperature=1.0, tool_resources=ToolResources(code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]), file_search=None), 
top_p=1.0)
"""

