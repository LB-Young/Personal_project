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
            await page.keyboard.press('Enter')
            
            # 等待答案生成
            print("等待答案生成...")
            await asyncio.sleep(60)  # 确保答案完全生成
            try:
                # 等待输入指示器出现和消失
                await page.waitForSelector('.typing-indicator', {'timeout': 10000})
                await page.waitForFunction(
                    'document.querySelector(".typing-indicator") === null',
                    {'timeout': 120000}  # 最多等待2分钟
                )
                await asyncio.sleep(2)  # 额外等待确保内容加载完成
            except Exception as e:
                print(f"等待答案生成时出错: {str(e)}")
                continue
                
            # 保存答案到本地文件
            print("正在保存答案...")
            response_element = await page.querySelector('.claude-response')
            if response_element:
                response_text = await page.evaluate('(element) => element.textContent', response_element)
                file_name = f"{question.strip()}.txt"
                file_name = "".join(c for c in file_name if c.isalnum() or c in (' ', '-', '_')).strip()
                file_path = os.path.join('claude_answers', file_name)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response_text)
                print(f"已保存答案到: {file_path}")
            
            # 开始新对话
            print("准备开始新对话...")
            await page.hover('.claude-logo')
            await asyncio.sleep(1)
            start_new_chat_button = await page.waitForSelector('button:has-text("Start new chat")', {'timeout': 5000})
            if start_new_chat_button:
                await start_new_chat_button.click()
            await asyncio.sleep(2)  # 等待新页面加载
            
        except Exception as e:
            print(f"处理问题时出错: {question}")
            print(f"错误信息: {str(e)}")
            continue
    
    await browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(automate_claude()) 