import base64
import json
import requests
import random


def update_file():
    print(f"开始更新文件内容")
    # 产生一个随机内容
    num_ran = random.randint(123, 13232523523)
    print(num_ran)
    import requests
    url = "https://api.github.com/repos/Sjj1024/Sjj1024/contents/.github/hidden/config.txt"
    payload = {
        "message": "update from automan",
        "content": str(base64.b64encode(f"{num_ran}".encode("utf-8")), "utf-8"),
        "sha": get_file_sha()
    }
    payload = json.dumps(payload)
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {"ghp_888grzs67MqxbZUH3wmIFKzecaKB0cTLy3ICBkl".replace("888", "")}',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'text/plain'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.text)


def get_file_sha():
    url = "https://api.github.com/repos/Sjj1024/Sjj1024/contents/.github/hidden/config.txt"
    payload = {}
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {"ghp_888grzs67MqxbZUH3wmIFKzecaKB0cTLy3ICBkl".replace("888", "")}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return response.json().get("sha")


def run():
    print("创造贡献...")
    # 产生一个随机数，然后判断是否发送请求
    num = random.randint(0, 100)
    if num > 70:
        print("开始发送请求")
        update_file()


if __name__ == '__main__':
    # run()
    update_file()
