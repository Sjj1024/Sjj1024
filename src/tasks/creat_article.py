import requests
import json
import re


def make_one(title):
    print(f"创造文章-----{title}")
    url = "https://i.cnblogs.com/api/posts"
    payload = json.dumps({
        "id": None,
        "postType": 1,
        "accessPermission": 0,
        "title": title,
        "url": None,
        "postBody": "<h3 id=\"override-the-entrypoint-of-an-image\">Override the entrypoint of an image</h3>\n<div class=\"introduced-in\">\n<p>Introduced in GitLab and GitLab Runner 9.4. Read more about the&nbsp;<a href=\"https://docs.gitlab.com/ee/ci/docker/using_docker_images.html#extended-docker-configuration-options\">extended configuration options</a>.</p>\n</div>\n<p>Before explaining the available entrypoint override methods, let&rsquo;s describe how the runner starts. It uses a Docker image for the containers used in the CI/CD jobs:</p>\n<ol>\n<li>The runner starts a Docker container using the defined entrypoint. The default from&nbsp;<code class=\"highlighter-rouge\">Dockerfile</code>&nbsp;that may be overridden in the&nbsp;<code class=\"highlighter-rouge\">.gitlab-ci.yml</code>&nbsp;file.</li>\n<li>The runner attaches itself to a running container.</li>\n<li>The runner prepares a script (the combination of&nbsp;<a href=\"https://docs.gitlab.com/ee/ci/yaml/index.html#before_script\"><code class=\"highlighter-rouge\">before_script</code></a>,&nbsp;<a href=\"https://docs.gitlab.com/ee/ci/yaml/index.html#script\"><code class=\"highlighter-rouge\">script</code></a>, and&nbsp;<a href=\"https://docs.gitlab.com/ee/ci/yaml/index.html#after_script\"><code class=\"highlighter-rouge\">after_script</code></a>).</li>\n<li>The runner sends the script to the container&rsquo;s shell&nbsp;<code class=\"highlighter-rouge\">stdin</code>&nbsp;and receives the output.</li>\n</ol>\n<p>To override the entrypoint of a Docker image, define an empty&nbsp;<code class=\"highlighter-rouge\">entrypoint</code>&nbsp;in the&nbsp;<code class=\"highlighter-rouge\">.gitlab-ci.yml</code>&nbsp;file, so the runner does not start a useless shell layer. However, that does not work for all Docker versions.</p>\n<ul>\n<li>For Docker 17.06 and later, the&nbsp;<code class=\"highlighter-rouge\">entrypoint</code>&nbsp;can be set to an empty value.</li>\n<li>For Docker 17.03 and earlier, the&nbsp;<code class=\"highlighter-rouge\">entrypoint</code>&nbsp;can be set to&nbsp;<code class=\"highlighter-rouge\">/bin/sh -c</code>,&nbsp;<code class=\"highlighter-rouge\">/bin/bash -c</code>, or an equivalent shell available in the image.</li>\n</ul>\n<p>The syntax of&nbsp;<code class=\"highlighter-rouge\">image:entrypoint</code>&nbsp;is similar to&nbsp;<a href=\"https://docs.docker.com/engine/reference/builder/#entrypoint\">Dockerfile&rsquo;s&nbsp;<code class=\"highlighter-rouge\">ENTRYPOINT</code></a>.</p>\n<p>Let&rsquo;s assume you have a&nbsp;<code class=\"highlighter-rouge\">super/sql:experimental</code>&nbsp;image with a SQL database in it. You want to use it as a base image for your job because you want to execute some tests with this database binary. Let&rsquo;s also assume that this image is configured with&nbsp;<code class=\"highlighter-rouge\">/usr/bin/super-sql run</code>&nbsp;as an entrypoint. When the container starts without additional options, it runs the database&rsquo;s process. The runner expects that the image has no entrypoint or that the entrypoint is prepared to start a shell command.</p>\n<p>With the extended Docker configuration options, instead of:</p>\n<ul>\n<li>Creating your own image based on&nbsp;<code class=\"highlighter-rouge\">super/sql:experimental</code>.</li>\n<li>Setting the&nbsp;<code class=\"highlighter-rouge\">ENTRYPOINT</code>&nbsp;to a shell.</li>\n<li>Using the new image in your CI job.</li>\n</ul>\n<p>You can now define an&nbsp;<code class=\"highlighter-rouge\">entrypoint</code>&nbsp;in the&nbsp;<code class=\"highlighter-rouge\">.gitlab-ci.yml</code>&nbsp;file.</p>\n<p>For Docker 17.06 and later:</p>\n<div class=\"language-yaml highlighter-rouge\">\n<div class=\"highlight\">\n<pre class=\"highlight\"><code><span class=\"na\">image<span class=\"pi\">:\n  <span class=\"na\">name<span class=\"pi\">: <span class=\"s\">super/sql:experimental\n  <span class=\"na\">entrypoint<span class=\"pi\">: <span class=\"pi\">[<span class=\"s2\">\"<span class=\"s\">\"<span class=\"pi\">]\n</span></span></span></span></span></span></span></span></span></span></span></code><button class=\"clip-btn\" title=\"Click to copy\" data-selector=\"true\"></button></pre>\n</div>\n</div>\n<p>For Docker 17.03 and earlier:</p>\n<div class=\"language-yaml highlighter-rouge\">\n<div class=\"highlight\">\n<pre class=\"highlight\"><code><span class=\"na\">image<span class=\"pi\">:\n  <span class=\"na\">name<span class=\"pi\">: <span class=\"s\">super/sql:experimental\n  <span class=\"na\">entrypoint<span class=\"pi\">: <span class=\"pi\">[<span class=\"s2\">\"<span class=\"s\">/bin/sh\"<span class=\"pi\">, <span class=\"s2\">\"<span class=\"s\">-c\"<span class=\"pi\">]\n</span></span></span></span></span></span></span></span></span></span></span></span></span></span></code><button class=\"clip-btn\" title=\"Click to copy\" data-selector=\"true\"></button></pre>\n</div>\n</div>\n<h2 id=\"define-image-and-services-in-configtoml\">Define image and services in&nbsp;<code class=\"highlighter-rouge\">config.toml</code></h2>\n<p>Look for the&nbsp;<code class=\"highlighter-rouge\">[runners.docker]</code>&nbsp;section:</p>\n<div class=\"language-toml highlighter-rouge\">\n<div class=\"highlight\">\n<pre class=\"highlight\"><code><span class=\"nn\">[runners.docker]\n  <span class=\"py\">image <span class=\"p\">= <span class=\"s\">\"ruby:latest\"\n  <span class=\"py\">services <span class=\"p\">= <span class=\"p\">[<span class=\"s\">\"mysql:latest\"<span class=\"p\">, <span class=\"s\">\"postgres:latest\"<span class=\"p\">]\n</span></span></span></span></span></span></span></span></span></span></span></code><button class=\"clip-btn\" title=\"Click to copy\" data-selector=\"true\"></button></pre>\n</div>\n</div>\n<p>The image and services defined this way are added to all jobs run by that runner.</p>\n<h2 id=\"access-an-image-from-a-private-container-registry\">Access an image from a private Container Registry</h2>\n<p>To access private container registries, the GitLab Runner process can use:</p>\n<ul>\n<li><a href=\"https://docs.gitlab.com/ee/ci/docker/using_docker_images.html#use-statically-defined-credentials\">Statically defined credentials</a>. That is, a username and password for a specific registry.</li>\n<li><a href=\"https://docs.gitlab.com/ee/ci/docker/using_docker_images.html#use-a-credentials-store\">Credentials Store</a>. For more information, see&nbsp;<a href=\"https://docs.docker.com/engine/reference/commandline/login/#credentials-store\">the relevant Docker documentation</a>.</li>\n<li><a href=\"https://docs.gitlab.com/ee/ci/docker/using_docker_images.html#use-credential-helpers\">Credential Helpers</a>. For more information, see&nbsp;<a href=\"https://docs.docker.com/engine/reference/commandline/login/#credential-helpers\">the relevant Docker documentation</a>.</li>\n</ul>\n<p>To define which option should be used, the runner process reads the configuration in this order:</p>\n<ul>\n<li>A&nbsp;<code class=\"highlighter-rouge\">DOCKER_AUTH_CONFIG</code>&nbsp;<a href=\"https://docs.gitlab.com/ee/ci/variables/index.html\">CI/CD variable</a>.</li>\n<li>A&nbsp;<code class=\"highlighter-rouge\">DOCKER_AUTH_CONFIG</code>&nbsp;environment variable set in the runner&rsquo;s&nbsp;<code class=\"highlighter-rouge\">config.toml</code>&nbsp;file.</li>\n<li>A&nbsp;<code class=\"highlighter-rouge\">config.json</code>&nbsp;file in&nbsp;<code class=\"highlighter-rouge\">$HOME/.docker</code>&nbsp;directory of the user running the process. If the&nbsp;<code class=\"highlighter-rouge\">--user</code>&nbsp;flag is provided to run the child processes as unprivileged user, the home directory of the main runner process user is used.</li>\n</ul>\n<h3 id=\"requirements-and-limitations\">Requirements and limitations</h3>\n<ul>\n<li>Available for&nbsp;<a href=\"https://docs.gitlab.com/runner/executors/kubernetes.html\">Kubernetes executor</a>&nbsp;in GitLab Runner 13.1 and later.</li>\n<li><a href=\"https://docs.gitlab.com/ee/ci/docker/using_docker_images.html#use-a-credentials-store\">Credentials Store</a>&nbsp;and&nbsp;<a href=\"https://docs.gitlab.com/ee/ci/docker/using_docker_images.html#use-credential-helpers\">Credential Helpers</a>&nbsp;require binaries to be added to the GitLab Runner&nbsp;<code class=\"highlighter-rouge\">$PATH</code>, and require access to do so. Therefore, these features are not available on shared runners, or any other runner where the user does not have access to the environment where the runner is installed.</li>\n</ul>\n<h3 id=\"use-statically-defined-credentials\">Use statically-defined credentials</h3>\n<p>There are two approaches that you can take to access a private registry. Both require setting the CI/CD variable&nbsp;<code class=\"highlighter-rouge\">DOCKER_AUTH_CONFIG</code>&nbsp;with appropriate authentication information.</p>\n<ol>\n<li>Per-job: To configure one job to access a private registry, add&nbsp;<code class=\"highlighter-rouge\">DOCKER_AUTH_CONFIG</code>&nbsp;as a&nbsp;<a href=\"https://docs.gitlab.com/ee/ci/variables/index.html\">CI/CD variable</a>.</li>\n<li>Per-runner: To configure a runner so all its jobs can access a private registry, add&nbsp;<code class=\"highlighter-rouge\">DOCKER_AUTH_CONFIG</code>&nbsp;as an environment variable in the runner&rsquo;s configuration.</li>\n</ol>",
        "categoryIds": None,
        "inSiteCandidate": False,
        "inSiteHome": False,
        "siteCategoryId": None,
        "blogTeamIds": None,
        "isPublished": True,
        "displayOnHomePage": True,
        "isAllowComments": True,
        "includeInMainSyndication": True,
        "isPinned": False,
        "isOnlyForRegisterUser": False,
        "isUpdateDateAdded": True,
        "entryName": None,
        "description": None,
        "featuredImage": None,
        "tags": None,
        "password": None,
        "datePublished": "2022-12-08T02:31:51.923Z",
        "dateUpdated": None,
        "isMarkdown": False,
        "isDraft": True,
        "autoDesc": None,
        "changePostType": False,
        "blogId": 0,
        "author": None,
        "removeScript": False,
        "clientInfo": None,
        "changeCreatedTime": False,
        "canChangeCreatedTime": False,
        "isContributeToImpressiveBugActivity": False,
        "usingEditorId": 3,
        "sourceUrl": None
    })
    headers = {
        'authority': 'i.cnblogs.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'content-type': 'application/json',
        'cookie': '_ga_4CQQXWHK3C=GS1.1.1665212127.1.0.1665212129.0.0.0; __gads=ID=2763fdfb38b78a7f:T=1665992538:S=ALNI_MZsqdsu-zwHXNqtj1iAX7gPUsIQUg; Hm_lvt_866c9be12d4a814454792b1fd0fed295=1668499414,1669620579; _gid=GA1.2.1505279721.1670205784; __gpi=UID=00000b7c3d2a241f:T=1668499414:RT=1670406430:S=ALNI_MYbiVsh3aVAUDc1rq9-vpo_Q8LsFg; .Cnblogs.AspNetCore.Cookies=CfDJ8NfDHj8mnYFAmPyhfXwJojezrfrJsX3HM9lJoXGRpeVJMH4mhx6vqZ6MO-qQrciUEqWT2ps4se94f4Y3CXbNpNRt91oMz3AOo0pftwJVDwsZ3Kv5GZt-cSWpqa6eoZVzv6lCyjVM-FZ_mDN88YifuLoPFGor-XBru3iaHHEwPHVMuMH_Q_wrkFdNBgki-417W8ocsfUoeO77MtwNrk56X0LeubpvWMf26YXLoHWGhoDoEw23R5guCTJLuZvbG-o2-1Qf5vNd6KjeR-jD5RY6hM-VtgUS0z9NT2omAwuiXyFvjdzrTSbPNJjluyU3Bl61ch-ay5WMHiACxBjXW6HxiUBomrdZ6OE8lNsux60JU3npyG3a4-YJ72aCmVCUruj-CZKgCKTLQ4CdZIfAqE873gkpWZTrrgayYlc9mTSaiM8Ne4CLxN21T1dLN2IhP6qKN61iO98XaxinjbrFsUONJXODv3xTMQBih24nnC9QbZbe-KUIDZALMXV1wPoHnZrya5B6kvkR66KxUkVDL_891oBjqfjA-GEXh46rJNFzMEB_mgNnlZc4-XBGJBB3TEvM5Q; .CNBlogsCookie=EA1644A0A4784C847AAC894A34D81D974B509B0BB9519935DDDA00615F89D962C906B4A9FA4544E8DC627127FDFE56808960560CCD20400D3467363A98348F42413DBEC4; _ga_3Q0DVSGN10=GS1.1.1670412268.1.1.1670412409.59.0.0; _ga=GA1.2.1521432481.1665209113; .AspNetCore.Antiforgery.b8-pDmTq1XM=CfDJ8NfDHj8mnYFAmPyhfXwJojcEg6ZR4WW6IV7OmazrjE6CyAF9zNgNrul8POIp7m0gNyZ2T4-l7euqwSnkChbawE-oiDMjwe-ySRMM_XKV4ywaSav-nFdPZ2RDYrNG04ZDPJ7PP1x0DsAlHv2vQPdK8zs; .AspNetCore.Session=CfDJ8NfDHj8mnYFAmPyhfXwJojdQaAEoIQBe9TwEuMBqXRhRP5cZ9uQSDONSUizAICSLBVBV%2B8uVSTHmC6GXHYEk9lO6iGbBn3iLLBj2Cdp65Or1MDaJGfcHZx%2BACwGj9LmuyF804MH4bX7UVKa0KrYVuScbjro9jfH5nw1GmPjxVikH; _gat_gtag_UA_476124_1=1; Hm_lpvt_866c9be12d4a814454792b1fd0fed295=1670412615; XSRF-TOKEN=CfDJ8NfDHj8mnYFAmPyhfXwJojfW1Uu5byxYvSwHLgo6mdI35XGO89qowMoA6SJI7MHCQyNVlov4n5p18YH7Y_9GFsFRjg0UTg2XBAmkNNCLoL6CGTFnmOk7pNzjYVqhWfh_jxY46ZCsoqWgCrxYF390MxcmUeaYp6s3Yo-uaSawp5X2YW6DMQD0xpIoPx36H3xB_Q; _gat_gtag_UA_48445196_1=1',
        'origin': 'https://i.cnblogs.com',
        'referer': 'https://i.cnblogs.com/posts/edit',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-xsrf-token': 'CfDJ8NfDHj8mnYFAmPyhfXwJojfW1Uu5byxYvSwHLgo6mdI35XGO89qowMoA6SJI7MHCQyNVlov4n5p18YH7Y_9GFsFRjg0UTg2XBAmkNNCLoL6CGTFnmOk7pNzjYVqhWfh_jxY46ZCsoqWgCrxYF390MxcmUeaYp6s3Yo-uaSawp5X2YW6DMQD0xpIoPx36H3xB_Q'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"创建文章结果：{response.json()}")


def get_content():
    content_list = ["https://docs.gitlab.com/ee/user/project/code_owners.html",
                    "https://docs.gitlab.com/ee/user/snippets.html",
                    "https://docs.gitlab.com/ee/user/project/repository/branches/",
                    "https://docs.gitlab.com/ee/user/project/repository/branches/default.html",
                    "https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html",
                    "https://docs.gitlab.com/ee/user/project/git_attributes.html"
                    ]


def get_example():
    print("获取文章标题")
    url = "https://blog.csdn.net/?spm=1000.2115.3001.4477"
    payload = {}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'uuid_tt_dd=10_19616795140-1665200689671-367015; __gads=ID=d06c9a6acbfc1de7-2220d55ea4d70068:T=1665200691:RT=1665200691:S=ALNI_Mbu5JkrC1adgb9kBV62ZZpxg4gdQg; UserName=weixin_44786530; UserInfo=3e9da6fdfcef4018b71fb7dd299b9661; UserToken=3e9da6fdfcef4018b71fb7dd299b9661; UserNick=1024%E5%B0%8F%E7%A5%9E; AU=47C; UN=weixin_44786530; BT=1665208243704; p_uid=U010000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22weixin_44786530%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_19616795140-1665200689671-367015!5744*1*weixin_44786530; dc_sid=03889dd58c5ee2a617f40f993a5c88bb; c_segment=7; _ga=GA1.2.1557385788.1667204710; __bid_n=18450b4328cbb03b4b4207; c_dl_um=-; HWWAFSESID=f837aa7b0b98a954a99; HWWAFSESTIME=1668306228113; __gpi=UID=00000b7e289acd01:T=1668750622:RT=1668750622:S=ALNI_MZXMYfvcP-dklswFdIrG5fCUMmr6w; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1668160708,1668482890,1669170957; SESSION=fc5b2bfd-72f0-4e69-bd31-3a9ab989ca57; c_dl_prid=1668161164852_281043; c_dl_rid=1670232721139_374276; c_dl_fref=https://www.baidu.com/link; c_dl_fpage=/download/xxxzzzyyy/604182; c_hasSub=true; c_first_ref=www.baidu.com; c_first_page=https%3A//blog.csdn.net/weixin_42863800/article/details/107024401; dc_session_id=10_1670465432736.135193; c_dsid=11_1670465434070.901928; log_Id_click=295; ssxmod_itna=iqGxgDBD9DuDcDU2EDz=D2iX3YOACK77QCCAiKnDBMSeiNDnD8x7YDvAI5iYADmh0N5eiDOPrK8C0i2fPq82nomsVFrDdi3DU4i8DCw2NWWDen=D5xGoDPxDeDADYo0DAqiOD7qDdXLvvz2xGWDmRkDWPDYxDrXpKDRxi7DDHQzx07DQykQSPmBhE1Q0BPHlKD9EoDsg0felKpjS3x/2YEIFB3Ex0kl40OShysGhoDUY5GMaYirZw3/lq4WBidQCx4KWiTfB+qYBGxCTxekmb9HBTKfTxxDDP4Oi9P4D; ssxmod_itna2=iqGxgDBD9DuDcDU2EDz=D2iX3YOACK77QCCAiKD8TZ4+xGXd445GaDm2009=KApd9Y7kDt7VG7dA=Kqi+kE0dQUGnh0sqR=q8ns3jcx8BsY3bDgpjkX7DS=0ZDzozkYfNdV44ckV1wdg6WkZPeNIcuTVGTCh6xb+Yc=Bi5qd1OH81OiecA8pZ78V0GzlDoGO1rWAfubvc8Fx8Ade9w4fhAb2UnwB2YvM8YtV6dUQK5j5MFXZlKweZuEtDPvLcuXt0OaPr1bd1uRV=TNK+BwdF9jYEy=weEW7LFlchevj/jie25WnXA/yfsQriD+z5ToqlHl7sdd8jSH3OsOkYxmWWmGfRKt7WDmqZwhuT+9wzBg8hqx2iblrzhDkRqeUWiiYQBDmKY3B7HXOK3x50+8LhYQBrB3Pg0707DMfvFEb9BWNhOM+8cj5NWKehA0YQO4NUwp=oGBjC07HxCdj4Hxbz6rzTrzjRKAWPD7QHAGniUdGhCCfOIyE0HH6KPDGcDG7eiDD; csrfToken=TCK9wNl_RUHJEYtv0BASyWk5; c_pref=https%3A//blog.csdn.net/weixin_44786530/article/details/128206025%3Fspm%3D1001.2014.3001.5501; c_ref=https%3A//www.csdn.net/%3Fspm%3D1001.2101.3001.4476; c_page_id=default; dc_tos=rmjvju; log_Id_pv=391; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1670465658; log_Id_view=3022',
        'Referer': 'https://www.csdn.net/?spm=1001.2101.3001.4476',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    content = response.content.decode()
    title_list = re.findall(r'class="blog-text">(.+?)</span', content)
    print(f"获取到的文章标题是:{title_list}")
    if title_list:
        return title_list[0]
    else:
        return ""


def run():
    print("总调度")
    title = get_example()
    if title:
        make_one(title)


if __name__ == '__main__':
    run()
