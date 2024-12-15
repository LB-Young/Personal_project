import pytest
from unittest.mock import patch, MagicMock
from tools.paper_with_code import paper_with_code_search
from lxml import html

@pytest.mark.asyncio
async def test_paper_with_code_search_params_format():
    """测试参数格式返回"""
    result = await paper_with_code_search(params_format=True)
    assert isinstance(result, list)
    assert result == ['max_results']

@pytest.mark.asyncio
async def test_paper_with_code_search_success():
    """测试成功获取论文"""
    # 模拟主页HTML
    mock_main_html = """
    <div>
        <div class="row">
            <div>
                <h1><a href="/paper/test-paper">Test Paper Title</a></h1>
            </div>
        </div>
    </div>
    """
    
    # 模拟详情页HTML
    mock_detail_html = """
    <div>
        <main>
            <div>
                <p><span>March 20, 2024</span></p>
            </div>
            <div>
                <p>Test paper abstract</p>
            </div>
            <div>
                <div>
                    <div>42 stars</div>
                </div>
            </div>
        </main>
    </div>
    """
    
    # 模拟响应
    mock_main_response = MagicMock()
    mock_main_response.status = 200
    mock_main_response.text = MagicMock(return_value=mock_main_html)
    
    mock_detail_response = MagicMock()
    mock_detail_response.status = 200
    mock_detail_response.text = MagicMock(return_value=mock_detail_html)
    
    # 模拟session
    mock_session = MagicMock()
    mock_session.get.return_value.__aenter__.side_effect = [
        mock_main_response,
        mock_detail_response
    ]
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await paper_with_code_search(max_results=1)
        
        assert isinstance(result, list)
        assert len(result) == 1
        paper = result[0]
        assert paper['title'] == "Test Paper Title"
        assert paper['published_date'] == "March 20, 2024"
        assert paper['abstract'] == "Test paper abstract"
        assert paper['stars'] == 42

@pytest.mark.asyncio
async def test_paper_with_code_search_http_error():
    """测试HTTP错误"""
    mock_response = MagicMock()
    mock_response.status = 404
    
    mock_session = MagicMock()
    mock_session.get.return_value.__aenter__.return_value = mock_response
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        with pytest.raises(Exception) as exc_info:
            await paper_with_code_search(max_results=1)
        assert "HTTP错误: 404" in str(exc_info.value)

@pytest.mark.asyncio
async def test_paper_with_code_search_parse_error():
    """测试解析错误"""
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.text = MagicMock(return_value="<invalid>html</invalid>")
    
    mock_session = MagicMock()
    mock_session.get.return_value.__aenter__.return_value = mock_response
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await paper_with_code_search(max_results=1)
        assert isinstance(result, list)
        assert len(result) == 0