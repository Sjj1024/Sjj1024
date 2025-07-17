import random
import time
import requests
import os
import json


def get_issue(keyword):
    url = f"https://api.github.com/search/issues?q={keyword}+state:open+in:title+repo:Sjj1024/PakePlus"
    headers = {
        'Authorization': f'Bearer {os.environ.get("GITHUB_TOKEN")}'
    }
    print(f"github token", os.environ.get("GITHUB_TOKEN"))
    response = requests.request("GET", url, headers=headers).json()
    print("response", response)
    issue_list = response.get("items")
    print("issue list", len(issue_list))
    for iss in issue_list:
        issue_num = iss.get("number")
        title = iss.get("title")
        if keyword in title:
            if "error" in title:
                body = """PakePlus packaging failure fixes:  
1. Use the latest version, re-enter the token or click the sync button to try again.  
2. Delete the old project and create a new one to repackage and publish.  
3. Or check the FAQ documentation: https://ppofficial.netlify.app/question  
4. Or you can join our discussion group: https://ppofficial.netlify.app/exchange    
PakePlus打包失败修复：  
1.使用最新版本，重新填写token或点击同步按钮试试，  
2.删除老项目，重新创建一个新的项目再打包发布试试，  
3.或查看常见问题文档：https://ppofficial.netlify.app/zh/question  
4.或可以加入我们交流群：https://ppofficial.netlify.app/zh/exchange"""
                create_comments(issue_num, body)
            close_issue(issue_num, "closed")


def create_comments(num, body):
    print("create comments.........")
    random_sleep = random.randint(5, 20)
    print(f"sleep {random_sleep} seconds")
    time.sleep(random_sleep)
    url = f"https://api.github.com/repos/Sjj1024/PakePlus/issues/{num}/comments"
    payload = json.dumps({
        "body": body,
    })
    headers = {
        'Authorization': f'Bearer {os.environ.get("GITHUB_TOKEN")}',
        'Content-Type': 'text/plain'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print("create comments response", response.json())


def close_issue(num, state):
    print("close issue.........")
    random_sleep = random.randint(5, 20)
    print(f"sleep {random_sleep} seconds")
    time.sleep(random_sleep)
    url = f"https://api.github.com/repos/Sjj1024/PakePlus/issues/{num}"
    payload = json.dumps({
        "state": state,
    })
    headers = {
        'Authorization': f'Bearer {os.environ.get("GITHUB_TOKEN")}',
        'Content-Type': 'text/plain'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print("update issue response", response.json())


def run():
    keywords = ["build error"]
    for k in keywords:
        get_issue(k)
        time.sleep(14)
        print("sleep 14 seconds")


if __name__ == '__main__':
    for _ in range(10):
        run()
    print("pp issue")
