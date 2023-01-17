import requests

url = "https://zxfdsfdsf.online/misc.php?mod=secqaa&action=update&idhash=qSAXuI0&0.4640535681735929"

payload={}
headers = {
  'authority': 'zxfdsfdsf.online',
  'accept': '*/*',
  'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
  'cookie': 'PHPSESSID=rm3gkta9m1fu4ig0mbuboeinnt; cPNj_2132_lastfp=66abe79b56fe4d1db0defa055279da8b; cPNj_2132_saltkey=NN4458B0; cPNj_2132_lastvisit=1673433278; cPNj_2132_auth=06788joK%2BD4uYlZRexqjR%2FG8wAZQ8JttJdnuYRzM6goKuvenUOLjNXRyasvLZVj%2BZwCmi2bDt9ohnbCnUoORIkva7Tk; cPNj_2132_lastcheckfeed=415015%7C1673436883; cPNj_2132_secqaaqSAEn10=10150.2b60e9210d2dd48385; cPNj_2132_home_diymode=1; cPNj_2132_nofavfid=1; cPNj_2132_sid=0; cPNj_2132_secqaaqSAOz20=4207.db50e0693c3d3f093c; cPNj_2132_secqaaqSATrT0=4545.7ba917518f0a6395fd; cPNj_2132_ulastactivity=1673840905%7C0; cPNj_2132_sendmail=1; cPNj_2132_lastact=1673841110%09plugin.php%09sign; cPNj_2132_lastact=1673847418%09misc.php%09secqaa; cPNj_2132_secqaaqSAXuI0=5804.f63279cc86265e8174',
  'referer': 'https://zxfdsfdsf.online/plugin.php?id=dd_sign:index',
  'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'script',
  'sec-fetch-mode': 'no-cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
