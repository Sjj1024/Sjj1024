import datetime
import os


def print_current():
    print("当前时间是", datetime.datetime.now())


def load_model(file, init_params=None):
    module_name = ''
    if len(file) > 3 and (file[-3:] == '.py' or file[-4:] == '.pyc'):
        if file[-3:] == '.py':
            module_name = file[:-3]
        if file[-4:] == '.pyc':
            module_name = file[:-4]
    print(f"开始执行任务:{module_name}")
    __import__(module_name)


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
                file_list.append(f"{f}.{file}")
        else:
            if "__pycache__" not in file:
                recursive_dir("/".join(newDir.split("/")[0:-1]), newDir.split("/")[-1], file_list)  # 如果不是文件，递归这个文件夹的路径


def sing_in():
    app_files = []
    recursive_dir(os.getcwd(), "tasks", app_files)
    print(f"注入的任务列表是:{app_files}")
    for app in app_files:
        if app.endswith(".py"):
            load_model(app)


if __name__ == '__main__':
    print_current()
    sing_in()
