config = {
    "account": [
        {
            "push": "email",  # together 为 True 时失效, 不写不推送
            "email": "648133599@qq.com",
            "cookie": "_uuid=10562D7C4-6A96-4C94-59A4-39103B2A9F74E38977infoc; buvid3=A004761B-0722-98B6-DE47-3F7F0CC63A4631114infoc; b_nut=1665200740; hit-dyn-v2=1; i-wanna-go-back=-1; fingerprint=ded88b3cf197e0f213b1f9e974af4987; buvid_fp_plain=undefined; SESSDATA=99028fc1,1682234827,d63b2*a1; bili_jct=bf73d54e0bf695548db4a9cb9e47d541; DedeUserID=405719127; DedeUserID__ckMd5=d59469073af85b9d; nostalgia_conf=-1; buvid_fp=ded88b3cf197e0f213b1f9e974af4987; sid=66ksxnk9; b_ut=5; bsource=search_baidu; CURRENT_FNVAL=4048; rpdid=|(umYuY~mluR0J'uYY)Yl)lJ|; buvid4=BA4D7D5B-20A4-FF98-DAEC-3661712DE6C831114-022100811-mwLDrsa6+FGgRfzMckPQcQ==; PVID=1; innersign=0; b_lsid=7E79C7E7_185144E658E; bp_video_offset_405719127=739758437043273732",
            "options": {
                "watch": True,  # 每日观看视频
                "coins": 10,  # 投币个数
                "share": True,  # 视频分享
                "comics": True,  # 漫画签到
                "lb": True,  # 直播签到
                "threshold": 100,  # 仅剩多少币时不再投币(不写默认100)
                "toCoin": True,  # 银瓜子兑换硬币
            }
        },
        # {
        #     "cookie": "账号2",
        #     "options": {
        #         "watch": True,
        #         "coins": 5,
        #         "share": True,
        #         "comics": True,
        #         "lb": True,
        #     },
        #     "push": "pushplus",
        # },
    ],
    "together": True,  # 是否合并发送结果, 不写或 True 时合并发送
}
