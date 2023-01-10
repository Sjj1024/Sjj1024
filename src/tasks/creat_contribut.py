import requests
import random


def update_file():
    print(f"开始更新文件内容")
    # 产生一个随机内容
    num_ran = random.randint(123, 13232523523)
    print(num_ran)
    import requests
    url = "https://api.github.com/repos/Sjj1024/Sjj1024/contents/tasks/blog/hello.txt"
    payload = "{\r\n  \"message\": \"update from INSOMNIA\",\r\n  \"content\": \"Y3JlYXRlIGZpbGUgZnJvbSBJTlNPTU5JQQoK5oiR54ix5L2g54ix\",\r\n  \"sha\":\"57642f5283c98f6ffa75d65e2bf49d05042b4a6d\"\r\n}"
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer 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',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'text/plain'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.text)


def run():
    print("创造贡献...")
    # 产生一个随机数，然后判断是否发送请求
    num = random.randint(0, 10)
    if num > 3:
        print("开始发送请求")
        update_file()


if __name__ == '__main__':
    run()
