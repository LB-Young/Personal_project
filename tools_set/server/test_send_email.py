import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from server import app
from send_email import send_email

client = TestClient(app)

@pytest.fixture
def mock_send_email():
    with patch('server.send_email', new_callable=AsyncMock) as mock:
        yield mock

@pytest.mark.asyncio
async def test_send_email_success(mock_send_email):
    # Mock成功响应
    mock_send_email.return_value = "邮件发送成功"
    
    test_data = {
        "subject": "测试邮件",
        "content": "这是一封测试邮件",
        "to": ["test1@example.com", "test2@example.com"]
    }
    
    response = client.post("/send_email", json=test_data)
    
    assert response.status_code == 200
    assert response.json() == {
        "answer": {
            "answer": "邮件发送成功"
        }
    }

@pytest.mark.asyncio
async def test_send_email_empty_content(mock_send_email):
    test_data = {
        "subject": "测试邮件",
        "content": "",
        "to": ["test@example.com"]
    }
    
    response = client.post("/send_email", json=test_data)
    
    assert response.status_code == 200
    assert response.json() == {
        "answer": {
            "answer": "邮件发送成功"
        }
    }

@pytest.mark.asyncio 
async def test_send_email_empty_recipients(mock_send_email):
    test_data = {
        "subject": "测试邮件",
        "content": "测试内容",
        "to": []
    }
    
    response = client.post("/send_email", json=test_data)
    
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_send_email_failure(mock_send_email):
    # Mock失败场景
    mock_send_email.side_effect = Exception("发送失败")
    
    test_data = {
        "subject": "测试邮件",
        "content": "测试内容",
        "to": ["test@example.com"]
    }
    
    response = client.post("/send_email", json=test_data)
    
    assert response.status_code == 500
    assert response.json() == {
        "detail": "发送失败"
    }
