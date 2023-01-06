import sys
import re
import time
from urllib import parse
import requests
import random


def get_html(page_url):
    print(f"开始获取html: {page_url}")
    payload = {}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'user-agent': user_agent
    }
    res = requests.request("GET", page_url, headers=headers, data=payload)
    try:
        html = res.content.decode()
        # set_cookies(res)
        return html
    except Exception as e:
        print(res.text)
        print(f"获取html出错：{e},开始重试新的请求。。。。。。。")
        raise Exception("获取html出错")


def get_user_info(param=""):
    url = f"{source_url}/home.php?mod=spacecp&ac=credit&showcredit=1"
    payload = {}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'user-agent': user_agent
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)
    user_info = {
        "用户名": re.search(r'访问我的空间">(.*?)</a>', response.text).group(1),
        "用户组": re.search(r'用户组: (.*?)</a>', response.text).group(1),
        "金钱": re.search(r'金钱: </em>(.*?)  &nbsp;', response.text).group(1),
        "积分": re.search(r'积分: </em>(.*?) </li>', response.text).group(1),
    }
    print(f"今日用户信息: {user_info}")
    return user_info


def get_commenteds():
    print("获取评论过的文章:")
    id_list = []
    page = 1
    while True:
        url = f"{source_url}/forum.php?mod=guide&view=my&type=reply&page={page}"
        html = get_html(url)
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
                "不好意思发了", "怎么全是链接错误", "但还是很喜欢", "刺激就行啊", "看不到了", "这些资源",
                "真不错真不错",
                "笑死我了哈哈哈", "高手在民间", "多谢老哥分享", "看起来挺不错", "先赞后看", "的确是好内容",
                "真人想多了",
                "因为我本纯良", "这个主题不错"]
    return txt_list[random.randint(0, len(txt_list) - 1)]


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
    set_cookies(res, cookie)
    print(res.content.decode())
    html = res.content.decode()
    if "回复发布成功" in html:
        print("评论完成了....")
    else:
        print("评论失败了")


def get_formhash(tid):
    print("获取hash值")
    url = f"{source_url}/forum.php?mod=viewthread&tid={tid}&extra=page%3D1"
    payload = {}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'user-agent': user_agent
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)
    form_hash = re.search(r'formhash=(.*?)">退出</a>', response.text).group(1)
    return form_hash


def post_commit(tid, txt, form_hash):
    print(f"开始回复评论：{tid} : {txt} hash:{form_hash}")
    url = f"https://zxfdsfdsf.online/forum.php?mod=post&action=reply&fid=95&tid={tid}&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
    # payload = 'file=&message=%E4%B8%80%E7%9B%B4%E5%8F%91%E7%83%A7&posttime=1672651842&formhash=44a857f9&usesig=&subject=%2B%2B'
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


def exec_jisuan(sunshu):
    res = eval(sunshu)
    print(f"算术答案: {sunshu} = {res}")
    return res


def set_cookies(res, cookie):
    cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
    c = res.cookies.get_dict()
    cookie_dict.update(c)
    cookie = "; ".join([f"{key}={val}" for key, val in cookie_dict.items()])
    return cookie


def get_suanshu(cookie):
    print(f"获取算术内容")
    url = f"{source_url}/plugin.php?id=dd_sign&mod=sign&mobile=2"
    payload = {}
    headers = {
        'authority': 'zxfdsfdsf.online',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cookie': cookie,
        'referer': f'{source_url}/plugin.php?id=dd_sign:index&mobile=2',
        'upgrade-insecure-requests': '1',
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    cookie = set_cookies(response, cookie)
    suanshu = re.search(r'输入下面问题的答案<br />(.*?) = \?</span>', response.text).group(1)
    res = exec_jisuan(suanshu)
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


def start_sign(params):
    print("开始签到")
    url = "https://zxfdsfdsf.online/plugin.php?id=dd_sign&mod=sign&signsubmit=yes&signhash=&handlekey=signform_&inajax=1"
    payload = f"formhash={params.get('formhash')}&signtoken={params.get('signtoken')}&secqaahash={params.get('secqaahash')}&secanswer={params.get('secanswer')}"
    headers = {
        'authority': 'zxfdsfdsf.online',
        'accept': 'application/xml, text/xml, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': params.get("cookie"),
        'origin': 'https://zxfdsfdsf.online',
        'referer': 'https://zxfdsfdsf.online/plugin.php?id=dd_sign&mod=sign&mobile=2',
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


def run():
    user_info = get_user_info()
    print(f"开始98评论主程序：{user_info.get('用户名')}")
    # 开始签到
    # params = get_suanshu(cookie)
    # start_sign(params)
    # 获取评论过的文章
    id_list = get_commenteds()
    # 获取前10页的文章链接
    article_list = get_articales()
    # 过滤没有评论过的文章链接
    need_post = [i for i in article_list if i not in id_list]
    # 发起评论
    for index, value in enumerate(need_post):
        commit_txt = get_comment_txt(index)
        form_hash = get_formhash(value)
        res = post_commit(value, commit_txt, form_hash)
        if res:
            break
        else:
            continue


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        name = "我真的很爱你"
        cookie = "cPNj_2132_saltkey=r9fMr1et;cPNj_2132_lastvisit=1672979843;cPNj_2132__refer=%252Fhome.php%253Fmod%253Dspacecp%2526ac%253Dinvite;cPNj_2132_lastfp=66abe79b56fe4d1db0defa055279da8b;cPNj_2132_sendmail=1;cPNj_2132_ulastactivity=1672983458%7C0;cPNj_2132_auth=43873yPqTgtEoPyWDNJ%2Fgd86pFxYXj45LvXi3QquKWYazTni4wpzUO7%2FrGaeEvlWwd6X0qnpxJ8APJxY2iyaTVlfScA;cPNj_2132_lastcheckfeed=438758%7C1672983458;cPNj_2132_checkfollow=1;cPNj_2132_lip=116.236.218.154%2C1672983458;cPNj_2132_sid=0;cPNj_2132_checkpm=1;cPNj_2132_home_diymode=1;cPNj_2132_lastact=1672983482%09misc.php%09patch"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    else:
        name = sys.argv[1]
        cookie = sys.argv[2]
        user_agent = sys.argv[3]
    source_url = "https://zcdsade.cfd"
    run()
