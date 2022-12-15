import requests

url = "https://w1.v2free.net/user/checkin"

payload = {}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Cookie': '_ga_NC10VPE6SR=GS1.1.1671083653.1.1.1671083741.0.0.0; _ga=GA1.1.2067806519.1671083654; uid=97689; email=ww-1096%40163.com; key=cc050c87a8ef20f8cc331f342bcac06cac1b514e3044f; ip=a91e7e9256cabb3e26c17318942088bf; expire_in=1673675701; _gcl_au=1.1.742135731.1671083707; crisp-client%2Fsession%2Fa47ae3dd-53d8-4b15-afae-fb4577f7bcd0=session_3e618f61-c349-4a46-bdc0-9e905d3e4222; crisp-client%2Fsocket%2Fa47ae3dd-53d8-4b15-afae-fb4577f7bcd0=0',
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

print(response.json())
