import requests

url = "https://w1.v2free.net/user/checkin"

payload={}
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
  'Connection': 'keep-alive',
  'Content-Length': '0',
  'Cookie': '_ga=GA1.1.84090738.1668585122; uid=86781; email=403783342@qq.com; key=65b4d3b2c246af755e497a9d078aa8a9b83f8fa52be8f; ip=31e319515740e845fd3560e00ccd8b59; expire_in=1671177159; _gcl_au=1.1.1696281904.1668585162; crisp-client/session/a47ae3dd-53d8-4b15-afae-fb4577f7bcd0=session_3d63d0e7-a516-4868-899a-33974a413cb2; _ga_NC10VPE6SR=GS1.1.1668651055.3.0.1668651063.0.0.0',
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
