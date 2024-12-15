# 导入环境变量
from dotenv import load_dotenv
load_dotenv()

# 创建Client
from openai import OpenAI
client = OpenAI()

# 创建一个Run
run = client.beta.threads.runs.create(
  thread_id='thread_Dh11LREODBbo8ciMCWGfVZxT',
  assistant_id='asst_VLL6Dm8zg9qhMwEJUkUcNlbs',
  instructions="请回答问题." # 如果你希望覆盖原有的指令
)
# 打印Run
print(run)

# 再次获取Run的状态
run = client.beta.threads.runs.retrieve(
  thread_id='thread_Dh11LREODBbo8ciMCWGfVZxT',
  run_id=run.id
)
# 打印Run
print(run)

"""
Run(id='run_zviIRGTfH0dfiQyTOOEDOt57', assistant_id='asst_VLL6Dm8zg9qhMwEJUkUcNlbs', cancelled_at=None, completed_at=None, created_at=1723969494, expns=None, metadata={}, model='gpt-4-turbo-preview', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=None, status='queued', thread_id='thread_Dh11LREODBbo8ciMCWGfVZxT', tool_choice='auto', tools=[CodeInterpreterTool(type='code_interpreter')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={})


Run(id='run_zviIRGTfH0dfiQyTOOEDOt57', assistant_id='asst_VLL6Dm8zg9qhMwEJUkUcNlbs', cancelled_at=None, completed_at=None, created_at=1723969494, expires_at=1723970094, failed_at=None, incomplete_details=None, instructions='请回答问题.', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4-turbo-preview', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=1723969494, status='in_progress', thread_id='thread_Dh11LREODBbo8ciMCWGfVZxT', tool_choice='auto', tools=[CodeInterpreterTool(type='code_interpreter')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={})

"""