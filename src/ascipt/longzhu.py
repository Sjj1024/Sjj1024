# __init__.py 为初始入口文件,工程代码的入口文件.
import time

# 导入动作库常用函数
from ascript.android.action import click, slide, Touch, gesture
# 导入控件检索相关
from ascript.android.node import Selector
# 导入图色相关
from ascript.android.screen import capture, FindColors, FindImages, Ocr
# 导入系统相关
from ascript.android import system
# 环境设备相关
from ascript.android.system import R, Device

from ascript.android import action

print("Hello AS!")


# 根据包名启动,推荐使用
# system.open("com.android.browser")


def next_click(text):
    downBtn = Selector(0).id("next").desc(text).find()
    if downBtn:
        downBtn.click()
    else:
        print(f"没有找到:{text}")
    time.sleep(1)


def down_click(text):
    downBtn = Selector(0).text(text).find()
    if downBtn:
        downBtn.click()
    else:
        print(f"没有找到:{text}")
    time.sleep(1)


def desc_click(text):
    downBtn = Selector(0).desc(text).find()
    if downBtn:
        downBtn.click()
    else:
        print(f"没有找到:{text}")
        down_click("页面全屏")
    time.sleep(1)


def x_y_click(x, y):
    know_btn = Selector().x(x).y(y).find()
    if know_btn:
        know_btn.click()
    else:
        print("没找到xy")
    time.sleep(2)


for i in range(300):
    next_click("下一集")

    desc_click("下载视频")

    down_click("立即下载")

    time.sleep(2)
