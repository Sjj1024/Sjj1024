import requests


def get_code():
    url = "https://tly.com/other/captcha.php?"
    payload = {}
    headers = {
        'authority': 'tly.com',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': '_ga=GA1.2.200343914.16801=6racb3hsoi5fpc7vr9vkdmjgd7; user_pwd=b1ab1bcd210c0db8d13a3b8a80533e181d1dc55ba3e9e; uid=203328; user_email=648133599%40qq.com; cf_clearance=dhHwfpa0j9UNE2s1Z.JP3zwQKnzhqzYPEexoAElE6hg-1683551332-0-150; _gid=GA1.2.153444678.1684141657; _gat=1; __cf_bm=CU.4Kjhi11.OoCUw2ARORaGBD1f5W7kLXT.VCLFXneA-1684141662-0-AbxB3/k/DaAivYijnAncyIVlbiqJIwqVQKk1+Y0l3CSKmgIXsqvRgcnbb3Rsjm0hhAhMuJUYV2S0PgDBmZFtA+TErrEeEmy/PIZkEGRIzuDM',
        'referer': 'https://tly.com/modules/index.php',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)


def signin_tly():
    url = "https://tly.com/modules/_checkin.php?captcha=bcz7"
    payload = {}
    headers = {
        'authority': 'tly.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': '_ga=GA1.2.200343914.1680155234; PHPSESSID=6racb3hsoi5fpc7vr9vkdmjgd7; user_pwd=b1ab1bcd210c0db8d13a3b8a80533e181d1dc55ba3e9e; uid=203328; user_email=648133599%40qq.com; _gid=GA1.2.153444678.1684141657; cf_chl_2=188aa92cca0fa4f; cf_clearance=wloN.ykeoH3kjbSqkA7fwjkeqsPKoZePUxxCtczvJUA-1684142171-0-150; _gat=1; __cf_bm=V9D4Dzm236r0capxTIEhQvd9sMJJXOrTMApeE5_aeKs-1684142221-0-AZeq888AdaA0UV2y+9/hLFKNf19a8p/jHagDyIo1b+cDZaZbP9J13BGSochwvp0LxigBVwQKNZMS/sYeilQDY7LrFfvvoq8Fs24/Rp9zRx5Z',
        'referer': 'https://tly.com/modules/index.php',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)


if __name__ == '__main__':
    get_code()
