import sys
import re
import time
from urllib import parse
import requests
import random


def set_cookies(res):
    global cookie
    cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
    c = res.cookies.get_dict()
    cookie_dict.update(c)
    cookie = "; ".join([f"{key}={val}" for key, val in cookie_dict.items()])


def get_html(page_url):
    # print("开始获取html")
    global cookie
    payload = {}
    headers = {
        'cookie': cookie,
        'user-agent': user_agent
    }
    res = requests.request("GET", page_url, headers=headers, data=payload)
    try:
        html = res.content.decode()
        set_cookies(res)
        return html
    except Exception as e:
        print(res.text)
        print(f"获取html出错：{e},开始重试新的请求。。。。。。。")
        raise Exception("获取html出错")


def get_commenteds():
    print("获取评论过的文章:")
    id_list = []
    page = 1
    while True:
        url = f"{source_url}/forum.php?mod=guide&view=my&type=reply&page={page}"
        html = get_html(url)
        comment_list = re.findall(r'tid=.*?class="xst"', html)
        print(comment_list)
        print(len(comment_list))
        ids = [i[4:10] for i in comment_list]
        if "下一页" in html and page <= 5:
            page += 1
            id_list += ids
        else:
            print(f"评论过的文章有{page}页，总共有{len(id_list)}篇文章被评论过")
            return id_list


def get_articales():
    article_list = []
    for i in range(2, 10):
        print(f"获取第{i}页文章列表......")
        page_url = f"{source_url}/forum.php?mod=forumdisplay&fid=95&page={i}"
        html = get_html(page_url)
        id_list = re.findall(r'tid=.*?class="s xst"', html)
        tid_list = [i[4:10] for i in id_list]
        article_list += tid_list
    print(f"得到总的文章链接是:{len(article_list)}")
    return article_list


def get_comment_txt(count):
    print(f"获取评论内容:{count}")
    txt_list = ["看起来挺骚的", "溜了，评分留下", "典型的大妈脸", "都是猛人", "被吓到了", "还是支持一下",
                "最近啥情况", "怎么看不了", "感谢大佬", "有磁力的吗", "最近这种有点多啊", "我看到过的", "这也太牛逼了",
                "感谢大佬的精彩分享", "都是神人", "艺高人胆大", "就是喜欢这样的题材", "这个不太好吧", "也开始拍剧情了",
                "看着真实", "不知道真的假的", "这么会玩的吗", "这可太刺激了", "看看这次是什么情况", "看着眼熟",
                "好资源，评分送上", "有够刺激的", "这玩意儿看看就好", "多更新这种题材的", "满足一下幻想", "不会是假的吧",
                "不好意思发了", "怎么全是链接错误", "但还是很喜欢", "刺激就行啊", "看不到了", "这些资源", "真不错真不错",
                "笑死我了哈哈哈", "高手在民间", "多谢老哥分享", "看起来挺不错", "先赞后看", "的确是好内容", "真人想多了",
                "因为我本纯良", "这个主题不错"]
    return txt_list[random.randint(0, len(txt_list)-1)]


def post_comm(tid, txt):
    print(f"开始评论了：{tid}, 评论内容是: {txt}")
    url = f"{source_url}/forum.php?mod=post&action=reply&fid=95&tid={tid}&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
    header = {
        "user-agent": user_agent,
        "cookie": cookie
    }
    data = {
        "message": txt,
        "posttime": int(time.time()),
        "formhash": "24435fbb"
    }
    res = requests.post(url, headers=header, data=data)
    set_cookies(res)
    print(res.content.decode())
    html = res.content.decode()
    if "回复发布成功" in html:
        print("评论完成了....")
    else:
        print("评论失败了")


def post_commit(tid, txt):
    print(f"开始回复评论：{tid} : {txt}")
    url = f"https://zxfdsfdsf.online/forum.php?mod=post&action=reply&fid=95&tid={tid}&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
    # payload = 'file=&message=%E4%B8%80%E7%9B%B4%E5%8F%91%E7%83%A7&posttime=1672651842&formhash=44a857f9&usesig=&subject=%2B%2B'
    body = {
        "file": "",
        "message": txt,
        "posttime": "1672651842",
        "formhash": "44a857f9",
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
        'cookie': cookie,
        'user-agent': user_agent
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    html = response.text
    if "回复发布成功" in html:
        print("回复发布成功, 评论完成了....")
        return True
    else:
        print(response.text)
        print("评论失败了")
        return False


def run():
    print(f"开始98评论主程序：{name}")
    # 获取评论过的文章
    id_list = get_commenteds()
    # 获取前10页的文章链接
    article_list = get_articales()
    # 过滤没有评论过的文章链接
    need_post = [i for i in article_list if i not in id_list]
    # 发起评论
    for index, value in enumerate(need_post):
        commit_txt = get_comment_txt(index)
        res = post_commit(value, commit_txt)
        if res:
            break
        else:
            continue


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        name = "我要舔你"
        cookie = "cPNj_2132_saltkey=BZ6j6Q05; cPNj_2132_lastvisit=1672651408; cPNj_2132_atarget=1; cPNj_2132_visitedfid=95; cPNj_2132_sendmail=1; cPNj_2132_lastfp=bc56b1f21fc3b458ea72f14c0f3faf3d; cPNj_2132_ulastactivity=1672655030%7C0; cPNj_2132_auth=d996lSaxnPze8qXzo12cKXhiA%2BD2S6WmZ%2FS8i8ocG8N6GwINi5bObGbiruq5v7jBsX5s982HHNrW9JSQsMsgng7AuHE; cPNj_2132_lastcheckfeed=438345%7C1672655030; cPNj_2132_lip=208.115.243.40%2C1672655030; cPNj_2132_sid=0; cPNj_2132_st_t=438345%7C1672655031%7Caa33adfd508388d901700d97ff3d285d; cPNj_2132_forum_lastvisit=D_95_1672655031; cPNj_2132_smile=1D1; cPNj_2132_lastact=1672655062%09forum.php%09ajax; cPNj_2132_forum_lastvisit=D_95_1672655172; cPNj_2132_lastact=1672655172%09forum.php%09forumdisplay; cPNj_2132_sid=0; cPNj_2132_st_t=438345%7C1672655172%7Ce4afc1d6c40947fb0a6aa820a1431905"
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    else:
        name = sys.argv[1]
        cookie = sys.argv[2]
        user_agent = sys.argv[3]
    source_url = "https://zxfdsfdsf.online"
    run()
