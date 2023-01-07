import requests
from bs4 import BeautifulSoup
import src.common.index as common


def sign(cookie):
    result = ""
    headers = {
        "Cookie": cookie,
        "ContentType": "text/html;charset=gbk",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    }
    requests.session().put(
        "https://www.52pojie.cn/home.php?mod=task&do=apply&id=2", headers=headers
    )
    fa = requests.session().put(
        "https://www.52pojie.cn/home.php?mod=task&do=draw&id=2", headers=headers
    )
    fb = BeautifulSoup(fa.text, "html.parser")
    fc = fb.find("div", id="messagetext").find("p").text
    if "您需要先登录才能继续本操作" in fc:
        result += "Cookie 失效"
    elif "恭喜" in fc:
        result += "签到成功"
    elif "不是进行中的任务" in fc:
        result += "今日已签到"
    else:
        result += "签到失败"
    print(result)
    return result


def main():
    print("开始执行52破解签到------------------------")
    some_one = common.common_conf.get("52pojie").get("account")
    msg_list = []
    for (key, val) in some_one.items():
        sign_msg = sign(cookie=val)
        print(f"52破解签到:{sign_msg}")
        msg_list.append(sign_msg)
    common.common_msg["52破解"] = msg_list


main()
