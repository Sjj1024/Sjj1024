from github import Github
import os
import py_compile

def put_github_file(path, content, commit=""):
    print("判断文件是否存在，存在就更新，不存在就增加")
    try:
        res = repo.get_contents(path)
        res = repo.update_file(path, "更新插件内容", content, res.sha)
        print(f"更新文件结果:{res}")
    except Exception:
        print("文件不存在,开始创建...")
        res = repo.create_file(path, "添加一个新文件", content)
        print(res)


def recursive_dir(path, f, file_list):
    """
    递归获取文件夹中所有的文件
    :param path:根目录
    :param f:子目录
    :param file_list:文件列表
    :return:
    """
    print(f"{path}/{f}")
    file_names = os.listdir(os.path.join(path, f))
    for file in file_names:
        if f.startswith("."):
            newDir = path + '/' + f + '/' + file
        else:
            newDir = path + '/' + f.split(".")[-1] + '/' + file
        if os.path.isfile(newDir):
            if "pycache" not in f and "pycache" not in file:
                py_file = newDir.split("homes//")[1]
                file_list.append(py_file)
        else:
            if "__pycache__" not in file:
                fi = "/".join(newDir.split("/")[0:-1])
                fl = newDir.split("/")[-1]
                if "." in fl:
                    print(fl)
                recursive_dir(fi, fl, file_list)


def run():
    print("同步此文件夹中的内容到git")
    # 将home_task编译加密
    py_compile.compile(r'home_task.py', "home_task.pyc")
    home_files = []
    recursive_dir(os.getcwd(), "", home_files)
    print(home_files)
    for app in home_files:
        print(app)
        if "pyc" in app:
            # 同步到github上
            with open(app, "rb") as f:
                put_github_file(app, f.read())
        elif app not in ["sync_files.py", "home_task.py"]:
            with open(app, "r", encoding="utf-8") as f:
                put_github_file(app, f.read())
        else:
            print("python原文件不进行同步")


"""
生成pyc文件
python -m py_compile home_task.py
"""
if __name__ == '__main__':
    GIT_REPO = "1024dasehn/GoHome"
    GIT_TOKEN = "ghp_888LSkJC7DbB8pgMw6mynhQGLienoPv4P0pOLZ0".replace("888", "")
    g = Github(GIT_TOKEN)
    repo = g.get_repo(GIT_REPO)
    run()
