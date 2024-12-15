import pytest
from unittest.mock import patch, MagicMock
from tools.wechatmp_spider import wechatmp_spider  # 假设函数名为wechatmp_spider

@pytest.mark.asyncio
async def test_wechatmp_spider_params_format():
    """测试参数格式返回"""
    result = await wechatmp_spider(params_format=True)
    assert isinstance(result, list)  # 验证返回参数列表

@pytest.mark.asyncio
async def test_wechatmp_spider_success():
    """测试成功获取微信公众号文章"""
    mock_article = {
        'title': '测试文章',
        'content': '文章内容',
        'publish_time': '2024-03-20',
        'author': '测试作者'
    }

    with patch('wechatmp_sdk.WeChatMP') as mock_wechat:
        mock_wechat.return_value.get_articles.return_value = [mock_article]
        
        result = await wechatmp_spider(account="test_account", max_num=1)
        assert isinstance(result, str)  # 验证返回JSON字符串

@pytest.mark.asyncio
async def test_wechatmp_spider_error():
    """测试异常情况"""
    with patch('wechatmp_sdk.WeChatMP', side_effect=Exception("API错误")):
        with pytest.raises(Exception) as exc_info:
            await wechatmp_spider(account="test_account", max_num=1)
        assert "获取微信公众号文章失败" in str(exc_info.value) 