# 企业微信提醒点外卖打卡等
import datetime
import requests
import json


def work_on_remind(url, content):
    # 提醒上班打卡
    payload = json.dumps({
        "msgtype": "text",
        "text": {
            "content": "上班打卡了，亲爱的宝子们~",
            "mentioned_list": [
                "@all"
            ]
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def pay_lunch_remind(url, content):
    # 提醒点外卖
    payload = json.dumps({
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_list": [
                "@all"
            ]
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def work_off_remind(url, content):
    # 提醒下班打卡
    payload = json.dumps({
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_list": [
                "@all"
            ]
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def run():
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=89c9eedd-31db-4e36-bbb3-6176ed9b4395"
    current_time = datetime.datetime.now()
    current_hour = datetime.datetime.now().hour
    print("当前时间是", current_time)
    if current_hour < 10:
        content = f"上班打卡了，亲爱的宝子们~，当前时间:{current_time}"
        work_on_remind(url, content)
    elif current_hour < 12:
        content = f"快点外卖吧，吃的胖胖的才有劲干活啊，亲爱的宝~, 当前时间:{current_time}"
        pay_lunch_remind(url, content)
    elif current_hour < 19:
        content = f"别干了，快下班打卡吧！总是忘记打卡的人，是不是你？！！！,当前时间:{current_time}"
        work_off_remind(url, content)


if __name__ == '__main__':
    run()
