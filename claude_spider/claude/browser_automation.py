# 导入异步IO库
import asyncio
# 导入pyppeteer浏览器自动化库
from pyppeteer import launch
# 导入时间处理库
import time
# 导入操作系统功能库
import os

# 定义主要的异步函数
async def automate_claude():
    # 设置Chromium浏览器可执行文件路径
    chromium_path = r'E:\chromium\chrome-win\chrome.exe'
    # 设置用户数据目录路径
    user_data_dir = r'C:\Users\YoungL\AppData\Local\Chromium\User Data'
    
    # 创建保存答案的目录名
    answers_dir = 'claude_answers'
    # 如果目录不存在则创建
    if not os.path.exists(answers_dir):
        os.makedirs(answers_dir)
    
    # 启动浏览器实例
    browser = await launch(
        headless=False,  # 显示浏览器界面
        executablePath=chromium_path,  # 指定浏览器路径
        userDataDir=user_data_dir,  # 指定用户数据目录
        args=[
            '--start-maximized',  # 最大化窗口
            '--profile-directory=Default'  # 使用默认配置文件
        ]
    )
    
    # 创建新标签页
    page = await browser.newPage()
    # 设置视窗大小
    await page.setViewport({'width': 1920, 'height': 1080})
    
    # 读取问题文件
    with open('questions.txt', 'r', encoding='utf-8') as f:
        questions = f.readlines()
    
    # 遍历每个问题
    for question in questions:
        try:
            # 去除问题前后的空白字符
            question = question.strip()
            print(f"正在处理问题: {question}")
            
            # 打开Claude新对话页面
            await page.goto('https://claude.ai/new')
            # 等待输入框出现
            await page.waitForSelector('textarea', {'timeout': 10000})
            # 输入问题
            await page.type('textarea', question)
            # 按回车发送问题
            await page.keyboard.press('Enter')
            
            # 等待答案生成
            print("等待答案生成...")
            await asyncio.sleep(60)  # 确保答案完全生成
            try:
                # 等待输入指示器出现
                await page.waitForSelector('.typing-indicator', {'timeout': 10000})
                # 等待输入指示器消失（表示回答完成）
                await page.waitForFunction(
                    'document.querySelector(".typing-indicator") === null',
                    {'timeout': 120000}  # 最多等待2分钟
                )
                # 额外等待2秒确保内容完全加载
                await asyncio.sleep(2)
            except Exception as e:
                print(f"等待答案生成时出错: {str(e)}")
                continue
            
            # 保存答案
            print("正在保存答案...")
            # 获取回答元素
            response_element = await page.querySelector('.claude-response')
            if response_element:
                # 提取回答文本
                response_text = await page.evaluate('(element) => element.textContent', response_element)
                
                # 生成文件名
                file_name = f"{question}.txt"
                # 清理文件名（只保留字母数字和部分标点）
                file_name = "".join(c for c in file_name if c.isalnum() or c in (' ', '-', '_')).strip()
                # 组合完整的文件路径
                file_path = os.path.join(answers_dir, file_name)
                
                # 将答案写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response_text)
                print(f"已保存答案到: {file_path}")
            
            # 开始新对话
            print("准备开始新对话...")
            # 鼠标悬停在Claude图标上
            await page.hover('.claude-logo')
            # 等待下拉菜单显示
            await asyncio.sleep(1)
            
            # 等待并点击"开始新对话"按钮
            start_new_chat_button = await page.waitForSelector('button:has-text("Start new chat")', {'timeout': 5000})
            if start_new_chat_button:
                await start_new_chat_button.click()
                # 等待页面跳转完成
                await asyncio.sleep(2)
            
            print("完成一轮对话，准备下一个问题...")
            
        # 捕获并处理可能的错误
        except Exception as e:
            print(f"处理问题时出错: {question}")
            print(f"错误信息: {str(e)}")
            continue
    
    # 关闭浏览器
    await browser.close()

# 程序入口点
if __name__ == '__main__':
    # 运行异步主函数
    asyncio.get_event_loop().run_until_complete(automate_claude()) 