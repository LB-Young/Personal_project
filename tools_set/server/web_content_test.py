#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import json

async def test_web_content_service():
    """
    测试web_content服务
    """
    # 测试URL列表
    urls = ["https://arxiv.org/pdf/2502.13130v1"]
    
    # 构建请求数据
    data = {
        "urls": urls
    }
    
    # 发送请求到服务
    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:3389/web_content", json=data) as response:
            if response.status == 200:
                result = await response.json()
                print("成功获取网页内容:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"请求失败，状态码: {response.status}")
                try:
                    error = await response.json()
                    print(f"错误信息: {json.dumps(error, indent=2, ensure_ascii=False)}")
                except:
                    text = await response.text()
                    print(f"响应内容: {text}")

if __name__ == "__main__":
    asyncio.run(test_web_content_service()) 