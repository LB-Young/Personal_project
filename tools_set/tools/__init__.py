from .dir_reader import dir_reader
from .wechatmp_spider import wechatmp_spider
from .save_to_local import save_to_local
from .paper_with_code import paper_with_code_search
from .send_email import send_email
from .youtube_caption import get_youtube_caption
from .finance.finance_news_search import finance_news_search
from .arxiv_search import arxiv_search
from .list_to_multiline_string import list_to_multiline_string
from .dict_to_multiline_string import dict_to_multiline_string
from .web_search_zhipu import web_search_zhipu
from .retrival_from_database import retrive_from_database
from .vl_model import vl_model
from .extract_tables_images_from_images import extract_tables_images_from_images
from .images_layout_analysis import images_layout_analysis
from .pdf2picture import pdf2pictures
from .flow_chart import flow_chart
from .mermaid_add_picture import mermaid_add_picture
from .duckduckgo_websearch import duckduckgo_websearch
from .jina_read_urls import jina_read_urls
from .jina_search import jina_search

other_tools = {
    "jina_read_urls": {
        "object": jina_read_urls,
        "describe": "使用Jina Reader API获取网页内容，需要参数{'urls': 待读取的URL列表}"
    },
    "jina_search": {
        "object": jina_search,
        "describe": "使用Jina Search API进行搜索，需要参数{'query': 搜索关键词}"
    },
    "web_search_zhipu": {
        "object": web_search_zhipu,
        "describe": "使用智谱AI搜索引擎进行网页搜索，需要参数{'keyword': 搜索关键词}"
    },
    "duckduckgo_websearch": {
        "object": duckduckgo_websearch,
        "describe": "使用DuckDuckGo搜索引擎进行网页搜索，需要参数{'query': 搜索关键词, 'num_results': 搜索结果数量}"
    },
    "retrive_from_database":{
        "object":retrive_from_database,
        "describe":"从数据库中检索数据，需要参数{'query':查询语句}",
    },
    "list_to_multiline_string":{
        "object":list_to_multiline_string,
        "describe":"把list转换为多行的字符串，需要参数{'list_data':待转换的list数据}",
    },
    "dict_to_multiline_string":{
        "object":dict_to_multiline_string,
        "describe":"把dict转换为多行的字符串，需要参数{'dict_data':待转换的dict数据}",
    },
    "arxiv_search":{
        "object":arxiv_search,
        "describe":"搜索arxiv上相关主题的论文，需要参数{'keyword':搜索的关键词, 'nums':搜索的论文数目}",
    },
    "finance_news_search":{
        "object":finance_news_search,
        "describe":"搜索关于金融的新闻，需要参数{'nums':搜索的新闻数目}",
    },
    "get_youtube_caption":{
        "object":get_youtube_caption,
        "describe":"提取yuotube视频的字幕，需要参数{'video_url':待提取的视频链接}",
    },
    "wechatmp_spider":{
        "object":wechatmp_spider,
        "describe":"微信公众号内容搜索器，需要参数{'keyword':搜索的关键词, 'nums':搜索文章数目}",
    },
    "dir_reader":{
        "object":dir_reader,
        "describe":"读取一个文件夹下的全部文件的内容，需要参数{'dirs':待读取的文件夹路径，格式为[dir1, dir22, ...]}",
    },
    "save_to_local":{
    "object":save_to_local,
    "describe":"将文本保存至本地，需要参数{'contents':需要保存的内容,'output_path':输出路径}",
    },
    "paper_with_code_search":{
        "object":paper_with_code_search,
        "describe":"读取paper with code 网站最新的论文，需要参数{'nums':需要读取的论文数目}",
    },
    "send_email": {
        "object":send_email,
        "describe":"发送邮件，需要参数{'subject':邮件主题，'content':邮件内容，'to':收件人邮箱地址列表}",
    },
    # 新增的四个工具
    "vl_model": {
        "object": vl_model,
        "describe": "提取图片中的文字内容，需要参数{'pic_path':图片路径}"
    },
    "extract_tables_images_from_images": {
        "object": extract_tables_images_from_images,
        "describe": "从图片中提取表格和图片，需要参数{'images_dir':图片目录, 'tables_images_outdir':输出目录}"
    },
    "images_layout_analysis": {
        "object": images_layout_analysis,
        "describe": "分析图片布局，需要参数{'images_dir':图片目录, 'layout_save_dir':布局保存目录}"
    },
    "pdf2pictures": {
        "object": pdf2pictures,
        "describe": "将PDF转换为图片，需要参数{'pdf_path':PDF文件路径, 'picture_save_path':图片保存路径}"
    },
    "flow_chart": {
        "object": flow_chart,
        "describe": "生成流程图，需要参数{'mermaid_string':mermaid字符串, 'output_path':输出路径}"
    },
    "mermaid_add_picture": {
        "object": mermaid_add_picture,
        "describe": "在mermaid流程图中添加图片，需要参数{'mermaid_string':mermaid字符串, 'pic_path':图片路径}"
    }
}

__all__ = other_tools