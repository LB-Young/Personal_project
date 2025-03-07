# Web Content Extraction Service

这个项目提供了一系列工具服务，包括新添加的网页内容提取服务。该服务使用Jina.ai Reader API从指定URL列表提取网页内容，包括文本、标题和元数据。

## 功能特点

- 从多个URL批量提取网页内容
- 支持提取纯文本、标题和元数据
- 可选择性地提取网页中的图片
- 提供RESTful API接口
- 符合OpenAPI规范

## 安装

1. 克隆仓库：

```bash
git clone <repository-url>
cd <repository-directory>
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 启动服务

```bash
python server.py
```

服务将在 `http://localhost:3389` 上运行。

### API 端点

#### 提取网页内容

```
POST /extract_web_content
```

请求体示例：

```json
{
  "urls": ["https://example.com/article", "https://jina.ai/reader"],
  "extract_images": false
}
```

响应示例：

```json
{
  "answer": {
    "answer": {
      "https://example.com/article": {
        "title": "示例文章标题",
        "text": "这是从网页中提取的纯文本内容示例。这里包含了文章的主要内容，已经被清理和格式化。",
        "url": "https://example.com/article",
        "status": "success"
      },
      "https://jina.ai/reader": {
        "title": "Jina AI Reader",
        "text": "Reader API 将URL转换为LLM友好的输入，只需在前面添加r.jina.ai即可。",
        "url": "https://jina.ai/reader",
        "status": "success"
      }
    }
  }
}
```

### 测试服务

运行测试脚本：

```bash
python web_content_extractor_test.py
```

## API 文档

完整的API文档可以在以下文件中找到：

- `web_content_extractor_api.yaml` - 网页内容提取服务的OpenAPI规范

## 依赖项

- FastAPI
- Uvicorn
- Pydantic
- aiohttp
- BeautifulSoup4

## 注意事项

- 该服务使用Jina.ai Reader API，在生产环境中需要使用实际的API密钥和端点
- 请遵循网站的robots.txt规则和使用条款
- 添加适当的请求延迟以避免过度请求
- API密钥应该存储在环境变量或配置文件中，而不是硬编码在代码中 