# simple_crawler.py
from DrissionPage import ChromiumPage
import time
import os
from DrissionPage.common import Actions

from DrissionPage import Chromium

# 连接浏览器并获取一个MixTab对象
tab = Chromium().latest_tab
# 访问网址
# tab.get('https://www.xiaohongshu.com/explore')
# 切换到收发数据包模式
# tab.change_mode()



# ele1 = tab.ele('#search-input')
# 向文本框元素对象输入文本
# ele1.input('猫\n')


eles = tab.eles("tag:span@@class=note-text")
# 停用词过滤
keywords = ['@', '哈哈哈', '笑死我了']
filtered_eles = [ele for ele in eles if not any(keyword in ele.text for keyword in keywords)]
# 遍历获取到的元素
for item in filtered_eles:
    # 打印元素文本
    print(item.text)



# 获取所有行元素
# items = tab.ele('.ui relaxed divided items explore-repo__list').eles('.item')
# 遍历获取到的元素
# for item in items:
    # 打印元素文本
    # print(item('t:h3').text)
    # print(item('.project-desc mb-1').text)
    # print()
