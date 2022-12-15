import requests

url = "https://w1.v2free.net/user/checkin"

payload = {}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Cookie': '_ga=GA1.1.1566143820.1671083625; uid=97690; email=996711778@qq.com; key=12db704880ee43c5cd2dc8cdc4e55c4f6876b2e071b55; ip=be269f8e3abd74e57f93dff4299e7789; expire_in=1673675735; _gcl_au=1.1.499271899.1671083738; _ga_NC10VPE6SR=GS1.1.1671083624.1.1.1671083813.0.0.0',
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
