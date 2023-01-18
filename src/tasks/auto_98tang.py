import random
import re
import smtplib
import sys
from email.mime.text import MIMEText
from urllib import parse
import requests


class TangTang(object):
    def __init__(self):
        self.name = ""
        self.cookie = ""
        self.user_name = ""
        self.user_money = ""
        self.ji_fei = ""
        self.user_agent = ""
        self.source_url = ""
        self.user_info = ""

    def get_user_info(self):
        url = f"{self.source_url}/home.php?mod=spacecp&ac=credit&showcredit=1"
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': self.cookie,
            'user-agent': self.user_agent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        self.set_cookies(response)
        # print(response.text)
        self.user_name = re.search(r'访问我的空间">(.*?)</a>', response.text).group(1)
        self.user_group = re.search(r'用户组: (.*?)</a>', response.text).group(1)
        self.user_money = re.search(r'金钱: </em>(.*?)  &nbsp;', response.text).group(1)
        self.ji_fei = re.search(r'积分: </em>(.*?) </li>', response.text).group(1)
        self.user_info = {
            "用户名": self.user_name,
            "用户组": self.user_group,
            "金钱": self.user_money,
            "积分": re.search(r'积分: </em>(.*?) </li>', response.text).group(1),
        }
        print(f"今日用户信息: {self.user_info}")
        return self.user_info

    def set_cookies(self, response):
        cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in self.cookie.split("; ")}
        c = response.cookies.get_dict()
        cookie_dict.update(c)
        self.cookie = "; ".join([f"{key}={val}" for key, val in cookie_dict.items()])
        return self.cookie

    def exec_jisuan(self, sunshu):
        res = eval(sunshu)
        print(f"算术答案: {sunshu} = {res}")
        return res

    def get_iphone_suan_shu(self):
        print("获取get_iphone_suan_shu")
        print(f"获取算术内容")
        url = f"{self.source_url}/plugin.php?id=dd_sign&mod=sign&mobile=2"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': self.cookie,
            'referer': f'{self.source_url}/plugin.php?id=dd_sign:index&mobile=2',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        cookie = self.set_cookies(response)
        suanshu = re.search(r'输入下面问题的答案<br />(.*?) = \?</span>', response.text).group(1)
        res = self.exec_jisuan(suanshu)
        params = {
            "id": "dd_sign",
            "mod": "sign",
            "signsubmit": "yes",
            "signhash": "",
            "handlekey": "signform_",
            "inajax": "1",
            "formhash": re.search(r'formhash" value="(.*?)" />', response.text).group(1),
            "signtoken": re.search(r'name="signtoken" value="(.*?)" />', response.text).group(1),
            "secqaahash": re.search(r'secqaahash" type="hidden" value="(.*?)" />', response.text).group(1),
            "secanswer": res,
            "cookie": cookie
        }
        return params

    def get_web_suan_shu(self):
        id_hash = "qSAUcj0"
        url = f"{self.source_url}/misc.php?mod=secqaa&action=update&idhash={id_hash}&0.4640535681735929"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': self.cookie,
            'referer': f'{self.source_url}/plugin.php?id=dd_sign:index',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        self.set_cookies(response)
        suan_shu = re.search(r"'(.*?) = \?'", response.text).group(1)
        suan_res = self.exec_jisuan(suan_shu)
        return {"id_hash": id_hash, "da_an": suan_res}

    def check_web_suanshu(self, params):
        url = f"{self.source_url}/misc.php?mod=secqaa&action=check&inajax=1&modid=&idhash=qSAEn10&secverify=15"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': self.cookie,
            'referer': f'{self.source_url}/plugin.php?id=dd_sign:index',
            'user-agent': self.user_agent,
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        self.set_cookies(response)
        print(response.text)

    def get_suanshu(self):
        print(f"获取算术内容")
        url = f"{source_url}/plugin.php?id=dd_sign&mod=sign&mobile=2"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': self.cookie,
            'referer': f'{source_url}/plugin.php?id=dd_sign:index&mobile=2',
            'upgrade-insecure-requests': '1',
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        cookie = self.set_cookies(response)
        suanshu = re.search(r'输入下面问题的答案<br />(.*?) = \?</span>', response.text).group(1)
        res = self.exec_jisuan(suanshu)
        params = {
            "id": "dd_sign",
            "mod": "sign",
            "signsubmit": "yes",
            "signhash": "",
            "handlekey": "signform_",
            "inajax": "1",
            "formhash": re.search(r'formhash" value="(.*?)" />', response.text).group(1),
            "signtoken": re.search(r'name="signtoken" value="(.*?)" />', response.text).group(1),
            "secqaahash": re.search(r'secqaahash" type="hidden" value="(.*?)" />', response.text).group(1),
            "secanswer": res,
            "cookie": cookie
        }
        return params

    def start_iphone_sign(self):
        print("开始签到")
        params = self.get_suanshu()
        url = f"{self.source_url}/plugin.php?id=dd_sign&mod=sign&signsubmit=yes&signhash=&handlekey=signform_&inajax=1"
        payload = f"formhash={params.get('formhash')}&signtoken={params.get('signtoken')}&secqaahash={params.get('secqaahash')}&secanswer={params.get('secanswer')}"
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': 'application/xml, text/xml, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': params.get("cookie"),
            'origin': f'{self.source_url}',
            'referer': f'{self.source_url}/plugin.php?id=dd_sign&mod=sign&mobile=2',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if "签到成功" in response.text:
            print("签到成功，金钱+2，明天记得来哦")
            return True
        elif "已经签到过啦，请明天再来" in response.text:
            print("已经签到过啦，请明天再来！")
            return True
        else:
            print(f"签到失败：{response.text}")
            return False

    def has_signed(self):
        print("判断是否已经签到了...")
        url = f"{self.source_url}/plugin.php?id=dd_sign:index"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': self.cookie,
            'referer': f'{self.source_url}/forum.php',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        if "今日未签到，点击签到" in response.text:
            # print(f"{self.user_name} : 今日已签到")
            return "今日未签到，点击签到"
        elif "您尚未登录" in response.text:
            print("您尚未登录")
            return response.text
        elif "今日已签到" in response.text:
            # print("今日已签到")
            return "今日已签到"
        else:
            print(f"没有检测到已签到：{response.text}")
            return "没有签到"

    def start_web_sign(self):
        print(f"开始web端签到...")
        params = self.get_web_suan_shu()
        id_hash = params.get("id_hash")
        da_an = params.get("da_an")
        url = f"{self.source_url}/misc.php?mod=secqaa&action=check&inajax=1&modid=&idhash={id_hash}&secverify={da_an}"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': self.cookie,
            'referer': f'{self.source_url}/plugin.php?id=dd_sign:index',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        if "succeed" in response.text:
            print(f"签到成功")
        else:
            print(f"签到异常:{response.text}")

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

    def get_html(self, page_url):
        print(f"开始获取html: {page_url}")
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': self.cookie,
            'user-agent': self.user_agent
        }
        res = requests.request("GET", page_url, headers=headers, data=payload)
        try:
            html = res.content.decode()
            if "登录" in html:
                print(html)
                self.send_email(f"{self.user_name}评论异常", html)
                raise Exception("cookie无效...")
            self.set_cookies(res)
            return html
        except Exception as e:
            print(res.text)
            print(f"获取html出错：{e},开始重试新的请求。。。。。。。")
            raise Exception("cookie无效")

    def get_articales(self):
        # 获取前十页内容
        article_list = []
        for i in range(2, 10):
            print(f"获取第{i}页文章列表......")
            page_url = f"{self.source_url}/forum.php?mod=forumdisplay&fid=95&page={i}"
            html = self.get_html(page_url)
            id_list = re.findall(r'tid=.*?class="s xst"', html)
            tid_list = [i[4:10] for i in id_list]
            article_list += tid_list
        print(f"得到总的文章链接是:{len(article_list)}")
        return article_list

    def get_commenteds(self):
        print("获取评论过的文章:")
        id_list = []
        page = 1
        while True:
            url = f"{self.source_url}/forum.php?mod=guide&view=my&type=reply&page={page}"
            html = self.get_html(url)
            comment_list = re.findall(r'tid=.*?class="xst"', html)
            # print(comment_list)
            # print(len(comment_list))
            ids = [i[4:10] for i in comment_list]
            if "下一页" in html and page <= 5:
                page += 1
                id_list += ids
            else:
                print(f"评论过的文章有{page}页，总共有{len(id_list)}篇文章被评论过")
                return id_list

    def get_comment_txt(self, count):
        print(f"获取评论内容:{count}")
        txt_list = ["看起来挺骚的", "溜了，评分留下", "典型的大妈脸", "都是猛人", "被吓到了", "还是支持一下",
                    "最近啥情况", "怎么看不了", "感谢大佬", "有磁力的吗", "最近这种有点多啊", "我看到过的",
                    "这也太牛逼了",
                    "感谢大佬的精彩分享", "都是神人", "艺高人胆大", "就是喜欢这样的题材", "这个不太好吧",
                    "也开始拍剧情了",
                    "看着真实", "不知道真的假的", "这么会玩的吗", "这可太刺激了", "看看这次是什么情况", "看着眼熟",
                    "好资源，评分送上", "有够刺激的", "这玩意儿看看就好", "多更新这种题材的", "满足一下幻想",
                    "不会是假的吧",
                    "不好意思发了", "怎么全是链接错误", "但还是很喜欢", "刺激就行啊", "看不到了", "这些资源",
                    "真不错真不错",
                    "笑死我了哈哈哈", "高手在民间", "多谢老哥分享", "看起来挺不错", "先赞后看", "的确是好内容",
                    "真人想多了",
                    "因为我本纯良", "这个主题不错"]
        return txt_list[random.randint(0, len(txt_list) - 1)]

    def get_formhash(self, tid):
        print("获取hash值")
        url = f"{self.source_url}/forum.php?mod=viewthread&tid={tid}&extra=page%3D1"
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': self.cookie,
            'user-agent': self.user_agent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        form_hash = re.search(r'formhash=(.*?)">退出</a>', response.text).group(1)
        return form_hash

    def post_commit(self, tid, txt, form_hash):
        print(f"开始回复评论：{tid} : {txt} hash:{form_hash}")
        url = f"{self.source_url}/forum.php?mod=post&action=reply&fid=95&tid={tid}&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
        body = {
            "file": "",
            "message": txt,
            "posttime": "1672656117",
            "formhash": form_hash,
            "usesig": "",
            "subject": ""
        }
        payload = parse.urlencode(body)
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': self.cookie,
            'user-agent': self.user_agent
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        self.set_cookies(response)
        html = response.text
        if "回复发布成功" in html:
            print("回复发布成功, 评论完成了....")
            return True
        else:
            print(response.text)
            print("评论失败了")
            return False

    def start_commit_one(self):
        # 获取评论过的文章
        id_list = self.get_commenteds()
        # 获取前10页的文章链接
        article_list = self.get_articales()
        # 过滤没有评论过的文章链接
        need_post = [i for i in article_list if i not in id_list]
        # 发起评论
        for index, value in enumerate(need_post):
            commit_txt = self.get_comment_txt(index)
            form_hash = self.get_formhash(value)
            res = self.post_commit(value, commit_txt, form_hash)
            if res:
                break
            else:
                continue


