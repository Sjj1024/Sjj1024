import requests
import re
from urllib import parse


def exec_jisuan(sunshu):
    res = eval(sunshu)
    print(f"算术答案: {sunshu} = {res}")
    return res


def get_suanshu():
    print(f"获取算术内容")
    url = f"{source_url}/plugin.php?id=dd_sign&mod=sign&mobile=2"
    payload = {}
    headers = {
        'authority': 'zxfdsfdsf.online',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cookie': cookie,
        'referer': f'{source_url}/plugin.php?id=dd_sign:index&mobile=2',
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    suanshu = re.search(r'输入下面问题的答案<br />(.*?) = \?</span>', response.text).group(1)
    res = exec_jisuan(suanshu)
    params = {
        "id": "dd_sign",
        "mod": "sign",
        "signsubmit": "yes",
        "signhash": "",
        "handlekey": "signform_",
        "inajax": "1",
        "formhash": re.search(r'formhash" value="(.*?)" />', response.text).group(1),
        "signtoken": re.search(r'name="signtoken" value="(.*?)" />', response.text).group(1),
        "secqaahash": re.search(r'secqaahash" type="hidden" value="(.*?)" />', response.text).group(1),
        "secanswer": res
    }
    return params


def start_sign(params):
    print("开始签到")
    url = "https://zxfdsfdsf.online/plugin.php?id=dd_sign&mod=sign&signsubmit=yes&signhash=&handlekey=signform_&inajax=1"
    payload = f"formhash={params.get('formhash')}&signtoken={params.get('signtoken')}&secqaahash={params.get('secqaahash')}&secanswer={params.get('secanswer')}"
    headers = {
        'authority': 'zxfdsfdsf.online',
        'accept': 'application/xml, text/xml, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
        'origin': 'https://zxfdsfdsf.online',
        'referer': 'https://zxfdsfdsf.online/plugin.php?id=dd_sign&mod=sign&mobile=2',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user_agent,
        'x-requested-with': 'XMLHttpRequest'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def run():
    print(f"总流程控制")
    params = get_suanshu()
    start_sign(params)

if __name__ == '__main__':
    source_url = "https://zxfdsfdsf.online"
    cookie = 'cPNj_2132_saltkey=hxX55J5a; cPNj_2132_lastvisit=1672747297; PHPSESSID=bcoe60n0h48f0r47359raie0le; cPNj_2132_lastfp=425c7d3ce09882875cd485c7f39ba317; cPNj_2132_ulastactivity=1672750903%7C0; cPNj_2132_auth=79a1Ock8ya6jC15taT1hMo5UtrYyqv3LLyJhKhC6Ztp9asoYtjyuX%2BvmQuU0ADqpaULmpcjHeDjN2MTs4PX2oTbVUrI; cPNj_2132_lastcheckfeed=417586%7C1672750903; cPNj_2132_checkfollow=1; cPNj_2132_lip=101.86.157.94%2C1672750903; cPNj_2132_sid=0; cPNj_2132_lastact=1672750905%09plugin.php%09sign; cPNj_2132_secqaa=10424.46522ffb79d22368a2'
    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    run()
