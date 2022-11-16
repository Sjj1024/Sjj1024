import requests
import json

url = "https://msg.csdn.net/v1/web/message/view/unread"

payload = json.dumps({
  "coupon": True
})
headers = {
  'authority': 'msg.csdn.net',
  'accept': 'application/json, text/javascript, */*; q=0.01',
  'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
  'content-type': 'application/json',
  'cookie': 'uuid_tt_dd=10_19616795140-1665200689671-367015; __gads=ID=d06c9a6acbfc1de7-2220d55ea4d70068:T=1665200691:RT=1665200691:S=ALNI_Mbu5JkrC1adgb9kBV62ZZpxg4gdQg; UserName=weixin_44786530; UserInfo=3e9da6fdfcef4018b71fb7dd299b9661; UserToken=3e9da6fdfcef4018b71fb7dd299b9661; UserNick=1024%E5%B0%8F%E7%A5%9E; AU=47C; UN=weixin_44786530; BT=1665208243704; p_uid=U010000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22weixin_44786530%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_19616795140-1665200689671-367015!5744*1*weixin_44786530; dc_sid=03889dd58c5ee2a617f40f993a5c88bb; c_segment=7; _ga=GA1.2.1557385788.1667204710; historyList-new=%5B%22swift%22%5D; __bid_n=18450b4328cbb03b4b4207; c_dl_fref=https://link.csdn.net/; c_dl_fpage=/download/weixin_42186579/15599070; c_dl_um=-; c_dl_prid=1668161160538_769822; c_dl_rid=1668161164852_281043; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1668160708,1668482890; dc_session_id=10_1668592227759.680259; log_Id_click=70; SESSION=NDViNjJjYWQtZDc1YS00NGI4LTk2ODMtNTI5MGY2MWUyNWY3; c_hasSub=true; c_page_id=default; c_pref=default; c_ref=default; c_first_ref=default; c_utm_source=1019330866; utm_source=1019330866; c_first_page=https%3A//www.csdn.net/%3Fspm%3D1001.2014.3001.4476; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1668594817; log_Id_view=588; ssxmod_itna2=iqRxRD0D9D2AeAKGHqInEDBDowjuD7KGkmQ+D8q=4xGXvQGaY4vcQ8x82YKo9r5wsVWAwvXQB9cdKep4ZoRathWwgEBbsQKEkDTGWP/pkizmu7W76RMB=S5ew/GiC/js1EbYIj9t0MNOfdjiAdNwWDjj4r26nde/e+x4nomX9bUC4x3eyEu0ACr1BM2Gl2nCCnUCfufe4Ra45i5B9361Gd5B4dh7Rhjj70az/wvp8Ty+uSYMiZv=8OB8Yr2h=GxwYgyrFq4Y3Sgim/LNkfPjVcGS3RGRNoIUQB7qMqZwHy/gVpxObqifAAVgfhONKBwC0vVaPK0wnAdKWw5RNhmK4F2FWt/WERowUWPVo6soir4QqtRT93Mhib+0XWoeFvN/LSmI87RVhRYFbOideKbi8Xk4vUCTP+tWIKFIRqtwbUrzURsow02Nmn4ezWe45pR=MrqH2Iimh+0I7ntI7un3bQFjTza6C9jAYLGdKWU8YjKFf7nYpDv+EEtOHIY7I7DZnEeuNMOpS+4DQKq87V8rZI9NUQp6gmGG7yR0D08DiQeYD===; ssxmod_itna=iqmxBDyD0DuD9iKtGHqiQTLuODcDRO0BhATodqGNLUoDZDiqAPGhDC8bFlmiEWor3TQRlEy3G3FOWgDrEmZ0RftQiQhYGLDmKDy7i7+hoD4RKGwD0eG+DD4DWDmWHDnxAQDjxGp9uXwV=Dm4GW8qGfDDoDYf6uDitD4qDBGOdDKqGg8T26CntdEwxP60+9D0tQxBLtbah9mWaFaGNPPpnxTgQDzTHDtqNMSLddx0PBldXxvY+W+74zKLwa704q4Ex5KYwtS0wNzikTS7GNiBwRrgeQWiD===; c_dsid=11_1668594836301.449733; dc_tos=rlfs0k; log_Id_pv=51',
  'origin': 'https://www.csdn.net',
  'referer': 'https://www.csdn.net/?spm=1001.2014.3001.4476',
  'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
