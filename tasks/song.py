import requests

url = "https://w1.v2free.net/user/checkin"

payload={}
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
  'Connection': 'keep-alive',
  'Content-Length': '0',
  'Cookie': '_ga=GA1.1.1292341500.1665285856; _gcl_au=1.1.375450545.1665285875; uid=70939; email=15670339118%40163.com; key=cb1d245a9b7a543b5211e8d4c75f54de25ab03a068b81; ip=bcc2edbac933ad4453dc67d20c8bbab9; expire_in=1696821904; crisp-client%2Fsession%2Fa47ae3dd-53d8-4b15-afae-fb4577f7bcd0=session_827e75a5-0b22-4df2-a1e4-4787b3660c37; _ga_NC10VPE6SR=GS1.1.1668649347.16.1.1668649352.0.0.0',
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
