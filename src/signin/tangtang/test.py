import requests

url = "https://zxfdsfdsf.online/plugin.php?id=dd_sign&mod=sign&signsubmit=yes&signhash=&handlekey=signform_&inajax=1"
payload = "formhash=22a219c9&signtoken=d943d73f1d4c7299835d4bc66e3a717f&secqaahash=SGk1c&secanswer=64"
headers = {
  'authority': 'zxfdsfdsf.online',
  'accept': 'application/xml, text/xml, */*; q=0.01',
  'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'cookie': 'cPNj_2132_saltkey=hxX55J5a; cPNj_2132_lastvisit=1672747297; PHPSESSID=bcoe60n0h48f0r47359raie0le; cPNj_2132_lastfp=425c7d3ce09882875cd485c7f39ba317; cPNj_2132_ulastactivity=1672750903%7C0; cPNj_2132_auth=79a1Ock8ya6jC15taT1hMo5UtrYyqv3LLyJhKhC6Ztp9asoYtjyuX%2BvmQuU0ADqpaULmpcjHeDjN2MTs4PX2oTbVUrI; cPNj_2132_lastcheckfeed=417586%7C1672750903; cPNj_2132_lip=101.86.157.94%2C1672750903; cPNj_2132_sid=0; cPNj_2132_lastact=1672751610%09plugin.php%09sign; cPNj_2132_secqaa=10554.2218ab3ed78139ffde; cPNj_2132_lastact=1672751732%09plugin.php%09sign; cPNj_2132_secqaa=10466.cbf2e3fe0092406618; cPNj_2132_sid=0',
  'origin': 'https://zxfdsfdsf.online',
  'referer': 'https://zxfdsfdsf.online/plugin.php?id=dd_sign&mod=sign&mobile=2',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
  'x-requested-with': 'XMLHttpRequest'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
