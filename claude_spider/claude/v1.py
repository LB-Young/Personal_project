import asyncio
from pyppeteer import launch
import time
import os

async def automate_claude():
    # 指定本地Chromium路径和用户数据目录
    chromium_path = r'E:\chromium\chrome-win\chrome.exe'
    user_data_dir = r'C:\Users\YoungL\AppData\Local\Chromium\User Data'
    
    # 启动配置
    browser = await launch(
        headless=False,
        executablePath=chromium_path,
        userDataDir=user_data_dir,  # 添加用户数据目录
        args=[
            '--start-maximized',
            '--profile-directory=Default'  # 使用默认配置文件
        ]
    )
    
    page = await browser.newPage()
    
    # 设置视窗大小
    await page.setViewport({'width': 1920, 'height': 1080})
    
    # 读取问题集
    with open('questions.txt', 'r', encoding='utf-8') as f:
        questions = f.readlines()
    
    for question in questions:
        try:
            # 打开新的Claude对话
            await page.goto('https://claude.ai/new')
            await page.waitForSelector('textarea', {'timeout': 10000})
            
            # 输入问题
            await page.type('textarea', question.strip())
            await asyncio.sleep(2)  # 等待新页面加载
            await page.keyboard.press('Enter')
            
            # 等待回答生成
            await page.waitForSelector('button[aria-label="Download"]', {'timeout': 30000})
            await asyncio.sleep(2)  # 确保答案完全生成
            
            # 下载答案
            await page.click('button[aria-label="Download"]')
            
            # 开始新对话
            await page.hover('.claude-logo')
            await page.waitForSelector('button:has-text("Start new chat")', {'timeout': 5000})
            await page.click('button:has-text("Start new chat")')
            
            await asyncio.sleep(2)  # 等待新页面加载
            
        except Exception as e:
            print(f"处理问题时出错: {question}")
            print(f"错误信息: {str(e)}")
            continue
    
    await browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(automate_claude()) 