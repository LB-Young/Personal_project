import pytest
import os
import json
from tools.save_to_local import save_to_local

@pytest.mark.asyncio
async def test_save_to_local_success(tmp_path):
    """测试成功保存文件"""
    test_data = {"test": "数据"}
    file_path = tmp_path / "test.json"
    
    result = await save_to_local(
        data=test_data,
        file_path=str(file_path),
        format='json'
    )
    
    assert os.path.exists(file_path)
    assert result is True
    
    # 验证文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
        assert saved_data == test_data

@pytest.mark.asyncio
async def test_save_to_local_invalid_input():
    """测试无效输入"""
    with pytest.raises(Exception) as exc_info:
        await save_to_local(data=None, file_path="test.json")
    assert "无效的输入参数" in str(exc_info.value)
    
    with pytest.raises(Exception) as exc_info:
        await save_to_local(data={}, file_path="")
    assert "无效的输入参数" in str(exc_info.value)

@pytest.mark.asyncio
async def test_save_to_local_invalid_format():
    """测试无效的文件格式"""
    with pytest.raises(Exception) as exc_info:
        await save_to_local(data={}, file_path="test.xyz", format='xyz')
    assert "不支持的文件格式" in str(exc_info.value)

@pytest.mark.asyncio
async def test_save_to_local_nested_path(tmp_path):
    """测试嵌套路径创建"""
    test_data = {"test": "数据"}
    nested_path = tmp_path / "a" / "b" / "c"
    file_path = nested_path / "test.json"
    
    result = await save_to_local(
        data=test_data,
        file_path=str(file_path),
        format='json'
    )
    
    assert os.path.exists(file_path)
    assert result is True