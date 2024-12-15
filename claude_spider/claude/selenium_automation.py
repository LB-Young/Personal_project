from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def automate_claude():
    # 设置Chrome选项
    chrome_options = webdriver.ChromeOptions()
    # 设置用户数据目录
    chrome_options.add_argument(r'--user-data-dir=C:\Users\86187\AppData\Local\Chromium\User Data')
    # chrome_options.add_argument(r"user-data-dir=E:\chromium\chrome-win\chrome.exe")
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument('--start-maximized')
    
    # 指定Chrome浏览器路径
    chrome_path = r'E:\chromium\chrome-win\chrome.exe'
    chrome_options.binary_location = chrome_path
    
    # 创建保存答案的目录
    answers_dir = 'claude_answers'
    if not os.path.exists(answers_dir):
        os.makedirs(answers_dir)
    
    # 初始化浏览器
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)  # 设置显式等待时间为20秒
    
    try:
        # 读取问题文件
        with open('questions.txt', 'r', encoding='utf-8') as f:
            questions = f.readlines()
        
        # 处理每个问题
        for question in questions:
            try:
                question = question.strip()
                print(f"正在处理问题: {question}")
                
                # 打开Claude新对话页面
                driver.get('https://claude.ai/new')
                
                # 等待输入框出现并输入问题
                textarea = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/main/div[2]/div/fieldset/div[1]/div[1]/div[1]/div')))
                textarea.send_keys(question)
                time.sleep(10)  # 等待2秒
                send_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/main/div[2]/div/fieldset/div[1]/div[1]/div[2]/div/div/button')))
                send_button.click()
                
                # 等待答案生成
                print("等待答案生成...")
                time.sleep(30)  # 等待60秒确保答案生成完成
                """
                /html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[4]/div/div/div[1]/div/div
                /html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/div
                """
                # 获取答案内容
                print("正在获取答案...")
                answer_element = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/div')))
                answer = answer_element.text
                
                # # 从剪贴板获取答案文本
                # from selenium.webdriver.common.action_chains import ActionChains
                # actions = ActionChains(driver)
                # actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                # answer = driver.find_element(By.TAG_NAME, 'body').text
                
                # 保存答案到文件
                file_name = f"{question}.txt"
                file_name = "".join(c for c in file_name if c.isalnum() or c in (' ', '-', '_')).strip()
                file_path = os.path.join(answers_dir, file_name)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(answer))
                print(f"已保存答案到: {file_path}")
                
                # 开始新对话
                print("准备开始新对话...")
                # 点击Claude图标开启新对话
                new_chat_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[3]/nav/div[2]/div[3]/div[2]/div[1]/ul/li/a')))
                new_chat_button.click()
                
                time.sleep(2)  # 等待页面加载
                print("完成一轮对话，准备下一个问题...")
                
            except Exception as e:
                print(f"处理问题时出错: {question}")
                print(f"错误信息: {str(e)}")
                continue
                
    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == '__main__':
    automate_claude()
