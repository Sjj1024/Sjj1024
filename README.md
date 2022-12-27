想我了？ 请star我  
这是一个跑定时任务的仓库，支持定时签到等服务哦，感谢github  
个人网站地址：[www.1024shen.com](https://1024shen.com/)

先安装依赖吧:   
https://pypi.tuna.tsinghua.edu.cn/simple/ 清华  
http://pypi.doubanio.com/simple/ 豆瓣  
http://mirrors.aliyun.com/pypi/simple/ 阿里  
https://pypi.mirrors.ustc.edu.cn/simple/ 中国科学技术大学  
http://mirrors.163.com/pypi/simple/ 网易

```angular2html
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

action定时签到配置：  
```json
{
  "github": {
    "token": "githubtoken，暂时没有用，可以不写",
    "rep": "仓库地址，暂时没有用，可以不写",
    "email": "接收邮件的邮箱"
  },
  "bilibili": {
    "together": true,
    "account": [
      {
        "push": "接收通知的方式",
        "email": "接收通知的邮箱",
        "cookie": "哔哩哔哩cookie",
        "options": {
          "watch": true,
          "coins": 10,
          "share": true,
          "comics": true,
          "lb": true,
          "threshold": 100,
          "toCoin": true
        }
      }
    ]
  },
  "v2free": {
    "account": {
      "用户昵称": "用户cookie",
      "用户昵称2": "用户cookie"
    }
  },
  "52pojie": {
    "account": {
      "用户1": "用户cookie",
      "用户2": "用户cookie"
    }
  },
  "message": {
    "email": {
      "mail_host": "邮箱host",
      "mail_user": "用户邮箱",
      "mail_pass": "用户密码或认证",
      "sender": "发送者邮箱"
    },
    "server_key": "server酱的key，暂时没有用，可以不写",
    "qmsg_key": "qmsg的key，暂时没有用，可以不写"
  }
}
```

博客园：
![](https://img2023.cnblogs.com/blog/2466361/202212/2466361-20221208182656762-1298240916.png)

cdnd:  
![](https://img-blog.csdnimg.cn/2049460a205a4b869ce2c66ee58a38c0.png)

github:
![](https://sjj1024.github.io/CvReport/img/220310103457shan.jpg)

github:
<iframe height=498 width=510 src="https://sjj1024.github.io/CvReport/img/test.mp4">
<video controls height='100%' width='100%' src="https://sjj1024.github.io/CvReport/img/test.mp4"></video>
[![IMAGE ALT TEXT](https://sjj1024.github.io/CvReport/img/com_cate.7addb7be.png)](https://sjj1024.github.io/CvReport/img/test.mp4 "Unity Snake Game")
