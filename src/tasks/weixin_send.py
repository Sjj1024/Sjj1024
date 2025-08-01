import requests
import json
import datetime


def send_wx(params):
    url = "https://wxpusher.zjiecode.com/api/send/message"
    payload = json.dumps({
        "appToken": "",
        "content": f"<h1>H1标题</h1><br/><p style=\"color:red;\">请进行签到: {params}</p>",
        "summary": f"签到:{params}",
        "contentType": 2,
        "uids": [
            ""
        ],
        "verifyPayType": 0
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def main():
    print("发送消息")
    current_hour = datetime.datetime.now().hour + 8
    current_minute = datetime.datetime.now().minute
    current_second = datetime.datetime.now().second
    current_time = f"{current_hour}点{current_minute}分{current_second}秒"
    dayOfWeek = datetime.datetime.now().weekday() + 1
    print(f"今天是星期{dayOfWeek}, 当前时间是：{current_time}")
    if (current_hour == 7) and (1 <= current_minute <= 59):
        content = f"上班打卡了，亲爱的宝子们~，当前时间:{current_time}"
        send_wx("6-8:30")
    elif (current_hour == 12) and (1 <= current_minute < 59):
        content = f"快点外卖吧，吃的胖胖的才有劲干活啊，亲爱的宝~, 当前时间:{current_time}"
        send_wx("12-2:30")
    elif (current_hour == 20) and (1 <= current_minute < 59):
        content = f"别干了，快下班打卡吧！总是忘记打卡的人，是不是你？！！！,当前时间:{current_time}"
        send_wx("7-9:30")
    else:
        print("不用发送打卡内容")


if __name__ == '__main__':
    main()
