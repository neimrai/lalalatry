import requests
import time
import random

def get_page_source(url):
    """
    获取指定URL的网页源代码
    
    Args:
        url (str): 要获取源代码的网页URL
    
    Returns:
        str: 网页源代码
    """
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # 发送GET请求
        response = requests.get(url, headers=headers, timeout=10)
        
        # 检查响应状态码
        if response.status_code == 200:
            # 设置正确的编码
            response.encoding = response.apparent_encoding
            # 返回网页源代码
            return response.text
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("请求超时")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {str(e)}")
        return None

def save_to_file(content, filename):
    """
    将内容保存到文件
    
    Args:
        content (str): 要保存的内容
        filename (str): 文件名
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"源代码已保存到: {filename}")
    except Exception as e:
        print(f"保存文件时出错: {str(e)}")

def main():
    # 要爬取的URL
    url = input("请输入要获取源代码的网址: ")
    
    # 获取网页源代码
    print("正在获取网页源代码...")
    source = get_page_source(url)
    
    if source:
        # 生成文件名（使用时间戳避免重名）
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"source_{timestamp}.html"
        
        # 保存到文件
        save_to_file(source, filename)
    else:
        print("获取源代码失败")

if __name__ == "__main__":
    main()
