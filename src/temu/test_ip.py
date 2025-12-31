#!/usr/bin/env Python
# -*- coding: utf-8 -*-

"""
使用requests请求代理服务器
请求http和https网页均适用
"""

import requests

# 提取代理API接口，获取1个代理IP
# api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=or67jn7d4eam4s7zzqnk&signature=$YOUR_SIGNATURE&num=1&sep=1"
#
# 获取API接口返回的代理IP
proxy_ip = "59.47.5.138:17165"

# 用户名密码认证(私密代理/独享代理)
username = "d2998408627"
password = "zwgh3kro"
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
}

# 要访问的目标网页
target_url = "https://www.baidu.com/"

# 使用代理IP发送请求
response = requests.get(target_url, proxies=proxies)

# 获取页面内容
if response.status_code == 200:
    print(response.text)
