"""
执行定时任务获取回家地址，并同步到各端
"""
import base64
from datetime import datetime
import json
from github import Github
from src.homes.hotbox import hot_urls
from src.homes.url_list import cate_list


def get_hot_urls():
    print("获取热门推荐地址")
    return hot_urls


def get_cate_list():
    hot_list = get_hot_urls()
    cate_list["hotbox"] = hot_list
    return cate_list


def read_daohang_html(template):
    with open(f"replace_html/{template}", "r", encoding="utf-8") as f:
        return f.read()


# 将热门推荐保存为html页面让android使用
def url_to_android_html(more_info):
    # 先将热门导航里面的内容通过模板写入到daohang.html中
    """
      <div class="tabBox">
        <h3 class="tabTitle">热门推荐</h3>
        <div class="aBox">
          <a href="https://www.baidu.com/" class="alink" target="_blank">百度一下</a>
        </div>
      </div>
    """
    # 提示的内容
    guide_div_str = f"""<div class="guide-time">{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</div>"""
    tips_div_str = f"""<div class="tips">{more_info}</div>"""
    tab_box_list = [guide_div_str, tips_div_str]
    cate_lists = get_cate_list()
    for key, val in cate_lists.items():
        # print(f"{key} : {val}")
        title = val["title"]
        data_url = val["data"]
        a_box_list = []
        for url_a in data_url:
            a_template = f"""<a href="{url_a["url"]}" class="alink" target="_blank">{url_a["title"]}</a>\n"""
            a_box_list.append(a_template)
        a_box_strs = "".join(a_box_list)
        tab_box_template = f"""<div class="tabBox">
            <h3 class="tabTitle">{title}</h3>
            <div class="aBox">
              {a_box_strs}
            </div>
          </div>"""
        tab_box_list.append(tab_box_template)
    tab_box_strs = "".join(tab_box_list)
    daohang_html = read_daohang_html("daohang_app_template.html")
    daohang_html_res = daohang_html.replace("templatePalace", tab_box_strs)
    with open("release_html/daohang_app_releases.html", "w", encoding="utf-8") as f:
        f.write(daohang_html_res)
    return daohang_html_res


# 从热门推荐里面能获取指定的url
def get_home_from_urls(key):
    cate_lists = get_cate_list()
    hot_homes = cate_lists.get("hotbox").get("data")
    for home in hot_homes:
        if home.get("title") == key:
            return home.get("url")
    raise Exception(f"没有找到对应的地址:{key}")


# 安卓app页面里面替换指定的网页内容
def cao_app_exe_page(html_path):
    with open(f"replace_html/{html_path}", "r", encoding="utf-8") as f:
        content_html = f.read()
        content_html = content_html.replace("""<html>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<body>""", "")
        content_html = content_html.replace("""</body>
</html>""", "")
        return content_html


