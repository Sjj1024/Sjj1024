import os
import json
import requests
from urllib.parse import urlparse

HAR_FILE = "cocos-games.fir.show.har"
FILTER_DOMAIN = "cocos-games.fir.show"
OUTPUT_DIR = "bitexiaodui"


def load_har_file(har_path):
    with open(har_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_urls(har_data, filter_domain=None):
    urls = []
    entries = har_data.get("log", {}).get("entries", [])
    for e in entries:
        req = e.get("request", {})
        url = req.get("url")
        if not url:
            continue
        if url.startswith("http"):
            if filter_domain:
                if filter_domain in urlparse(url).netloc:
                    urls.append(url)
            else:
                urls.append(url)
    # 去重保序
    seen, unique_urls = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique_urls.append(u)
    return unique_urls


def download_file(url, base_output):
    try:
        parsed = urlparse(url)
        path = parsed.path.lstrip("/")
        if not path:
            path = "index.html"
        save_path = os.path.join(base_output, path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"✅ 下载成功: {url}")
    except Exception as e:
        print(f"❌ 下载失败: {url} ({e})")


def main():
    if not os.path.exists(HAR_FILE):
        print(f"❌ 未找到 {HAR_FILE}，请放在当前目录下")
        return
    print(f"📖 正在读取 {HAR_FILE} ...")
    har_data = load_har_file(HAR_FILE)

    print("🔍 提取资源链接中 ...")
    urls = extract_urls(har_data, filter_domain=FILTER_DOMAIN)

    if not urls:
        print("❌ 未提取到任何有效资源链接。")
        return

    print(f"共提取到 {len(urls)} 个资源，开始下载 ...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for url in urls:
        download_file(url, OUTPUT_DIR)

    print("\n🎯 下载完成！请运行以下命令启动本地服务器：")
    print(f"cd {OUTPUT_DIR} && python3 -m http.server 8080")


if __name__ == "__main__":
    main()
