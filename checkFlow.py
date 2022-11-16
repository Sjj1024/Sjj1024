import datetime
import os

import requests
import json


def print_current():
    print("当前时间是", datetime.datetime.now())


def sing_in():
    print(os.getcwd())


if __name__ == '__main__':
    print_current()
    sing_in()
