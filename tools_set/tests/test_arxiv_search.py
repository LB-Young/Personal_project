import pytest
from unittest.mock import patch, MagicMock
from tools.arxiv_search import arxiv_search

@pytest.mark.asyncio
async def test_arxiv_search_params_format():
    """测试参数格式返回"""
    result = await arxiv_search(params_format=True)
    assert isinstance(result, list)
    assert set(result) == {'keyword', 'max_results'}

@pytest.mark.asyncio
async def test_arxiv_search_success():
    """测试成功搜索论文"""
    mock_paper = MagicMock()
    mock_paper.title = "Test Paper"
    mock_paper.authors = ["Author 1", "Author 2"]
    mock_paper.published = "2024-03-20"
    mock_paper.summary = "This is a test paper"
    mock_paper.pdf_url = "https://arxiv.org/pdf/1234.5678"

    with patch('arxiv.Search') as mock_search:
        mock_search.return_value = [mock_paper]
        
        result = await arxiv_search(keyword="machine learning", max_results=1)
        papers = result
        
        assert isinstance(papers, list)
        assert len(papers) == 1
        assert papers[0]['title'] == "Test Paper"
        assert papers[0]['authors'] == ["Author 1", "Author 2"]
        assert papers[0]['summary'] == "This is a test paper"
        assert papers[0]['pdf_url'] == "https://arxiv.org/pdf/1234.5678"

@pytest.mark.asyncio
async def test_arxiv_search_empty_result():
    """测试搜索结果为空"""
    with patch('arxiv.Search', return_value=[]):
        result = await arxiv_search(keyword="nonexistent", max_results=1)
        assert isinstance(result, list)
        assert len(result) == 0

@pytest.mark.asyncio
async def test_arxiv_search_error():
    """测试搜索异常"""
    with patch('arxiv.Search', side_effect=Exception("API错误")):
        with pytest.raises(Exception) as exc_info:
            await arxiv_search(keyword="test", max_results=1)
        assert "获取arXiv论文失败" in str(exc_info.value) 