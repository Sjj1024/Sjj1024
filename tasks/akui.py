import requests

url = "https://w1.v2free.net/user/checkin"

payload={}
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
  'Connection': 'keep-alive',
  'Content-Length': '0',
  'Cookie': '_ga=GA1.1.1297017311.1668585169; uid=86785; email=zhaoakun%40qq.com; key=6adb0f8be42cac2cbe71a5c6536c94667413bbec0fd80; ip=2b5a6657c79039bf4edff64ab8964a31; expire_in=1671177401; _gcl_au=1.1.81869821.1668585404; _ga_NC10VPE6SR=GS1.1.1668650754.3.1.1668651294.0.0.0; crisp-client%2Fsession%2Fa47ae3dd-53d8-4b15-afae-fb4577f7bcd0=session_36437667-79c6-4f5a-bb2c-18af83c92846; crisp-client%2Fsocket%2Fa47ae3dd-53d8-4b15-afae-fb4577f7bcd0=0',
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
