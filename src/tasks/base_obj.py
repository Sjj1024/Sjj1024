import smtplib
from email.mime.text import MIMEText


class BaseMessage(object):

    def __init__(self):
        self.name = "基础的发送email对象"

    def send_email(self, title, msg, email="648133599@qq.com"):
        content = str(msg)
        # 163邮箱服务器地址
        mail_host = "smtp.163.com"
        # 163用户名
        mail_user = "lanxingsjj@163.com"
        # 密码(部分邮箱为授权码)
        mail_pass = ""
        # 邮件发送方邮箱地址
        sender = ""
        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = [email]
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
