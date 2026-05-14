# __init__.py 为初始入口文件,工程代码的入口文件.

# 导入动作库常用函数
from ascript.android.action import click,slide,Touch,gesture
# 导入控件检索相关
from ascript.android.node import Selector
# 导入图色相关
from ascript.android.screen import capture,FindColors,FindImages,Ocr
# 导入系统相关
from ascript.android import system
# 环境设备相关
from ascript.android.system import R,Device

print("Hello AS!")

# 根据包名启动,推荐使用
system.open("com.android.browser")


# for i in range(300):
