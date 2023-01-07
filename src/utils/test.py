import requests
from urllib import parse
import smtplib
from email.mime.text import MIMEText
import src.common.index as common


def send_html_email(title, json: dict, email="648133599@qq.com"):
    # 163邮箱服务器地址
    mail_host = "smtp.163.com"
    # 163用户名
    mail_user = "lanxingsjj@163.com"
    # 密码(部分邮箱为授权码)
    mail_pass = "QULRMYHTUVMHYVGM"
    # 邮件发送方邮箱地址
    sender = "lanxingsjj@163.com"
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = [common.common_conf.get("github").get("email")] if email == "" else [email]
    # 邮件内容设置
    content = ""
    for (key, val) in json.items():
        content += f"""
        <h1>{key}</h1>
          <p style="color: red;">{val}</p>
        """
    message = MIMEText(content, _subtype="html", _charset="utf-8")
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
    send_html_email("html", "85")
