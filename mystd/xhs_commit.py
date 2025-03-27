import json
import time
import random
import execjs
import requests
from loguru import logger
import re
from fetch_details import fetch_xiaohongshu_data
import pandas as pd
import os
from datetime import datetime
 
img_path='result'
output_file_path = "result.csv"
 
# 初始化 CSV 文件并写入表头
if not os.path.exists(output_file_path):
    with open(output_file_path, mode="w", encoding="utf-8-sig", newline="") as f:
        f.write("note_url,last_update_time,note_id,xsec_token,type,title,text,topics,likes,comments,collects,shares\n")
 
def base36encode(number, digits='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    base36 = ""
    while number:
        number, i = divmod(number, 36)
        base36 = digits[i] + base36
    return base36.lower()
def generate_search_id():
    timestamp = int(time.time() * 1000) << 64
    random_value = int(random.uniform(0, 2147483646))
    return base36encode(timestamp + random_value)
def parse_data(data):
    items = data.get('data', {}).get('items', [])
    parsed_info = []
 
    for item in items:
        note = item.get('note_card', {})
        title = note.get('title', '')
        desc = note.get('desc', '')
 
        # 提取并清理话题
        topics = [word.strip('#').replace('[话题]', '').strip() for word in desc.split() if '[话题]' in word]
        desc_cleaned = ' '.join([word for word in desc.split() if '[话题]' not in word]).strip()
 
        interact_info = note.get('interact_info', {})
        liked_count = interact_info.get('liked_count', 0)
        comment_count = interact_info.get('comment_count', 0)
        collected_count = interact_info.get('collected_count', 0)
        share_count = interact_info.get('share_count', 0)
 
        parsed_info.append({
            '标题': title,
            '内容': desc_cleaned,
            '点赞数': liked_count,
            '评论数': comment_count,
            '收藏数': collected_count,
            '转发数': share_count,
            '话题': topics
        })
 
    return parsed_info
 
 
def convert_to_int(value):
    if '万' in value:
        value = value.replace('万', '')
        return float(value) * 10000  # 转换为万单位的整数
    else:
        return value
 
search_data = {
    "keyword": "关键词",
    "page": 1,#爬的页数游标，需要不断更改
    "page_size": 20,#不用修改
    "search_id": generate_search_id(),
    "sort": "general",#排序的方式 综合，最热，最新
    "note_type": 0
}
cookies={‘你自己的cookies’
}
 
headers = {‘你自己的请求头’}
 
url = 'https://edith.xiaohongshu.com/api/sns/web/v1/search/notes'
api_endpoint = '/api/sns/web/v1/search/notes'
a1_value=cookies['a1']
 
 
for page in range(1,12):
    search_data['page'] = str(page)
    with open('1.js', 'r', encoding='utf-8') as f:
        js_script = f.read()
        context = execjs.compile(js_script)
        sign = context.call('getXs', api_endpoint, search_data, a1_value)
 
    GREEN = "\033[1;32;40m  %s  \033[0m"
 
    headers['x-s'] = sign['X-s']
    headers['x-t'] = str(sign['X-t'])
    headers['X-s-common'] = sign['X-s-common']
    response = requests.post(url, headers=headers, data=json.dumps(search_data, separators=(",", ":"), ensure_ascii=False).encode('utf-8'))
    logger.info(f'{response.json()}')
    if response.status_code==200:
 
        data = response.json()
        notes = data.get('data', {}).get('items', [])
        for note in notes:
            try:
                xsec_token = note.get('xsec_token')
                note_id = note.get('id')
                note_url='https://www.xiaohongshu.com/explore/'+note_id+'?xsec_token='+xsec_token+'&xsec_source=pc_feed'
                note_data, status_code_result, headers_result = fetch_xiaohongshu_data(note_id, xsec_token, cookies)
                print(note_data)
                time=note_data['data']['items'][0]['note_card'].get('last_update_time', 'N/A')
                datetime_obj = datetime.utcfromtimestamp(time / 1000)
                last_update_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
                note_type = note_data['data']['items'][0]['note_card'].get('type', 'N/A')
                img_urls = []
                image_urls = [img['url_default'] for img in note_data['data']['items'][0]['note_card']['image_list'] if
                              'url_default' in img]
 
                output_dir = f"./{img_path}/{note_id}"
                os.makedirs(output_dir, exist_ok=True)
 
                # 下载并保存图片
                for i, url in enumerate(image_urls):
                    image_path = os.path.join(output_dir, f"image_{i + 1}.jpg")
                    try:
                        response = requests.get(url)
                        response.raise_for_status()
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                        print(f"图片已保存: {image_path}")
                    except requests.exceptions.RequestException as e:
                        print(f"图片下载失败 {url}: {e}")
                result = parse_data(note_data)
                display_title=result[0]['标题'].replace("\n", "").strip()
                text = result[0]['内容'].replace("\n", "").strip()
                likes = convert_to_int(result[0]['点赞数'])
                comments = convert_to_int(result[0]['评论数'])
                collects = convert_to_int(result[0]['收藏数'])
                shares = convert_to_int(result[0]['转发数'])
                topics = ", ".join(result[0]['话题']).replace("\n", "").strip()
                data_row = {
                    'note_url':note_url,
                    'last_update_time':last_update_time,
                    'note_id': note_id,
                    'xsec_token': xsec_token,
                    'type': note_type,
                    "title": display_title,
                    "desc": text,
                    "tag_list": topics,
                    "likes": likes,
                    "comments": comments,
                    "collects": collects,
                    "shares": shares
                }
                df = pd.DataFrame([data_row])
                df.to_csv(output_file_path, mode="a", index=False, header=False, encoding="utf-8-sig", quoting=1)
            except:
                pass
    else:
        print('请求过于频繁，请稍后再试')