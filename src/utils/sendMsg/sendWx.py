import requests
from urllib import parse
import smtplib
from email.mime.text import MIMEText
import src.common.index as common


def send_weixin(title, msg):
    content = str(msg)
    server_key = common.common_conf.get("message").get("server_key")
    url = f"https://sctapi.ftqq.com/{server_key}.send"
    title_encode = parse.quote(title)
    msg_encode = parse.quote(content)
    payload = f"title={title_encode}&desp={msg_encode}"
    headers = {
        'authority': 'sctapi.ftqq.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'origin': 'https://sct.ftqq.com',
        'referer': 'https://sct.ftqq.com/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"server_send:{response.json()}")


def send_qq(title, msg):
    qmsg_key = "78e1206603f05f58330f708de86d1fbc"
    params = {"msg": f"标题:{title}, 消息：{msg}"}
    res = requests.get(f"https://qmsg.zendee.cn:443/send/{qmsg_key}", params=params).json()
    if res["code"] == 0:
        print("消息推送成功")
    else:
        print(f"推送错误；{res}")


def send_email(title, msg, email=""):
    content = str(msg)
    # 163邮箱服务器地址
    email_conf = common.common_conf.get("message").get("email")
    mail_host = email_conf.get("mail_host")
    # 163用户名
    mail_user = email_conf.get("mail_user")
    # 密码(部分邮箱为授权码)
    mail_pass = email_conf.get("mail_pass")
    # 邮件发送方邮箱地址
    sender = email_conf.get("sender")
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = [common.common_conf.get("github").get("email")] if email == "" else [email]
    # 设置email信息
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = title
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]
    # 登录并发送邮件
    try:
        # 在阿里云上就要改为下面这种，本地和服务器都友好：
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        print('send email success')
    except smtplib.SMTPException as e:
        print('send email error', e)  # 打印错误


if __name__ == '__main__':
    # send_weixin("我的宝啊", "我想你!!!!!!!!!!!!!!")
    # send_qq("我的宝啊", "我想你!!!!!!!!!!!!!!")
    send_email("我的宝啊", {"a": 1})
