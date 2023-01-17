# import re
#
# import requests
#
# import src.common.index as common
#
#
# def exec_jisuan(sunshu):
#     res = eval(sunshu)
#     print(f"算术答案: {sunshu} = {res}")
#     return res
#
#
# def set_cookies(res, cookie):
#     cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
#     c = res.cookies.get_dict()
#     cookie_dict.update(c)
#     cookie = "; ".join([f"{key}={val}" for key, val in cookie_dict.items()])
#     return cookie
#
#
# def get_suanshu(cookie):
#     print(f"获取算术内容")
#     url = f"{source_url}/plugin.php?id=dd_sign&mod=sign&mobile=2"
#     payload = {}
#     headers = {
#         'authority': 'zxfdsfdsf.online',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
#         'cookie': cookie,
#         'referer': f'{source_url}/plugin.php?id=dd_sign:index&mobile=2',
#         'upgrade-insecure-requests': '1',
#         'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
#     }
#     response = requests.request("GET", url, headers=headers, data=payload)
#     cookie = set_cookies(response, cookie)
#     suanshu = re.search(r'输入下面问题的答案<br />(.*?) = \?</span>', response.text).group(1)
#     res = exec_jisuan(suanshu)
#     params = {
#         "id": "dd_sign",
#         "mod": "sign",
#         "signsubmit": "yes",
#         "signhash": "",
#         "handlekey": "signform_",
#         "inajax": "1",
#         "formhash": re.search(r'formhash" value="(.*?)" />', response.text).group(1),
#         "signtoken": re.search(r'name="signtoken" value="(.*?)" />', response.text).group(1),
#         "secqaahash": re.search(r'secqaahash" type="hidden" value="(.*?)" />', response.text).group(1),
#         "secanswer": res,
#         "cookie": cookie
#     }
#     return params
#
#
# def start_sign(params):
#     print("开始签到")
#     url = "https://zxfdsfdsf.online/plugin.php?id=dd_sign&mod=sign&signsubmit=yes&signhash=&handlekey=signform_&inajax=1"
#     payload = f"formhash={params.get('formhash')}&signtoken={params.get('signtoken')}&secqaahash={params.get('secqaahash')}&secanswer={params.get('secanswer')}"
#     headers = {
#         'authority': 'zxfdsfdsf.online',
#         'accept': 'application/xml, text/xml, */*; q=0.01',
#         'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
#         'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'cookie': params.get("cookie"),
#         'origin': 'https://zxfdsfdsf.online',
#         'referer': 'https://zxfdsfdsf.online/plugin.php?id=dd_sign&mod=sign&mobile=2',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-origin',
#         'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
#         'x-requested-with': 'XMLHttpRequest'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     if "签到成功" in response.text:
#         print("签到成功，金钱+2，明天记得来哦")
#         return True
#     elif "已经签到过啦，请明天再来" in response.text:
#         print("已经签到过啦，请明天再来！")
#         return True
#     else:
#         print(f"签到失败：{response.text}")
#         return False
#
#
# def get_user_info(params):
#     url = f"{source_url}/home.php?mod=spacecp&ac=credit&showcredit=1"
#     payload = {}
#     headers = {
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
#         'cache-control': 'max-age=0',
#         'cookie': params.get("cookie"),
#         'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
#     }
#     response = requests.request("GET", url, headers=headers, data=payload)
#     # print(response.text)
#     user_info = {
#         "用户名": re.search(r'访问我的空间">(.*?)</a>', response.text).group(1),
#         "用户组": re.search(r'用户组: (.*?)</a>', response.text).group(1),
#         "金钱": re.search(r'金钱: </em>(.*?)  &nbsp;', response.text).group(1),
#         "积分": re.search(r'积分: </em>(.*?) </li>', response.text).group(1),
#     }
#     print(f"今日用户信息: {user_info}")
#     return user_info
#
#
# def run():
#     some_one = common.common_conf.get("98tang").get("account")
#     msg_list = []
#     for (key, val) in some_one.items():
#         params = get_suanshu(val)
#         msg = get_user_info(params)
#         res_flag = start_sign(params)
#         if res_flag:
#             msg = get_user_info(params)
#             msg_list.append(msg)
#     common.common_msg["98Tang"] = msg_list
#
#
# source_url = "https://zxfdsfdsf.online"
#
# if __name__ == '__main__':
#     # cookie = 'cPNj_2132_saltkey=hxX55J5a; cPNj_2132_lastvisit=1672828669; cPNj_2132_lastfp=ca2c26c95a40ea67064e19fe01c0d6f2; cPNj_2132_hide_show=true; cPNj_2132_ulastactivity=1672832277%7C0; cPNj_2132_auth=ebee2aeAXGN1Udu4ehZWA%2FHlmYn0diMDOpYzhLsnAYR7FB929oOqy9FJI9cyFroAcNnBzLjYAuj2K30dSDQ2kyPp90E; cPNj_2132_lastcheckfeed=438345%7C1672832277; cPNj_2132_lip=101.86.157.94%2C1672832277; cPNj_2132_sid=0; cPNj_2132_home_diymode=1; cPNj_2132_lastact=1672832295%09home.php%09space'
#     # user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
#     run()
# else:
#     run()
