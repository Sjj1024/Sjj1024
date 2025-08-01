from src.signin.bilibili.bilibili import BiliBili
from src.signin.bilibili.config import config
from src.utils.sendMsg.sendWx import send_weixin, send_email
import src.common.index as common


def main():
    print(f"开始执行哔哩哔哩签到------------------------------")
    together = config.get("together")
    account = config.get("account")
    msg_list = []
    for one in account:
        options = one.get("options")
        push = one.get("push")
        email = one.get("email")
        bilibili = BiliBili(one["cookie"])
        res = bilibili.start(options)
        if push and together and push == "email":
            msg_list.append(res)
        elif push and push == "email":
            send_email("哔哩哔哩签到", res, email)
    if together:
        common.common_msg["哔哩哔哩"] = msg_list


# main()
# 
# if __name__ == "__main__":
#     main()
