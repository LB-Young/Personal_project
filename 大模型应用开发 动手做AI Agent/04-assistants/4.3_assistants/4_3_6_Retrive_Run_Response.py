# 导入环境变量
from dotenv import load_dotenv
load_dotenv()

# 创建Client
from openai import OpenAI
client = OpenAI()

# 刚才创建的Thread的ID
thread_id = 'thread_Dh11LREODBbo8ciMCWGfVZxT' 

# 读取线程的消息
messages = client.beta.threads.messages.list(
  thread_id=thread_id
)
# 打印消息
print(messages)
