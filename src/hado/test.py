# 导入节点检索模块
import time
from ascript.ios.node import Selector
from ascript.ios import system


def work_click():
    print("点击上下班按钮")
    btn = Selector().index(9).find()
    if btn:
        btn.click()
        time.sleep(2)


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
    # 仍要打卡
    first_btn = Selector().label("仍要打卡").find()
    if first_btn:
        first_btn.click()
        time.sleep(2)
    # 找到当前时间
    current_time = Selector().index(8).find()
    if current_time:
        time_str: str = current_time.value
        print(f"当前时间: {time_str}")
        if time_str.startswith("9"):
            work_click()
        elif time_str.startswith("21"):
            work_click()
        else:
            print("时间不匹配")
    # 点击返回到仍要打卡页面
    back_btn = Selector().name("gadget.navigationBarItem.backButton").find()
    if back_btn:
        back_btn.click()
        time.sleep(2)


def main():
    print("main")
    while True:
        control()
        print("开始睡眠20分钟")
        time.sleep(20 * 60)


main()