def run():
    tang = TangTang()
    tang.source_url = source_url
    tang.user_name = name
    tang.cookie = cookie
    tang.user_agent = user_agent
    tang.get_user_info()
    tang.start_commit_one()
    qiandao = tang.has_signed()
    if qiandao == "今日未签到，点击签到":
        # tang.start_web_sign()
        tang.start_iphone_sign()
    elif "今日已签到" in qiandao:
        print(qiandao)
    else:
        print(f"签到异常: {qiandao}")


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        name = "LCJ1275"
        cookie = "cPNj_2132_saltkey=pRGuETKZ; cPNj_2132_lastvisit=1673947874; cPNj_2132_lastfp=ff63697e01d406ee4e4f20a439084855; cPNj_2132_ulastactivity=1673951520%7C0; cPNj_2132_auth=d9f28KJ95Omo%2BEJQ38UJPM%2BAmd2mMmABXyKdsu10mfEjnuPqnknFCgadBlDel4wvNbbjeQT5QNLGvDxWpGXtoUeRmLU; cPNj_2132_lastcheckfeed=422246%7C1673951520; cPNj_2132_sid=0; cPNj_2132_nofavfid=1; cPNj_2132_sendmail=1; PHPSESSID=qk7vnd0dr5ldpf1439srof848r; cPNj_2132_lastact=1673951855%09index.php%09"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    else:
        name = sys.argv[1]
        cookie = sys.argv[2]
        user_agent = sys.argv[3]
    source_url = "https://zxfdsfdsf.online"
    run()
