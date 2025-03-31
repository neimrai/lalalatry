import time
import random
import pandas as pd
import requests
import json

class XiaohongshuScraper:
    def __init__(self):
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Origin': 'https://www.xiaohongshu.com',
            'Referer': 'https://www.xiaohongshu.com',
            # 可能需要添加其他必要的headers
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_note_info(self, note_id):
        """获取笔记信息"""
        try:
            # 笔记详情API
            url = f'https://www.xiaohongshu.com/api/sns/web/v1/feed/{note_id}'
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取笔记信息失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取笔记信息出错: {str(e)}")
            return None

    def get_comments(self, note_id, cursor=""):
        """获取评论数据"""
        try:
            # 评论API
            url = f'https://www.xiaohongshu.com/api/sns/web/v2/comment/page'
            params = {
                'note_id': note_id,
                'cursor': cursor,
                'size': 20
            }
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取评论失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取评论出错: {str(e)}")
            return None

    def extract_comments(self, note_id):
        """提取所有评论"""
        comments = []
        cursor = ""
        
        while True:
            # 获取评论数据
            data = self.get_comments(note_id, cursor)
            if not data or 'data' not in data:
                break

            # 提取评论信息
            for comment in data['data'].get('comments', []):
                comment_data = {
                    "用户名": comment.get('user', {}).get('nickname'),
                    "评论内容": comment.get('content'),
                    "评论时间": comment.get('create_time'),
                    "点赞数": comment.get('like_count')
                }
                comments.append(comment_data)

            # 检查是否还有更多评论
            cursor = data['data'].get('cursor')
            if not cursor or not data['data'].get('has_more'):
                break

            # 随机等待，避免请求过快
            time.sleep(random.uniform(1, 2))

        print(f"成功提取{len(comments)}条评论")
        return comments

    def save_to_excel(self, data, filepath):
        """将数据保存到Excel文件"""
        try:
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False)
            print(f"数据已成功保存至: {filepath}")
        except Exception as e:
            print(f"保存Excel文件时出错: {str(e)}")

def main():
    # 创建爬虫实例
    scraper = XiaohongshuScraper()
    
    # 从URL中提取笔记ID
    note_id = "67e4256c000000000b015309"
    
    # 获取笔记信息
    note_info = scraper.get_note_info(note_id)
    if not note_info:
        print("无法获取笔记信息，程序退出")
        return
    
    # 提取评论数据
    comments_data = scraper.extract_comments(note_id)
    
    # 保存数据到Excel
    if comments_data:
        excel_path = f"comments_{note_id}.xlsx"
        scraper.save_to_excel(comments_data, excel_path)

if __name__ == "__main__":
    main()