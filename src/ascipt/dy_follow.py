from ascript.ios.node import Selector
from ascript.ios import system
import time


# 找到按钮并点击
def find_and_click(label: str):
    count = 0
    while True:
        print(f"等待label:{label}....")
        know_btn = Selector().xpath(f"//*[@name='{label}']").find()
        if count < 3:
            count += 1
            if know_btn:
                know_btn.click()
                time.sleep(3)
                return True
        else:
            return False


def index_and_click(index: int):
    count = 0
    while True:
        print(f"等待index:{index}....")
        know_btn = Selector().index(index).find()
        if count < 3:
            count += 1
            if know_btn:
                print("找到了:", index)
                know_btn.click()
                time.sleep(2)
                return True
        else:
            print("没有找到:", index)
            return False


def xy_and_click(x: int, y: int):
    count = 0
    while True:
        print(f"等待xy:{x}{y}....")
        know_btn = Selector().x(x).y(y).find()
        if count < 3:
            count += 1
            if know_btn:
                print("找到了xy: ", x, y)
                know_btn.click()
                time.sleep(2)
                return True
        else:
            print("没有找xy:", x, y)
            return False


def count_func(key):
    print("统计次数")
    global total_count
    global count_dict
    if count_dict.get("title") == key:
        print("不统计")
    else:
        print("统计一次")
        count_dict["title"] = key
        total_count += 1


def wait_label(label):
    while True:
        print(f"等待:{label}....")
        know_btn = Selector().xpath(f"//*[@name='{label}']").find()
        if know_btn:
            know_btn.click()
            break
        else:
            time.sleep(3)


def click_unfollow():
    """
    点击取消关注
    """
    res = find_and_click("互相关注")
    if res:
        res = find_and_click("取消关注")
        if res:
            print("取消关注成功")
        else:
            print("取消关注失败")
    else:
        print("没找到互相关注按钮")


def single_click():
    all_user = Selector().xpath(f"//*[@name='互相关注']").find_all()
    print(f"找到{len(all_user)}个互相关注按钮")
    if all_user and len(all_user) > 1:
        for i in range(len(all_user)):
            print(f"取消关注第{i + 1}个用户")
            if i <= 0 or i >= 8:
                continue
            all_user[i].click()
            time.sleep(2)
            res = find_and_click("取消关注")
            if res:
                print("取消关注成功")
            else:
                print("取消关注失败")
            know_btn = Selector().xpath(f"//*[@name='我知道了']").find()
            if know_btn:
                know_btn.click()
                print("点击我知道了")
            time.sleep(2)
    else:
        print("没有找到互相关注")


def main():
    system.app_start(bundle_id="com.ss.iphone.ugc.Aweme")
    time.sleep(2)
    while True:
        Selector().scroll("down", 1).find()
        single_click()
        time.sleep(2)


main()
