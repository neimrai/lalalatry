import pickle
import time
from DrissionPage import ChromiumPage


page = ChromiumPage()
page.get("https://www.xiaohongshu.com")
# 留出120秒时间手动登录，如果操作速度快时间可以减少一点
# time.sleep(120)
cookies = page.cookies()
with open("cookies.pkl", "wb") as cookies_file:
    pickle.dump(cookies, cookies_file)  # 保存 cookies
    
