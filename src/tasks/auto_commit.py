import datetime
import json
import random
import re
import time
import sys
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText


class AutoCommit:
    def __init__(self, name, cookie):
        self.cant_title = []
        self.cant_tid = []
        self.posted_article = None
        self.source_url = ""
        self.user_name = name
        self.post_url = self.source_url + "/post.php?"
        self.get_source_url()
        self.grader = ""
        self.commit_dist_num = 9
        self.cl_cookie = cookie
        self.user_agent = ""

    def get_soup(self, page_url):
        # 获取单张我的评论页面中的所有评论过的文章id和标题
        time.sleep(1)
        header = {
            "user-agent": self.user_agent,
            "cookie": self.cl_cookie,
            "referer": self.source_url + "/index.php"
        }
        try:
            res = requests.get(page_url, headers=header, timeout=10)
            html = res.content.decode()
        except Exception as e:
            print(f"有错误{e},开始重试新的请求......")
            source_url = self.get_source_url()
            new_url = page_url.replace(self.source_url, source_url)
            res = requests.get(new_url, headers=header, timeout=10)
            html = res.content.decode()
            self.source_url = source_url
        soup = BeautifulSoup(html, "lxml")
        return soup

    def get_source_url(self):
        if self.source_url:
            return self.source_url
        url = "https://get.xunfs.com/app/listapp.php"
        data = {"a": "get18", "system": "ios"}
        res = requests.post(url=url, data=data)
        res_json = json.loads(res.content.decode("utf-8"))
        # 打印出地址信息和更新时间
        home_url = [res_json["url1"], res_json["url2"], res_json["url3"], res_json["update"]]
        for i in home_url:
            url = "https://" + i
            try:
                res = requests.get(url, timeout=10)
                if res.status_code == 200:
                    print(f"获取到的地址是:{url}")
                self.source_url = url
                return url
            except:
                continue

    def get_userinfo(self):
        print("get_userinfo_bycookie-----")
        # 获取下一页的链接, 有就返回，没有就返回false
        source_url = self.get_source_url()
        url = source_url + "/profile.php"
        soup = self.get_soup(url)
        if soup:
            gread_span = soup.select("#main > div.t > table > tr > td:nth-child(3) > a")  # 如果没有找到，返回None
            email_span = soup.select("#main > div.t > table > tr > td:nth-child(2) > a")  # 如果没有找到，返回None
            info_url = f"{source_url}/{gread_span[0].get('href')}"
            email_url = f"{source_url}/{email_span[0].get('href')}"
            print(f"您的用户名是：, 您的等级是：{info_url}")
            info_soup = self.get_soup(info_url)
            email_soup = self.get_soup(email_url)
            if info_soup and email_soup:
                email = re.search(r"E-MAIL\n(.*?)com",
                                  email_soup.select("#main > form")[0].get_text()).group(1) + "com"
                all_info = info_soup.select("#main > div:nth-child(3)")[0].select("table")[0].get_text()
                user_name = re.search(r'用戶名(.*?) \(', all_info).group(1)
                user_id = re.search(r'\(數字ID:(.*?)\)', all_info).group(1)
                dengji = re.search(r'會員頭銜(.*?)\n', all_info).group(1)
                jifen = re.search(r'綜合積分(.*?)\n', all_info).group(1)
                fatie = re.search(r'發帖(.*?)\n', all_info).group(1)
                weiwang = re.search(r'威望(.*?) 點\n', all_info).group(1)
                money = re.search(r'金錢(.*?) USD\n', all_info).group(1)
                gongxian = re.search(r'貢獻(.*?) 點\n', all_info).group(1)
                gongxian_link = re.search(r'隨機生成\)(.*?)\n', all_info).group(1)
                regist_time = re.search(r'註冊時間(.*?)\n', all_info).group(1)
                self.userinfo = {
                    "user_name": user_name,
                    "user_id": user_id,
                    "dengji": dengji,
                    "jifen": jifen,
                    "fatie": fatie,
                    "weiwang": weiwang,
                    "money": money,
                    "gongxian": gongxian,
                    "gongxian_link": gongxian_link,
                    "regist_time": regist_time,
                    "email": email
                }
                return self.userinfo
            else:
                return {}
        else:
            return {}

    # 获取已评论文章列表
    def get_commiteds(self):
        print("获取已评论文章")
        article_dict = {}
        # 获取下一页的链接, 有就返回，没有就返回false
        url = self.source_url + "/personal.php?action=post"
        soup = self.get_soup(url)
        last_num = soup.find(id="last")  # 如果没有找到，返回None
        if last_num:
            print("说明有不止一页评论内容")
            last_num = soup.find(id="last").get("href")
            all_page = last_num.split("page=")[1]
            all_num = int(all_page) + 1
            # 如果评论过的文章大与2页，就按两页算
            if all_num > 2:
                all_num = 2
            for i in range(1, all_num):
                page_url = self.source_url + f"/personal.php?action=post&page={i}"
                print(f"正在抽取第{i}页中的评论数据")
                soup = self.get_soup(page_url)
                # 通过soup获得已经评论过的文章id和标题
                article_list = soup.select(".a2")
                article_title = [i.get_text() for i in article_list]
                article_id = [i.get("href") for i in article_list]
                tid_list = [i.split("tid=")[1].split("&")[0] for i in article_id]
                article_dict.update(dict(zip(tid_list, article_title)))
        else:
            print("说明只有一页评论内容")
            article_list = soup.select(".a2")
            article_title = [i.get_text() for i in article_list]
            article_id = [i.get("href") for i in article_list]
            tid_list = [i.split("tid=")[1].split("&")[0] for i in article_id]
            article_dict.update(dict(zip(tid_list, article_title)))
        print(f"获取到评论过的文章个数是：{len(article_dict)}----------------->")
        return article_dict

    # 获取发布的文章
    def get_posted_tids(self):
        print("获取发布的文章")
        article_dict = {}
        # 获取下一页的链接, 有就返回，没有就返回false
        url = self.source_url + "/personal.php"
        soup = self.get_soup(url)
        last_num = soup.find(id="last")  # 如果没有找到，返回None
        if last_num:
            print("说明有不止一页评论内容")
            last_num = soup.find(id="last").get("href")
            all_page = last_num.split("page=")[1]
            all_num = int(all_page) + 1
            # 如果评论过的文章大与2页，就按两页算
            if all_num > 2:
                all_num = 2
            for i in range(1, all_num):
                page_url = self.source_url + f"/personal.php?action=post&page={i}"
                print(f"正在抽取第{i}页中的评论数据")
                soup = self.get_soup(page_url)
                # 通过soup获得已经评论过的文章id和标题
                article_list = soup.select(".a2")
                article_title = [i.get_text() for i in article_list]
                article_id = [i.get("href") for i in article_list]
                tid_list = [i.split("tid=")[1].split("&")[0] for i in article_id]
                article_dict.update(dict(zip(tid_list, article_title)))
        else:
            print("说明只有一页评论内容")
            article_list = soup.select(".a2")
            article_title = [i.get_text() for i in article_list]
            article_id = [i.get("href") for i in article_list]
            tid_list = [i.split("tid=")[1].split("&")[0] for i in article_id]
            article_dict.update(dict(zip(tid_list, article_title)))
        print(f"获取已发布的文章个数是：{len(article_dict)}----------------->")
        return article_dict

    # 获取账号等级
    def get_grade(self):
        print("获取用户名和账号等级")
        # 获取下一页的链接, 有就返回，没有就返回false
        url = self.source_url + "/index.php"
        soup = self.get_soup(url)
        if "請輸入用戶名" in soup.decode():
            print(f"没有获取到用户名等信息:{soup.decode()}")
            self.send_email(f"{self.user_name} :评论异常,Cookie失效", soup.decode())
        gread_span = soup.select("body")[0].get_text()  # 如果没有找到，返回None
        self.user_name = re.search(r'\t(.*?) 退出', gread_span).group(1)
        self.grader = re.search(r'您的等級: (.*?) ', gread_span).group(1)
        self.weiwang = re.search(r'威望: (.*?) 點', gread_span).group(1)
        self.jinqian = re.search(r'金錢: (.*?) USD', gread_span).group(1)
        self.gongxian = re.search(r'貢獻: (.*?) 點', gread_span).group(1)
        print(f"您的用户名：{self.user_name}, 等级：{self.grader}, 威望：{self.weiwang}，貢獻：{self.gongxian}")
        if int(self.weiwang) >= 100:
            print("开始产邀请码了")
        return self.grader

    # 获取技术交流版块前两页文章列表
    def get_titles(self):
        print("获取技术交流区前三页的文章链接，并提取tid和标题")
        jishu_article_dict = {}
        for i in range(1, 3):
            # 获取下一页的链接, 有就返回，没有就返回false
            url = self.source_url + f"/thread0806.php?fid=7&search=&page={i}"
            print(f"开始获取{url}页文章链接")
            soup = self.get_soup(url)
            time.sleep(5)
            titles = soup.select("h3 a")
            titles_href = [x.get("href") for x in titles]
            titles_text = [x.get_text() for x in titles]
            # 提取出文章的tid
            if i == 1:  # 如果获取到的是第一页的链接，则剔除前8个链接，因为那是社区公告
                titles_href = [x.get("href") for x in titles][9:]
                titles_text = [x.get_text() for x in titles][9:]
            tid_list = []
            for x in titles_href:
                if "html" in x:
                    tid_list.append(x.split("/")[-1].split(".")[0])
                elif "tid" in x:
                    tid_list.append(x.split("=")[1])
            # 判断如果获取到的tidlist长度和titles_text长度一样，就压缩成字典，保存到列表中
            if len(tid_list) == len(titles_text):
                jishu_article_dict.update(dict(zip(tid_list, titles_text)))
            else:
                print("获取到的文章列表长度不一致")
                return
        # 所有页面文章链接获取到之后，将链接打印出来
        print(f"获取到技术区文章个数是：{len(jishu_article_dict)}----------------->")
        return jishu_article_dict

    # 筛选出没有评论过的文章链接
    def filters_titles(self, posted_article, jishu_article):
        print("筛选出没有评论过的文章链接")
        posted_article_keys = set(posted_article.keys())
        jishu_article_keys = set(jishu_article.keys())
        commited_tid = posted_article_keys & jishu_article_keys
        filtered_tid = jishu_article_keys.difference(posted_article_keys)
        filtered_article_link = {}
        for i in filtered_tid:
            filtered_article_link[i] = jishu_article[i]
        print(f"过滤中发现已经评论过的文章个数是：{len(commited_tid)}----------------->")
        print(f"获取到过滤后没有评论过的文章个数是：{len(filtered_article_link)}----------------->")
        return filtered_article_link

    # 开始发起评论
    def send_commit(self, tid, title, commit):
        # 遍历没有评论过的文章链接
        print("遍历没有评论过的文章链接")
        post_url = self.source_url + "/post.php?"
        gbk_title = f"Re:{title}".encode()
        gbk_commit = commit.encode()
        commit_data = {
            "atc_money": 0,
            "atc_rvrc": 0,
            "atc_usesign": 1,
            "atc_convert": 1,
            "atc_autourl": 1,
            "atc_title": gbk_title,
            "atc_content": gbk_commit,
            "step": 2,
            "action": "reply",
            "fid": 7,
            "tid": tid,
            "atc_attachment": "none",
            "pid": None,
            "article": None,
            "verify": "verify", }
        zuiai_header = {
            "user-agent": self.user_agent,
            "cookie": self.cl_cookie,
            "content-type": "application/x-www-form-urlencoded"
        }
        rel_url = post_url
        response = requests.post(rel_url, headers=zuiai_header, data=commit_data, timeout=10)
        res_html = response.content.decode()
        success = "發貼完畢點擊進入主題列表"
        guashui = "灌水預防機制已經打開，在1024秒內不能發貼"
        every_10 = "用戶組權限：你所屬的用戶組每日最多能發 10 篇帖子"
        if success in res_html or guashui in res_html or every_10 in res_html:
            print(f"回复帖子{tid}:{title}成功------------->")
            self.posted_article.update({tid: title})
            return True
        else:
            print(f"回复帖子{tid}:{title}失败------------->{res_html}")
            if "被管理員禁言" in res_html:
                return res_html
            return False

    def send_email(self, title, msg, email="648133599@qq.com"):
        content = str(msg)
        # 163邮箱服务器地址
        mail_host = "smtp.163.com"
        # 163用户名
        mail_user = "lanxingsjj@163.com"
        # 密码(部分邮箱为授权码)
        mail_pass = "QULRMYHTUVMHYVGM"
        # 邮件发送方邮箱地址
        sender = "lanxingsjj@163.com"
        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = [email]
        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = title
        # 发送方信息
        message['From'] = sender
        # 接受方信息
        message['To'] = receivers[0]
        # 登录并发送邮件
        try:
            # 在阿里云上就要改为下面这种，本地和服务器都友好：
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            # 登录到服务器
            smtpObj.login(mail_user, mail_pass)
            # 发送
            smtpObj.sendmail(sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            print('send email success')
        except smtplib.SMTPException as e:
            print('send email error', e)  # 打印错误

    # 执行主程序
    def run(self):
        print("评论程序开始运行")
        self.grader = self.get_grade()
        self.posted_article = self.get_commiteds()
        self.posted_article.update(self.get_posted_tids())
        jishu_article = self.get_titles()
        filtered_link = self.filters_titles(self.posted_article, jishu_article)
        for tid, title in filtered_link.items():
            # 过滤掉禁止无关回复的文章
            if tid in self.cant_tid or any([True for t in self.cant_title if t in title]):
                print(f"遇到了不可以回复的文章{title} : {tid}")
                continue
            if self.grader == "新手上路":
                commit = "1024"  # 回复帖子的内容
            else:
                commit_list = ["我支持你", "了解一下", "发帖辛苦", "我喜欢这个", "点赞支持", "感谢分享", "你很棒",
                               "我很喜欢", "感谢你的发帖", "还有更骚的", "你很厉害", "这个也不错", "有点意思", "不知道真假",
                               "我想试试", "有没有看过的", "不错不错"]
                commit = random.choice(commit_list)
            print("评论的内容是：" + commit)
            try:
                res = self.send_commit(tid, title, commit)
                if res is True:
                    return
                else:
                    self.send_email(f"{self.user_name}评论异常", res)
                    return
            except Exception as e:
                print(e)
                self.send_email(f"{self.user_name}评论异常", e)


def get_my_ip():
    res = requests.get('http://myip.ipip.net', timeout=5).text
    print(res)


def one_commit():
    get_my_ip()
    print("当前时间是", datetime.datetime.now())
    print("正在运行的脚本名称: '{}'".format(sys.argv[0]))
    print("脚本的参数数量: '{}'".format(len(sys.argv)))
    print("脚本的参数: '{}'".format(str(sys.argv)))
    if len(sys.argv) <= 1:
        user_name = "两杯可乐"
        # cookie = "PHPSESSID=rfbtkc0f0v6s8chku4hflmcv7h;227c9_ck_info=%2F%09;227c9_winduser=UAAJDgwAaAsOXwdVVAJUDFRaBQRYVg0CAlZdC1FRAQ4CDwcMUgNYPg%3D%3D;227c9_groupid=8;227c9_lastvisit=0%091673614803%09%2Fprofile.php%3F"
        cookie = '227c9_ck_info=%2F%09;227c9_groupid=8;227c9_lastvisit=0%091673615325%09%2Flogin.php%3F;227c9_winduser=VAgBWFZRMAZUAAMOBQMABQsFWlwCUlcBDlMMDVAIUQFVBAADVQtQaA%3D%3D;PHPSESSID=hh5nrgiqa9so9ov3k9e79k3fc1;'
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    else:
        user_name = sys.argv[1]
        cookie = sys.argv[2]
        user_agent = sys.argv[3]
    commiter = AutoCommit(user_name, cookie)
    # 配置不可以回复的文章
    commiter.cant_tid = ['5448754', "5448978", "5424564"]
    commiter.cant_title = ["禁止无关回复", "乱入直接禁言"]
    commiter.user_agent = user_agent
    commiter.run()


if __name__ == '__main__':
    one_commit()
