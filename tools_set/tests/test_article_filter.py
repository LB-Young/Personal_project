import pytest
from tools.artical_fiter import article_filter

@pytest.mark.asyncio
async def test_article_filter_params_format():
    """测试参数格式返回"""
    test_articles = [
        {'content': '测试文章1'},
        {'content': '测试文章2'}
    ]
    result = await article_filter(articles=test_articles, query='')
    assert isinstance(result, list)

@pytest.mark.asyncio
async def test_article_filter_success():
    """测试文章过滤功能"""
    test_articles = [
        {
            'content': '这是一篇关于人工智能的文章，讨论了机器学习的应用',
            'title': 'AI文章'
        },
        {
            'content': '今天的天气真不错，阳光明媚',
            'title': '天气'
        },
        {
            'content': '深度学习在计算机视觉领域取得了重大突破',
            'title': '深度学习'
        }
    ]
    
    # 测试相关查询
    result = await article_filter(
        articles=test_articles,
        query='人工智能 机器学习'
    )
    assert len(result) >= 1
    assert '人工智能' in result[0]['content']
    
    # 测试无关查询
    result = await article_filter(
        articles=test_articles,
        query='足球比赛'
    )
    assert len(result) == 0

@pytest.mark.asyncio
async def test_article_filter_empty_query():
    """测试空查询"""
    test_articles = [
        {'content': '测试文章1'},
        {'content': '测试文章2'}
    ]
    result = await article_filter(articles=test_articles, query='')
    assert len(result) == len(test_articles)

@pytest.mark.asyncio
async def test_article_filter_invalid_input():
    """测试无效输入"""
    # 测试None输入
    with pytest.raises(Exception) as exc_info:
        await article_filter(articles=None, query='测试')
    assert "无效的文章列表" in str(exc_info.value)
    
    # 测试错误的文章格式
    with pytest.raises(Exception) as exc_info:
        await article_filter(articles=[{'wrong_key': 'value'}], query='测试')
    assert "文章格式错误" in str(exc_info.value)

@pytest.mark.asyncio
async def test_article_filter_threshold():
    """测试相似度阈值"""
    test_articles = [
        {'content': '人工智能和机器学习'},
        {'content': '完全无关的内容'}
    ]
    
    # 测试相似度过滤
    result = await article_filter(
        articles=test_articles,
        query='AI'
    )
    
    # 验证结果
    assert isinstance(result, list)