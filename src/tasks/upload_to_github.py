import base64
import json
import requests


def read_file(file_path):
    with open(file_path, "rb+") as f:
        return f.read()


def add_file(path, content, message):
    url = f"https://api.github.com/repos/Sjj1024/CvReport/contents/img/{path}"
    headers = {"Authorization": "Bearer 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",
               'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    base64_content = base64.b64encode(content).decode('utf-8')
    # print(base64_content)
    payload = json.dumps({
        "message": message,
        "branch": "gh-pages",
        "content": base64_content
    })
    print("开始推送文件....")
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.text)


if __name__ == '__main__':
    file = read_file(r"E:\Dpandata\Myproject\Sjj1024\src\tasks\meizi.mp4")
    add_file("meizi.mp4", file, "添加超过25M的apk文件")