import requests
import src.common.index as common


def get_ssr(key, cookie):
    url = "https://w1.v2free.net/user/checkin"
    payload = {}
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Cookie': cookie,
        'Origin': 'https://w1.v2free.net',
        'Referer': 'https://w1.v2free.net/user',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        print(f"{key}: {response.json()}")
        return f"{key}: {response.json()}"
    except Exception as e:
        print(f"{key}: {response.content}: {e}")
        return f"{key}: {response.content}: {e}"


def main():
    print("开始执行V2Free签到------------------------")
    some_one = common.common_conf.get("v2free").get("account")
    msg_list = []
    for (key, val) in some_one.items():
        msg = get_ssr(key, val)
        msg_list.append(msg)
    common.common_msg["V2FREE"] = f"签到:{msg_list}"


main()
