import requests

def get_papers_simple():
    url = "http://47.94.46.58:3389/papers/list"
    payload = {"nums": 2}  # 获取5篇论文
    
    try:
        response = requests.post(url, json=payload)
        breakpoint()
        data = response.json()
        breakpoint()
        # 打印每篇论文的基本信息
        for paper in data['answer']:
            print(f"\n论文标题: {paper['title']}")
            print(f"作者: {', '.join(paper['authors'])}")
            print(f"URL: {paper['url']}")
            print("-" * 30)
            
    except Exception as e:
        print(f"发生错误: {e}")

    url = "http://47.94.46.58:3389/list_to_multiline_string"
    payload = {
        "list_content": [paper['title'] for paper in data['answer']]
    }
    response = requests.post(url, json=payload)
    data = response.json()
    print(data)

    url = "http://47.94.46.58:3389/send_email"
    payload = {
        "subject": "daily paper recommend",
        "content": data['answer'],
        "to": ['lby15356@gmail.com']
    }
    response = requests.post(url, json=payload)
    data = response.json()
    print(data)
if __name__ == "__main__":
    get_papers_simple()