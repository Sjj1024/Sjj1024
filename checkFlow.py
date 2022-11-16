import datetime
import requests
import json


def print_current():
    print("当前时间是", datetime.datetime.now())


def sing_in():
    url = "https://ug.baidu.com/mcp/pc/pcsearch"

    payload = json.dumps({
        "invoke_info": {
            "pos_1": [
                {}
            ],
            "pos_2": [
                {}
            ],
            "pos_3": [
                {}
            ]
        }
    })
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'BIDUPSID=D7B9154ACC8761518E035AB612CDE524; PSTM=1665195559; BAIDUID=D7B9154ACC876151D59CE7C83EA954CF:FG=1; BDUSS=zlzS1k5S3dyYmZDLTVRbWlhSGpsd0NBR3hYWm0yeVBDSH5vV0pyV1ZoM1VmR2hqSVFBQUFBJCQAAAAAAAAAAAEAAABzJ0dPwLbQx01lMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANTvQGPU70BjZ; BDUSS_BFESS=zlzS1k5S3dyYmZDLTVRbWlhSGpsd0NBR3hYWm0yeVBDSH5vV0pyV1ZoM1VmR2hqSVFBQUFBJCQAAAAAAAAAAAEAAABzJ0dPwLbQx01lMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANTvQGPU70BjZ; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=36552_37683_37773_37623_34812_37303_37724_37801_37672_37743_26350_37791; MCITY=-289%3A; delPer=0; BA_HECTOR=2ha4a4018l8l2g252l2l20pm1hn96c41e; BAIDUID_BFESS=D7B9154ACC876151D59CE7C83EA954CF:FG=1; ZFY=k5SgfWxnERUsb2TJIifkPp:AQCreOIlz9U:AgL:BuZjCaA:C; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[tox4WRQ4-Km]=mk3SLVN4HKm; ab_sr=1.0.1_OWE5ODRlN2E1YjkxMTdjNmIyZDcxZGNjOGY1YTYyMzRmYTgzOWYwZWFjM2VjYThlMTk3ZDQ2MDMyNDQ2MTgyMTFjZjA2Mjg5Y2EzN2IzMWUxMTE0YzY2MDZiMWZlZjA2N2IxMWVhOWFjY2FmNzFmZDJlMDRkZjZhMzZjNmQ3NzExYTllZTc2YjkzNGRiMTc0MjFjNDk3MTYxMjYwOGVmZDJiMTU3ZmZjZWM0Y2NjMDQ3ZjgwMGVkYzA1ZWVkYTk4; PSINO=2',
        'Origin': 'https://www.baidu.com',
        'Referer': 'https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=baidu&wd=%E7%83%AD%E9%A5%AD%E8%8F%9C%E6%94%BE%E8%BF%9B%E5%86%B0%E7%AE%B1%E5%8F%AF%E4%BB%A5%E5%90%97&oq=%25E7%2583%25AD%25E9%25A5%25AD%25E8%258F%259C%25E6%2594%25BE%25E8%25BF%259B%25E5%2586%25B0%25E7%25AE%25B1%25E5%258F%25AF%25E4%25BB%25A5%25E5%2590%2597&rsv_pq=be37abea000358fb&rsv_t=a3ffRJxBGCz4CA15rsUBWLCrB8MoX63dQJuCFe8snFj0NI6WB7kUIPj34MM&rqlang=cn&rsv_enter=0&rsv_dl=ts_0&rsv_btype=t&prefixsug=%25E7%2583%25AD%25E9%25A5%25AD%25E8%258F%259C%25E6%2594%25BE%25E8%25BF%259B%25E5%2586%25B0%25E7%25AE%25B1%25E5%258F%25AF%25E4%25BB%25A5%25E5%2590%2597&rsp=0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    print_current()
    sing_in()
