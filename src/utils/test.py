import requests

url = "https://payjs.cn/api/native"

payload = 'body=payjs%E6%94%B6%E6%AC%BE%E6%B5%8B%E8%AF%95&out_trade_no=1699601458&total_fee=10&mchid=1593541201&sign=F6987C896F199229D40D0DE521427F5D'
headers = {
    'content-type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
