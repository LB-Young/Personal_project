import pytest
from unittest.mock import patch, MagicMock
from tools.bilibili_retrival import bilibili_retrival  # 假设函数名为bilibili_retrival

@pytest.mark.asyncio
async def test_bilibili_retrival_params_format():
    """测试参数格式返回"""
    result = await bilibili_retrival(params_format=True)
    assert isinstance(result, list)  # 验证返回参数列表

@pytest.mark.asyncio
async def test_bilibili_retrival_success():
    """测试成功获取B站视频"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'data': {
            'result': [{
                'aid': 12345,
                'title': '测试视频',
                'description': '视频描述',
                'author': '测试用户',
                'play': 1000,
            }]
        }
    }

    with patch('aiohttp.ClientSession') as mock_session:
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response
        
        result = await bilibili_retrival(keyword="测试", max_results=1)
        assert isinstance(result, str)  # 验证返回JSON字符串

@pytest.mark.asyncio
async def test_bilibili_retrival_error():
    """测试异常情况"""
    with patch('aiohttp.ClientSession', side_effect=Exception("网络错误")):
        with pytest.raises(Exception) as exc_info:
            await bilibili_retrival(keyword="测试", max_results=1)
        assert "获取B站视频失败" in str(exc_info.value) 