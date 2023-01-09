import os
import sys
import time


def test1():
    print("HEELO WORLD")


if __name__ == '__main__':
    test1()
    time.sleep(3)
    print('程序重启...')
    # 获取当前解释器路径
    p = sys.executable
    # 启动新程序(解释器路径, 当前程序)
    os.execl(p, p, *sys.argv)
    # 关闭当前程序
    sys.exit()

