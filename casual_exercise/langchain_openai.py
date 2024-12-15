# from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
# # openai_api_key="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"
# llm = OpenAI()
# chat_model = ChatOpenAI()

# llm.predict("hi!")

# chat_model.predict("hi!")










import openai

# Set your API key
api_key = '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'
openai.api_key = api_key

# Prompt for the AI to generate a completion
prompt_text = "Once upon a time"
response = openai.ChatCompletion.create(
  model="text-davinci-003",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt_text}
  ]
)

print(response.choices[0].text.strip())