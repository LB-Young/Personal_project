import os
import pytest
from tools.extract_tables_images_from_pdf import extract_tables_images_from_pdf

@pytest.fixture
def test_pdf_path():
    # 这里需要替换为实际的测试PDF文件路径
    return "/Users/liubaoyang/Desktop/flowchart/难选高钙白钨矿选矿技术研究.pdf"

@pytest.fixture
def output_dir(tmp_path):
    # 使用pytest的tmp_path fixture创建临时目录
    return str("/Users/liubaoyang/Desktop/flowchart" / 'output')

@pytest.mark.asyncio
async def test_params_format():
    """测试参数格式返回"""
    result = await extract_tables_images_from_pdf(params_format=True)
    assert result == ['file_path', 'picture_out_path']

@pytest.mark.asyncio
async def test_empty_params():
    """测试空参数异常"""
    with pytest.raises(Exception) as exc_info:
        await extract_tables_images_from_pdf()
    assert str(exc_info.value) == 'PDF路径和保存路径不能为空'

@pytest.mark.asyncio
async def test_invalid_pdf_path(output_dir):
    """测试无效的PDF文件路径"""
    with pytest.raises(Exception) as exc_info:
        await extract_tables_images_from_pdf('invalid.pdf', output_dir)
    assert str(exc_info.value) == 'PDF文件不存在'

@pytest.mark.asyncio
async def test_successful_extraction(test_pdf_path, output_dir):
    """测试成功提取表格和图片"""
    result = await extract_tables_images_from_pdf(test_pdf_path, output_dir)
    
    # 验证返回消息
    assert f'已成功从{test_pdf_path}提取表格和图片，保存在{output_dir}目录下' == result
    
    # 验证输出目录是否存在
    assert os.path.exists(output_dir)
    
    # 验证是否生成了图片文件
    files = os.listdir(output_dir)
    assert len(files) > 0
    
    # 验证生成的文件是否为PNG格式
    for file in files:
        assert file.endswith('.png')