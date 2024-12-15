# 导入环境变量
from dotenv import load_dotenv
load_dotenv()

# 创建Client
from openai import OpenAI
client = OpenAI()

# 创建一个线程
thread = client.beta.threads.create()
# 打印线程
print(thread)
"""
Thread(id='thread_Dh11LREODBbo8ciMCWGfVZxT', created_at=1723969296, metadata={}, object='thread', tool_resources=ToolResources(code_interpreter=None, file_search=None))
"""


# 向线程添加消息
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="我把每个花束定价为进价基础上加价20%,进价80元时,我的售价是多少。"
)
# 打印消息
print(message)
"""
Message(id='msg_cnLqEGWegxIeR5vkxvF1lM1P', assistant_id=None, attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], 
value='我把每个花束定价为进价基础上加价20%,进价80元时,我的售价是多少。'), type='text')], created_at=1723969296, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='user', run_id=None, status=None, thread_id='thread_Dh11LREODBbo8ciMCWGfVZxT')
"""
