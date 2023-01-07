import datetime
import os
import json
import src.common.index as common
from src.utils.sendMsg.sendWx import send_email, send_html_email


def load_conf():
    try:
        conf = os.environ.get("CONFIGER")
        conf_obj = json.loads(conf)
        common.common_conf = conf_obj
        print(f"加载配置成功！")
    except Exception as e:
        send_email(f"加载配置异常", f"加载配置失败: {e}")


def load_model(file):
    module_name = ''
    if len(file) > 3 and (file[-3:] == '.py' or file[-4:] == '.pyc'):
        if file[-3:] == '.py':
            module_name = file[:-3]
        if file[-4:] == '.pyc':
            module_name = file[:-4]
    print(f"开始执行任务:{module_name}")
    try:
        __import__(module_name)
    except Exception as e:
        print(f"加载模块{module_name}失败: {e}")
        send_email(f"加载模块{module_name}异常", f"加载模块{module_name}失败: {e}")


def recursive_dir(path, f, file_list):
    """
    递归获取文件夹中所有的文件
    :param path:根目录
    :param f:子目录
    :param file_list:文件列表
    :return:
    """
    file_names = os.listdir(os.path.join(path, f))  # 获取当前路径下的文件名，返回List
    for file in file_names:
        newDir = path + '/' + f + '/' + file  # 将文件命加入到当前文件路径后面
        if os.path.isfile(newDir):  # 如果是文件
            if "pycache" not in f and "pycache" not in file:
                module_file = "src" + newDir.split("src")[1].replace("/", ".")
                if module_file.find("index") != -1:
                    file_list.append(module_file)
        else:
            if file not in ["__pycache__", "tasks", "utils", "common"]:
                recursive_dir("/".join(newDir.split("/")[0:-1]), newDir.split("/")[-1], file_list)  # 如果不是文件，递归这个文件夹的路径


def run():
    print("当前时间是", datetime.datetime.now())
    load_conf()
    app_files = []
    recursive_dir(os.getcwd(), "src", app_files)
    print(f"注入的任务列表是:{app_files}")
    for app in app_files:
        if app.endswith(".py"):
            load_model(app)
    print(f"定时签到结果：{common.common_msg}")
    # send_email(f"定时签到{datetime.datetime.now()}", common.common_msg)
    send_html_email(f"定时签到{datetime.datetime.now()}", common.common_msg)


if __name__ == '__main__':
    run()
