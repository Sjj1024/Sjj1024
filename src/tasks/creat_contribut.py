import requests
import random


def update_file():
    print(f"开始更新文件内容")
    # 产生一个随机内容
    num_ran = random.randint(123, 13232523523)
    print(num_ran)


def run():
    print("创造贡献...")
    # 产生一个随机数，然后判断是否发送请求
    num = random.randint(0, 10)
    if num > 3:
        print("开始发送请求")
        update_file()


if __name__ == '__main__':
    run()
