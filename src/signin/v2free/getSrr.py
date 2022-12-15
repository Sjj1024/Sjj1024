import requests


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
    print(f"{key}: {response.json()}")


def main():
    some_one = {
        "akui": '_ga=GA1.1.1297017311.1668585169; uid=86785; email=zhaoakun%40qq.com; key=6adb0f8be42cac2cbe71a5c6536c94667413bbec0fd80; ip=2b5a6657c79039bf4edff64ab8964a31; expire_in=1671177401; _gcl_au=1.1.81869821.1668585404; _ga_NC10VPE6SR=GS1.1.1668650754.3.1.1668651294.0.0.0; crisp-client%2Fsession%2Fa47ae3dd-53d8-4b15-afae-fb4577f7bcd0=session_36437667-79c6-4f5a-bb2c-18af83c92846; crisp-client%2Fsocket%2Fa47ae3dd-53d8-4b15-afae-fb4577f7bcd0=0',
        "song": '_ga=GA1.1.1292341500.1665285856; _gcl_au=1.1.375450545.1665285875; uid=70939; email=15670339118%40163.com; key=cb1d245a9b7a543b5211e8d4c75f54de25ab03a068b81; ip=bcc2edbac933ad4453dc67d20c8bbab9; expire_in=1696821904; crisp-client%2Fsession%2Fa47ae3dd-53d8-4b15-afae-fb4577f7bcd0=session_827e75a5-0b22-4df2-a1e4-4787b3660c37; _ga_NC10VPE6SR=GS1.1.1668649347.16.1.1668649352.0.0.0',
        "xuelei": '_ga=GA1.1.84090738.1668585122; uid=86781; email=403783342@qq.com; key=65b4d3b2c246af755e497a9d078aa8a9b83f8fa52be8f; ip=31e319515740e845fd3560e00ccd8b59; expire_in=1671177159; _gcl_au=1.1.1696281904.1668585162; crisp-client/session/a47ae3dd-53d8-4b15-afae-fb4577f7bcd0=session_3d63d0e7-a516-4868-899a-33974a413cb2; _ga_NC10VPE6SR=GS1.1.1668651055.3.0.1668651063.0.0.0',
        "wubo": '_ga_NC10VPE6SR=GS1.1.1671083653.1.1.1671083741.0.0.0; _ga=GA1.1.2067806519.1671083654; uid=97689; email=ww-1096%40163.com; key=cc050c87a8ef20f8cc331f342bcac06cac1b514e3044f; ip=a91e7e9256cabb3e26c17318942088bf; expire_in=1673675701; _gcl_au=1.1.742135731.1671083707; crisp-client%2Fsession%2Fa47ae3dd-53d8-4b15-afae-fb4577f7bcd0=session_3e618f61-c349-4a46-bdc0-9e905d3e4222; crisp-client%2Fsocket%2Fa47ae3dd-53d8-4b15-afae-fb4577f7bcd0=0',
        "xingwen": '_ga=GA1.1.1566143820.1671083625; uid=97690; email=996711778@qq.com; key=12db704880ee43c5cd2dc8cdc4e55c4f6876b2e071b55; ip=be269f8e3abd74e57f93dff4299e7789; expire_in=1673675735; _gcl_au=1.1.499271899.1671083738; _ga_NC10VPE6SR=GS1.1.1671083624.1.1.1671083813.0.0.0',
    }
    for (key, val) in some_one.items():
        get_ssr(key, val)


main()
