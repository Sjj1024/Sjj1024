import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def down_date(url: str):
    print(f"开始下载链接: {url}")
    # url = "https://h0.cn/20230513/yYmXp1xC/1000kb/hls/fJGlM1482095.ts"
    file_name = url.strip().split("/")[-1]
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'none',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("GET", url, headers=headers)
    with open(f"downloads/{file_name}", "wb") as f:
        f.write(response.content)
    return file_name


def down_control(links):
    # print("数据库中已经存在数据，就从已存在数据中随机copy...")
    executor = ThreadPoolExecutor(max_workers=50)
    task_list = []
    done_list = []
    print(f"所有子线程都在努力创造数据了")
    for link in links:
        # 添加到下载线程
        task_list.append(executor.submit(lambda cxp: down_date(*cxp), (link,)))
    for future in as_completed(task_list):
        file_name = future.result()
        done_list.append(file_name)
        print(f"下载进度: {len(done_list) / len(task_list) * 100}%  文件下载完成:{file_name}")
    print(f"所有任务已经添加完成！")


def read_link():
    with open("down.m3u8", "r+", encoding="utf-8") as f:
        content = f.read()
        link_list = content.split("\n\n")
        return link_list


def start_run():
    print("读取下载链接")
    down_list = read_link()
    down_control(down_list)
    # down_date("")


if __name__ == '__main__':
    start_run()
