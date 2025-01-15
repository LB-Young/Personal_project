from .dir_reader import DirReader
from .wechatmp_spider import WechatSpider
from .save_to_local import SaveToLocal
from .paper_with_code import PaperWithCodeSearch
from .send_email import SendEmail
from .youtube_caption import GetYoutubeCaption
from .finance.finance_news_search import FinanceNewsSearch
from .arxiv_search import ArxivSearch
from .list_to_multiline_string import ListToMultilineString

other_tools = {
    "list_to_multiline_string":ListToMultilineString,
    "arxiv_search":ArxivSearch,
    "finance_news_search":FinanceNewsSearch,
    "get_youtube_caption":GetYoutubeCaption,
    "wechatmp_spider":WechatSpider,
    "dir_reader":DirReader,
    "save_to_local":SaveToLocal,
    "paper_with_code_search":PaperWithCodeSearch,
    "send_email": SendEmail,
}

__all__ = other_tools