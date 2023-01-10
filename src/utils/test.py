import requests
res = requests.get('http://myip.ipip.net', timeout=5).text
print(res)