import pytest
from unittest.mock import patch, MagicMock
from tools.youtube_retrival import youtube_retrival  # 假设函数名为youtube_retrival

@pytest.mark.asyncio
async def test_youtube_retrival_params_format():
    """测试参数格式返回"""
    result = await youtube_retrival(params_format=True)
    assert isinstance(result, list)  # 验证返回参数列表

@pytest.mark.asyncio
async def test_youtube_retrival_success():
    """测试成功获取YouTube视频"""
    mock_video = {
        'id': 'video123',
        'title': '测试视频',
        'description': '视频描述',
        'publishedAt': '2024-03-20T10:00:00Z',
        'viewCount': '1000'
    }

    with patch('googleapiclient.discovery.build') as mock_build:
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.search.return_value.list.return_value.execute.return_value = {
            'items': [mock_video]
        }

        result = await youtube_retrival(keyword="测试", max_results=1)
        assert isinstance(result, str)  # 验证返回JSON字符串
        
@pytest.mark.asyncio
async def test_youtube_retrival_error():
    """测试异常情况"""
    with patch('googleapiclient.discovery.build', side_effect=Exception("API错误")):
        with pytest.raises(Exception) as exc_info:
            await youtube_retrival(keyword="测试", max_results=1)
        assert "获取YouTube视频失败" in str(exc_info.value) 