def get_app_files():
    print("生成安卓app配置")
    """
    三个地址:
    github:https://api.github.com/repos/Sjj1024/Sjj1024/contents/.github/hubsql/appHuijia.txt
    博客园:https://www.cnblogs.com/sdfasdf/p/16965757.html
    CSDN:https://xiaoshen.blog.csdn.net/article/details/129345827
    """
    app_info = {
        "name": "Android1024",
        "version": 3.1,
        "update": True,
        "file_path": ".github/hubsql/appHuijia.txt",
        "upcontent": "增加了JavBus和2048地址，修复91论坛地址获取失败问题。升级有问题请加QQ/微信：2950525265",
        "upurl": "https://www.cnblogs.com/sdfasdf/p/16965757.html",
        "showmessage": False,
        "message": "这是最新版本，增加了返回按钮",
        "message_url": "",
        "interval": 10,  # 刷贡献的时间间隔/每多少小时刷一次
        "brush_rate": 100,  # 刷贡献的百分比，越大越容易触发刷
        "brush_all": True,  # 是否全部刷，只要是headers里面的，就都刷？
        # 分享的内容
        "more_urls": "1024回家APP：https://wwd.lanzoue.com/iQeC00912epc，\n浏览器插件：https://wwd.lanzoue.com/iQeC00912epc",
        # 更多推荐页面
        "more_html": url_to_android_html(
            """<span style="color: red;">提示: 部分网站可能需要VPN翻墙后访问，APP版</span>"""),
        "headers": "/index.php?u=628155&ext=9a511;/index.php?u=52993&ext=99ea2;/index.php?u=595394&ext=c180e;/index.php?u=384581&ext=26585;/index.php?u=627793&ext=09126",
        "about": f"""
         1.如果你想感谢我，请合理给我打赏吧，<br>我的比特币账户：<span style="padding: 0 5px 0 2px;word-wrap: break-word;">3HJTSzf2GL7Bj8r7HakUNS1G9jauemk1Lt</span><br>我的以太坊账户：<span style="padding: 0 5px 0 2px;word-wrap: break-word;">0xb9061992ea948e247a4542209c14c5e7ea79afc6</span><br>
         2.1024回家浏览器拓展插件：支持谷歌Chrome、Microsoft Edge、360浏览器、
         星愿浏览器、小白浏览器、遨游、搜狗极速、等等基于Chromium内核的浏览器：
         <a href="https://wwlu.lanzoum.com/iUhPX0p8fm6h" style="text-decoration: none;" > </a><br>
         3.1024回家Windows桌面端：待发布<a href="https://wwlu.lanzoum.com/iUhPX0p8fm6h" style="text-decoration: none;" > </a><br>
         4.1024回家Macbook桌面端：开发中...<a href="https://wwlu.lanzoum.com/iUhPX0p8fm6h" style="text-decoration: none;" > </a><br>
         5.不要用UC/夸克等垃圾国产浏览器，不然你会发现很多网站都会被屏蔽，并且监听你的浏览信息，非常可拍！<br>
         6.本APP永久停止更新！愿你安好！
        """,
        "header_ms": "这里总有你想看的吧",  # 这是app菜单栏头部
        "header_url": "",  # 点击头部显示的跳转
        "caoliu_url1": get_home_from_urls("1024草榴1"),  # 草榴免翻地址
        "caoliu_url2": get_home_from_urls("1024草榴2"),  # 草榴免翻地址
        "caoliu_url3": get_home_from_urls("1024草榴3"),  # 草榴免翻地址
        "article_ad": "",
        "commit_ad": "",  # 草榴评论区广告，支持html
        # 注册页面中，需要邀请码的提示语，为空则什么都不提示
        "mazinote": "",
        "porn_video_app": "https://its.better2021app.com",  # 91视频地址
        "porn_video_url": get_home_from_urls("91Pr视频1"),  # 91视频地址
        "porn_video_1ad": "",
        "porn_video_2ad": "",
        "porn_video_3ad": "",
        "porn_video_4ad": "",
        "porn_video_5ad": "",
        "porn_video_6ad": "",
        "porn_video_footer": "",
        "porn_image_url": get_home_from_urls("91Pr图片"),  # 91图片区地址
        "porn_photo_header": "",
        "porn_photo_header2": "",
        "porn_photo_footer": "",
        "porn_photo_wentou": "",
        "porn_vip_page": cao_app_exe_page("porn_vip_page.html"),
        "heiliao_url1": get_home_from_urls("黑料B打烊1"),  # 黑料免翻地址
        "heiliao_url2": get_home_from_urls("黑料B打烊2"),  # 黑料免翻地址
        "heiliao_url3": get_home_from_urls("黑料B打烊3"),  # 黑料免翻地址
        "heiliao_header": "",
        "heiliao_footer": "",
        "heiliao_artical": "",
        "sehuatang1": get_home_from_urls("98色花堂1"),
        "sehuatang2": get_home_from_urls("98色花堂2"),
        "sehuatang3": get_home_from_urls("98色花堂3"),
        "javbus1": get_home_from_urls("JavBus网1"),
        "javbus2": get_home_from_urls("JavBus网2"),
        "javbus3": get_home_from_urls("JavBus网3"),
        "luntan20481": get_home_from_urls("2048地址1"),
        "luntan20482": get_home_from_urls("2048地址2"),
        "luntan20483": get_home_from_urls("2048地址3")
    }
    return app_info


def get_iphone_files():
    print("生成iphone配置")
    return {
        "name": "Chrome1024",
        "file_path": ".github/hubsql/iphoneHuijia.txt", }


def get_chrome_files():
    print("生成chrome配置")
    return {
        "name": "Chrome1024",
        "file_path": ".github/hubsql/chromeHuijia.txt", }


def get_desktop_files():
    print("生成desktop配置")
    return {
        "name": "Chrome1024",
        "file_path": ".github/hubsql/desktopHuijia.txt", }


def encode_json(info):
    print("将各端配置编码")
    jsonStr = json.dumps(info)
    b_encode = base64.b64encode(jsonStr.encode("utf-8"))
    bs64_str = b_encode.decode("utf-8")
    realContent = f"VkdWxlIGV4cHJlc3Npb25z{bs64_str}VkdWxlIGV4cHJlc3Npb25z"
    # print(f"加密结果:\n{realContent}")
    print(f"博客园加密：")
    print(f"""
    <div style="display: none">{realContent}</div>
    """)
    return realContent


def save_encode_content_html(app_type, content):
    with open("./replace_html/encode_content_template.html", "r", encoding="utf-8") as f:
        template = f.read()
        content_html = template.replace("encodeContent", content)
        with open(f"release_html/boke_content_{app_type}.html", "w", encoding="utf-8") as res:
            res.write(content_html)


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


def run():
    print("开始获取地址")
    # 组装各端配置信息
    app_file = get_app_files()
    iphone_file = get_iphone_files()
    chrome_file = get_chrome_files()
    desktop_file = get_desktop_files()
    # 生成加密内容分发到git
    for app in [app_file, iphone_file, chrome_file, desktop_file]:
        file_path = app.get("file_path")
        print(f"原始信息:{app}")
        content = encode_json(app)
        name = app.get("name")
        print(f"{name} 加密后的数据是: {content}")
        save_encode_content_html(name, content)
        put_github_file(file_path, content)
    # 生成html内容存储到git


if __name__ == '__main__':
    GIT_REPO = "1024dasehn/huijia"
    GIT_TOKEN = "ghp_888LSkJC7DbB8pgMw6mynhQGLienoPv4P0pOLZ0".replace("888", "")
    g = Github(GIT_TOKEN)
    repo = g.get_repo(GIT_REPO)
    run()
