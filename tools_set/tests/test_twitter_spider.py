import pytest
from unittest.mock import patch, MagicMock
from tools.twitter_spider import twitter_spider
import json

@pytest.mark.asyncio
async def test_twitter_spider_params_format():
    """测试参数格式返回"""
    result = await twitter_spider(params_format=True)
    assert result == ['keyword', 'nums']

@pytest.mark.asyncio
async def test_twitter_spider_success():
    """测试成功获取推文"""
    # 模拟推文数据
    mock_tweet = MagicMock()
    mock_tweet.id_str = "123456"
    mock_tweet.text = "测试推文"
    mock_tweet.created_at = "2024-03-20 10:00:00"
    mock_tweet.user.screen_name = "test_user"
    mock_tweet.retweet_count = 10
    mock_tweet.favorite_count = 20

    # 模拟 tweepy.Cursor 返回的数据
    mock_cursor = MagicMock()
    mock_cursor.items.return_value = [mock_tweet]

    with patch('tweepy.OAuthHandler'), \
         patch('tweepy.API'), \
         patch('tweepy.Cursor', return_value=mock_cursor):
        
        result = await twitter_spider(keyword="测试", nums=1)
        tweets = json.loads(result)
        
        assert len(tweets) == 1
        assert tweets[0]['id'] == "123456"
        assert tweets[0]['text'] == "测试推文"
        assert tweets[0]['user'] == "test_user"
        assert tweets[0]['retweet_count'] == 10
        assert tweets[0]['favorite_count'] == 20

@pytest.mark.asyncio
async def test_twitter_spider_error():
    """测试异常情况"""
    with patch('tweepy.OAuthHandler', side_effect=Exception("API错误")):
        with pytest.raises(Exception) as exc_info:
            await twitter_spider(keyword="测试", nums=1)
        assert "爬取Twitter内容失败" in str(exc_info.value) 