import requests

# 使用Jina Reader API格式的URL
url = 'https://r.jina.ai/https://github.com/Alibaba-NLP/ViDoRAG'
headers = {'Authorization': 'Bearer jina_96b4defcf63443a6bac47b925e172ab1dyLdulatxXX6jfMjmnTEafMXHxdp'}

response = requests.get(url, headers=headers)

# 将响应内容写入文件
with open('content1.txt', 'w', encoding='utf-8') as file:
    file.write(response.text)
