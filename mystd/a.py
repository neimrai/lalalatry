from DrissionPage import Chromium
from DrissionPage.common import Settings
from DrissionPage import SessionPage

from DrissionPage import SessionPage

page = SessionPage()
page.get('https://www.xiaohongshu.com/explore/67dd4d37000000000900f495')
# page.get('http://www.baidu.com')
# page.get('http://gitee.com')
# 获取页面标题
print(page.title)
# 获取页面html
print(page.url)
print(page.url_available)
print(page.session)

for i in page.cookies(all_domains=True):
    print(i)