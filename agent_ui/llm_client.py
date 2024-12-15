from openai import OpenAI

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key="sk-bbbb062c55f24dd5928f4c4448c37f1f", base_url="https://api.deepseek.com/v1")

    def ado_requests(self, prompt):
        print("prompt:", prompt)
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
