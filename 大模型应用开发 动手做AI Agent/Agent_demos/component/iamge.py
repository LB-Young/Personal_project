# 导入OpenAI库
from openai import OpenAI

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 初始化OpenAI客户端
client = OpenAI()

# 请求DALL-E生成图片
response = client.images.generate(
  model="dall-e-3",
  prompt="电商永恒之夏宣传海报，配上文案",
  size="1024x1024",
  quality="standard",
  n=1,
)
breakpoint()
# 获取图片URL
image_url = response.data[0].url

# 读取图片
import requests
image = requests.get(image_url).content

# 在Notebook中显示图片
from IPython.display import Image
Image(image)
