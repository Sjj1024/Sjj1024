from src.signin.bilibili.bilibili import BiliBili
from src.signin.bilibili.config import config
from src.utils.sendMsg.sendWx import send_weixin, send_email


def main():
    print(f"开始执行哔哩哔哩签到...")
    together = config.get("together")
    account = config.get("account")
    msg_list = []
    email = ""
    for one in account:
        options = one.get("options")
        push = one.get("push")
        email = one.get("email")
        bilibili = BiliBili(one["cookie"])
        res = bilibili.start(options)
        if push and together and push == "email":
            msg_list.append(res)
        elif push and push == "email":
            send_email(email, "哔哩哔哩签到", res)
    if together:
        send_email(email, "哔哩哔哩签到", msg_list)


main()

if __name__ == "__main__":
    main()
