# 导入节点检索模块
import time
import datetime
from ascript.ios.node import Selector
from ascript.ios import system
from ascript.ios import action


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
                time.sleep(2)
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


def work_click():
    print("点击上班按钮")
    if find_and_click("上班打卡"):
        time.sleep(2)


def down_click():
    print("点击下班按钮")
    if find_and_click("下班打卡"):
        time.sleep(4)
        signle_v2free()


def click_btn():
    # 找到当前时间
    morn_time = Selector().index(6).find()
    off_time = Selector().index(9).find()
    if morn_time and morn_time.value:
        start_str: str = morn_time.value
        # morn_time 08:42:49
        print("morn_time", start_str, len(start_str))
        if start_str and start_str.startswith("09") and len(start_str) == 8:
            minute_str = int(start_str[3:5])
            if minute_str > 30:
                work_click()
        else:
            print("不到早上打卡时间")
    else:
        print("no more time")
    if off_time and off_time.value:
        off_str: str = off_time.value
        print("off_time", off_str, len(off_str))
        if off_str and off_str.startswith("21") and len(off_str) == 8:
            minute_str = int(off_str[3:5])
            if minute_str > 30:
                down_click()
        else:
            print("不到下班打卡时间")
    else:
        print("no off_time")


def control():
    # 关闭系统升级的按钮
    close_btn = Selector().label("关闭").find()
    if close_btn:
        close_btn.click()
        time.sleep(2)
    # 启动飞书
    # com.bytedance.ee.lark
    # 根据包名启动,推荐使用
    system.app_start(bundle_id="com.bytedance.ee.lark")
    time.sleep(2)
    # 点开假勤
    if find_and_click("假勤"):
        print("点击了假勤")
        time.sleep(2)
    # 仍要打卡
    if find_and_click("仍要打卡"):
        time.sleep(2)
    try:
        click_btn()
    except Exception as e:
        print("click error", e)
    # 点击返回到仍要打卡页面
    print("返回到打卡页面")
    back_btn = Selector().name("gadget.navigationBarItem.backButton").find()
    if back_btn:
        back_btn.click()
        time.sleep(2)
    print("返回到主界面....")


def signle_v2free():
    system.open_url("https://w1.v2free.cc/user")
    time.sleep(6)
    wait_label("知道了")
    time.sleep(3)
    # 滑动显示签到
    action.slide(15, 655, 15, 311)
    time.sleep(3)
    # 点击签到
    single_btn = Selector().xpath("//*[@name='check  点我签到获取流量']").find()
    if single_btn:
        print("点我获取流量")
        single_btn.click()
        wait_label("知道了")
    else:
        print("没有找到点我获取流量")
    time.sleep(6)
    system.app_start(bundle_id="com.bytedance.ee.lark")


def main():
    print("main")
    system.app_start(bundle_id="com.bytedance.ee.lark")
    time.sleep(2)
    # time_str = Selector().label("下班打卡").brother(1).find()
    """
    2025-02-21 08:42:46: main
    2025-02-21 08:42:49: morn_time 08:42:49
    2025-02-21 08:42:49: off_time 已进入打卡范围: HADO
    """
    # print(time_str.value)
    while True:
        # 获取今天的日期
        today = datetime.datetime.today()
        # 判断今天是否是工作日（周一到周五是工作日）
        if today.weekday() < 5:  # weekday()返回0（周一）到6（周日）
            print("是")
            control()
        else:
            print("不是")
        print("开始睡眠20分钟")
        time.sleep(6 * 60)


main()
