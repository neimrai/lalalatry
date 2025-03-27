import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox
from DrissionPage import ChromiumPage
import pickle
import time
from DrissionPage.common import Actions
 
 
class App:
    def __init__(self):
        # 创建用户数据目录
        """
        文件夹结构
        data->  goods_name_1 -> links -> link1.txt
                                      -> link2.txt
                             -> notebooks -> notebook1.txt
                                          -> notebook2.txt
            ->  goods_name_2
            ->  cookies -> name_1.pkl
                        -> name_2.pkl
        """
        home_directory = os.path.expanduser("~")
        data_folder = os.path.join(home_directory, "data")
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        self.data_folder = data_folder
        self.cookies_folder = os.path.join(self.data_folder, "cookies")
        if not os.path.exists(self.cookies_folder):
            os.makedirs(self.cookies_folder)
        # 小红书的平台url
        self.platform_url = "https://www.xiaohongshu.com"
        # 窗口设置
        self.root = tk.Tk()
        self.root.geometry('300x200')
        self.root.title("小红书爬虫工具")
        self.root.resizable(False, False)
        # 设置菜单
        self.menubar = tk.Menu(self.root)
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label="添加账户cookies", command=self.add_cookies)
        self.edit_menu.add_command(label="删除账户cookies", command=self.delete_cookies)
        self.menubar.add_cascade(label="编辑", menu=self.edit_menu)
        self.menubar.add_cascade(label="操作说明", command=self.options)
        self.root.config(menu=self.menubar)
        # 设置爬虫页面
        self.good_name_label = tk.Label(self.root, text="下面输入搜索内容:")
        self.good_name_label.pack()
        self.good_name_entry = tk.Entry(self.root)
        self.good_name_entry.pack()
        self.accounts_label = tk.Label(self.root, text="选择账户:")
        self.accounts_label.pack()
        self.accounts_combobox = ttk.Combobox(self.root)
        self.accounts_combobox.pack()
        all_accounts = os.listdir(self.cookies_folder)
        self.accounts_combobox["values"] = all_accounts
        self.button = tk.Button(self.root, text="开始爬虫", command=self.start_crawling)
        self.button.pack()
        self.root.mainloop()
 
    def add_cookies(self):
        def confirm():
            messagebox.showinfo(
                message="请先打开小红书准备扫码, 扫码时间只有60秒，请在规定时间内完成，否则后续可能会出现账号没有登录的问题！")
            page = ChromiumPage()
            page.get(self.platform_url)
            # 等待手动身份验证
            time.sleep(60)
            cookies = page.cookies()
            file_path = os.path.join(self.cookies_folder, f"{name_entry.get()}.pkl")
            with open(file_path, "wb") as cookies_file:
                pickle.dump(cookies, cookies_file)  # 保存 cookies
            messagebox.showinfo(message="保存成功！")
            page.quit()
 
        window = tk.Toplevel(self.root)
        window.geometry('300x200')
        name_label = tk.Label(window, text="您的姓名是:")
        name_label.pack()
        name_entry = tk.Entry(window)
        name_entry.pack()
        button = tk.Button(window, text="确定", command=confirm)
        button.pack()
 
    def delete_cookies(self):
        def delete():
            selected_value = combobox.get()
            os.remove(os.path.join(self.cookies_folder, selected_value))
            messagebox.showinfo(message=f"{selected_value}已经被删除!")
 
        window = tk.Toplevel(self.root)
        window.geometry('300x200')
        label = tk.Label(window, text="在下方选择需要删除的cookies")
        label.pack()
        combobox = ttk.Combobox(window)
        combobox.pack()
        data = os.listdir(self.cookies_folder)
        combobox["values"] = data
        button = tk.Button(window, text="删除", command=delete)
        button.pack()
 
    def options(self):
        window = tk.Toplevel(self.root)
        window.geometry("400x200")
        window.resizable(False, False)
        title = "运行步骤:"
        label = tk.Label(window, text=title)
        label.pack()
        first = tk.Label(window, text="1.先点击编辑菜单栏上的添加cookies按钮,运行之后得到相应的cookies.")
        first.pack()
        second = tk.Label(window, text="2.然后在输入框中输入搜索内容，并选择相应的cookies开始爬虫程序.")
        second.pack()
        final = tk.Label(window, text="3.最后等待程序运行完即可在用户主目录下的data文件夹中看到相应的文件.")
        final.pack()
        note = tk.Label(window, text="注:若遇到反爬的措施，可以更换账号进行下一次操作!")
        note.pack()
 
    def start_crawling(self):
        def remove_character(string):
            result = ""
            for _ in string:
                if _.isdigit():
                    result = result + _
            return result
 
        messagebox.showinfo(
            message="代码运行时间较长，为确保能将所有笔记爬取完成，请务必保持屏幕常亮(或者保持人在电脑前),感谢您的使用!")
        if not self.good_name_entry.get():
            messagebox.showerror(message="搜索内容不能为空！")
        goods_name = self.good_name_entry.get()
        if not os.path.exists(os.path.join(self.data_folder, goods_name)):
            os.makedirs(os.path.join(self.data_folder, goods_name))
        goods_folder = os.path.join(self.data_folder, goods_name)
        selected_value = self.accounts_combobox.get()
        page = ChromiumPage()
        ac = Actions(page)
        path = os.path.join(self.cookies_folder, selected_value)
        # 加载cookies
        with open(path, "rb") as cookies_file:
            cookies = pickle.load(cookies_file)
        for cookie in cookies:
            page.set.cookies(cookie)
        page.get(self.platform_url)
        page.set.window.max()
        time.sleep(2)
        page.ele("xpath:/html/body/div[2]/div[1]/div[1]/header/div[2]/input").input(goods_name)
        ac.key_down("ENTER")
        ac.key_up("ENTER")
        time.sleep(2)
        all_ = page.ele("@id=note")
        page.actions.click(all_)
        all_links = set()
        while True:
            last_num = len(all_links)
            for _ in page.eles("@class=cover ld mask"):
                all_links.add(_.attr("href"))
            now_num = len(all_links)
            page.actions.scroll(800)
            time.sleep(0.5)
            print(f"链接数量为{len(all_links)}，正在增加，向下滚动800单位！")
            if now_num == last_num:
                break
        all_links = list(all_links)
        links_path = os.path.join(goods_folder, "links.txt")
        with open(links_path, "w", encoding="utf-8") as f:
            for i in range(len(all_links)):
                f.write(all_links[i] + "\n")
                print(f"成功将第{i + 1}个链接写入文件！")
        page.quit()
        if not os.path.exists(os.path.join(goods_folder, "notebooks")):
            os.makedirs(os.path.join(goods_folder, "notebooks"))
        notebooks_folder = os.path.join(goods_folder, "notebooks")
        # 打开文件中的链接逐个提取笔记
        with open(links_path, "r", encoding="utf-8") as f:
            all_links = [_.rstrip() for _ in f.readlines()]
        i = 1
        for link in all_links:
            page = ChromiumPage()
            print(f"开始爬取第{i}篇笔记！")
            # 加载 cookies
            with open(path, "rb") as cookies_file:
                cookies = pickle.load(cookies_file)
            for cookie in cookies:
                page.set.cookies(cookie)
            page.get(link)
            try:
                title = page.ele("@id=detail-title").attr("text")
            except:
                title = ""
            print(f"标题是{title}")
            try:
                ID = page.ele("@class=username").attr("text")
                print(f"ID为{ID}")
            except:
                ID = ""
            try:
                content = page.ele("@class=note-text").attr("text")
                print(f"标题为{title},ID为{ID}的内容已提取。")
            except:
                content = ""
            try:
                date = page.ele("@class=date").attr("text")
                print(f"发布时间是{date}。")
            except:
                date = ""
            try:
                likes = page.ele(
                    "xpath:/html/body/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[3]/div/div/div[1]/div["
                    "2]/div/div[1]/span[1]/span[2]").attr("text")
                print(f"点赞数目为", likes)
            except:
                likes = ""
            try:
                collect = page.ele("@class=collect-wrapper").attr("text")
                print(f"收藏数量是{collect}")
            except:
                collect = ""
            try:
                chat = page.ele("@class=chat-wrapper").attr("text")
                print(f"评论数量是{chat}")
            except:
                chat = ""
            with open(os.path.join(notebooks_folder, f"notebook{i}.txt"), "w", encoding="utf-8") as f1:
                f1.write(f"作者ID:{ID}\n")
                f1.write(f"标题:{title}\n")
                f1.write(f"内容:{content}\n")
                f1.write(f"发布时间:{date}\n")
                f1.write(f"点赞数目:{remove_character(likes)}\n")
                f1.write(f"收藏数量:{remove_character(collect)}\n")
                f1.write(f"评论数量:{remove_character(chat)}\n")
            print(f"第{i}篇笔记已爬取完成!")
            page.quit()
            time.sleep(10)
            i += 1
        messagebox.showinfo(message="全部笔记已爬取完成！")
 
 
if __name__ == '__main__':
    App()