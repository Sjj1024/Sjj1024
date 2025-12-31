#!/usr/bin/env Python
# -*- coding: utf-8 -*-

"""
请求http和https网页均适用
"""
import requests
from playwright.sync_api import sync_playwright

# 提取代理API接口，获取1个代理IP
# api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=or67jn7d4eam4s7zzqnk&num=1&signature=$YOUR_SIGNATURE&sep=1"

# 获取API接口返回的代理IP
proxy_ip = "58.19.54.135:13006"

# 用户名密码方式
username = "d2998408627"
password = "zwgh3kro"

# 要访问的目标网页
url = "https://www.douyin.com/user/MS4wLjABAAAAH_YSjSBpUOItBNIP5B3B235ER7GUYgJ1qnkpKPF2kKc?from_tab_name=main"

proxies = {
    "server": proxy_ip,
    "username": username,
    "password": password,
}

# 白名单方式（需提前设置白名单）
# proxies = {
#     "server": proxy,
# }

with sync_playwright() as playwright:
    # headless=True 无头模式，不显示浏览器窗口
    # browser = playwright.chromium.launch(channel="msedge", headless=True, proxy=proxies)  # Microsoft Edge 浏览器
    # browser = playwright.firefox.launch(headless=True, proxy=proxies)                     # Mozilla Firefox 浏览器
    # browser = playwright.webkit.launch(headless=True, proxy=proxies)                      # WebKit 浏览器，如 Apple Safari
    browser = playwright.chromium.launch(channel="chrome", headless=False, proxy=proxies)  # Google Chrome 浏览器
    context = browser.new_context()
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=80000)
    content = page.content()
    print(context)
    if "awemeCount" in content:
        print(f"抖音号作品数存在")
    else:
        print(f"抖音号作品数不存在")
    # other actions...
    browser.close()

# sucess! client ip: 118.183.78.232
# sucess! client ip: 120.225.114.171