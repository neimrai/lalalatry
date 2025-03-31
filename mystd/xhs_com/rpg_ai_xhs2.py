import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class XiaohongshuScraper:
    def __init__(self):
        # 设置Chrome选项
        chrome_options = Options()
        # 添加一些选项来避免检测
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # 初始化WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
        })
        
        # 设置等待时间
        self.wait = WebDriverWait(self.driver, 10)
        
    def open_page(self, url):
        """打开指定URL的页面"""
        try:
            self.driver.get(url)
            # 等待页面加载完成
            time.sleep(3)
            return True
        except TimeoutException:
            print("页面加载超时，正在重试...")
            return False
            
    def get_page_title(self):
        """获取页面标题"""
        return self.driver.title
    
    def scroll_page(self, scroll_times=123):
        """滚动页面以加载更多内容"""
        for i in range(scroll_times):
            # 滚动页面
            self.driver.execute_script("window.scrollBy(0, 300);")
            # 随机等待时间，模拟人工操作
            time.sleep(random.uniform(0.1, 0.3))
            
            # 检查是否到达页面底部
            if self.check_end_element():
                print(f"已到达页面底部，共滚动{i+1}次")
                break
            
            # 每滚动10次暂停一下，避免被检测
            if (i + 1) % 10 == 0:
                wait_time = random.uniform(1, 3)
                print(f"已滚动{i+1}次，暂停{wait_time:.1f}秒")
                time.sleep(wait_time)
    
    def check_end_element(self):
        """检查是否存在表示页面底部的元素"""
        try:
            # 查找页面底部元素，根据实际情况调整选择器
            end_element = self.driver.find_element(By.XPATH, "//*[contains(text(), '- THE END -')]")
            return end_element.is_displayed()
        except NoSuchElementException:
            return False
    
    def extract_comments(self):
        """提取页面中的一级评论"""
        comments = []
        try:
            # 根据实际情况调整选择器
            comment_elements = self.driver.find_elements(By.CSS_SELECTOR, ".comment-item")
            
            for element in comment_elements:
                try:
                    # 提取评论内容、用户名、时间等信息
                    
                    username = element.find_element(By.CSS_SELECTOR, ".author").text
                    content = element.find_element(By.CSS_SELECTOR, ".note-text").text
                    num = element.find_element(By.CSS_SELECTOR, ".count").text
                    
                    comment_data = {
                        "用户名": username,
                        "评论内容": content,
                        "评论点赞量": num
                    }
                    
                    # 可以根据需要提取更多信息
                    comments.append(comment_data)
                except Exception as e:
                    print(f"提取单条评论时出错: {str(e)}")
                    continue
            
            print(f"成功提取{len(comments)}条评论")
            return comments
        
        except Exception as e:
            print(f"提取评论时出错: {str(e)}")
            return comments
    
    def save_to_excel(self, data, filepath):
        """将数据保存到Excel文件"""
        try:
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False)
            print(f"数据已成功保存至: {filepath}")
        except Exception as e:
            print(f"保存Excel文件时出错: {str(e)}")
    
    def close_browser(self):
        """关闭浏览器"""
        self.driver.quit()
        print("浏览器已关闭")

def main():
    # 创建爬虫实例
    scraper = XiaohongshuScraper()
    
    # 小红书帖子URL
    url = "https://www.xiaohongshu.com/explore/67e4256c000000000b015309"
    
    # 打开页面
    success = scraper.open_page(url)
    if not success:
        print("无法打开页面，程序退出")
        scraper.close_browser()
        return
    
    # 获取页面标题
    page_title = scraper.get_page_title()
    print(f"页面标题: {page_title}")
    
    # 滚动页面加载更多评论
    scraper.scroll_page()
    
    # 等待一段随机时间
    time.sleep(random.uniform(1, 3))
    
    # 提取评论数据
    comments_data = scraper.extract_comments()
    
    # 保存数据到Excel
    if comments_data:
        excel_path = f"C:\\Users\\EDY\\Desktop\\{page_title}.xlsx"
        scraper.save_to_excel(comments_data, excel_path)
    
    # 关闭浏览器
    scraper.close_browser()

if __name__ == "__main__":
    main()
