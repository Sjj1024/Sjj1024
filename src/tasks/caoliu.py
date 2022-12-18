import json
import time
import requests
from bs4 import BeautifulSoup


class AutoCommit:
    def __init__(self, name, cookie):
        self.source_url = self.get_source_url()
        self.name = name
        self.post_url = self.source_url + "/post.php?"
        self.grader = ""
        self.commit_dist_num = 9
        self.cl_cookie = cookie
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"

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
        url = "https://get.xunfs.com/app/listapp.php"
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"a": "get18", "system": "ios"}
        res = requests.post(url=url, headers=header, data=data)
        res_json = json.loads(res.content.decode("utf-8"))
        # 打印出地址信息和更新时间
        home_url = [res_json["url1"], res_json["url2"], res_json["url3"], res_json["update"]]
        for i in home_url:
            url = "https://" + i
            print(url)
            try:
                res = requests.get(url, timeout=5)
                if res.status_code == 200:
                    print(f"获取到的地址是:{url}")
                return url
            except:
                continue

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
        gread_span = soup.select(".tr3 td:first-child .s3")  # 如果没有找到，返回None
        self.user_name = soup.select('div[colspan="2"] span')[0].get_text()
        self.grader = gread_span[0].get_text()
        print(f"您的用户名是：{self.user_name}, 您的等级是：{self.grader}")
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
            return False

    # 执行主程序
    def run(self):
        print("评论程序开始运行")
        self.source_url = self.get_source_url()
        self.posted_article = self.get_commiteds()
        self.posted_article.update(self.get_posted_tids())
        jishu_article = self.get_titles()
        filtered_link = self.filters_titles(self.posted_article, jishu_article)
        for tid, title in filtered_link.items():
            self.grader = self.get_grade()
            if self.grader == "新手上路":
                commit = "1024"  # 回复帖子的内容
            else:
                commit = "感谢分享"  # 回复帖子的内容
            print("评论的内容是：" + commit)
            try:
                if self.send_commit(tid, title, commit):
                    return
            except Exception as e:
                print(e)
                    
    
def one_commit():
    commiter = AutoCommit("将赏日落", "PHPSESSID=jaqqomtqe1phjbnrprhp6u3mgk; 227c9_ck_info=/	; 227c9_winduser=VAsAV1dVMFRQVwIIVAJWVAUHVVkFBAFWWFEAVwcMAlUFVwoDBF0AaA==; 227c9_groupid=8; 227c9_lastvisit=0	1671354323	/index.php?")
    commiter.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    commiter.run()


if __name__ == '__main__':
    one_commit()
    