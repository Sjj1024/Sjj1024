config = {
    "together": False,  # 是否合并发送结果, 不写或 True 时合并发送
    "account": [
        {
            "push": "email",  # together 为 True 时失效, 不写不推送
            "email": "648133599@qq.com",
            "cookie": "buvid3=39CBF8F1-15F7-A1E7-FEF7-2F75D60A9FBF98924infoc; b_nut=1751897498; _uuid=BF65AFC7-105DC-A2A3-5CA7-10FF2757102F81088323infoc; CURRENT_QUALITY=0; buvid_fp=4b868540638619ec9ee1d6b9ea9253b6; buvid4=76BA0DAA-54CE-1D17-7164-51D0625D17F290748-025080122-wvLLBCnxbC3XMDMnmiz5fw%3D%3D; rpdid=|(u))JkRYJ|k0J'u~lR|lmkmu; enable_web_push=DISABLE; home_feed_column=5; b_lsid=5D1102A24_19A118B6003; SESSDATA=9da85d70%2C1776783001%2Ca3f0e%2Aa1CjBXNgM3OPHNsoObZ9mifXF7YIndfJEwvM1zKmbMC1LjVlmD4lpfUw3PU599n7LosdcSVmtKRV81RjUxMm1OTGE0ZkhQRUY2N1ZpQnIxLXJPLXdsbjFGdkNCbXhnbHQxUDFrVjJPMEUtTWJ6NjAybWhoQzNKaHRtU0tHdlR4MHkySkhnYXNFMVZ3IIEC; bili_jct=a6abe3b866b90649392d491ad715cf26; DedeUserID=3632304542976802; DedeUserID__ckMd5=3b593eb55b65bd52; bp_t_offset_3632304542976802=1126967687252017152; theme-tip-show=SHOWED; CURRENT_FNVAL=2000; browser_resolution=1462-181; sid=ppjky0mh; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjE0OTAzMDMsImlhdCI6MTc2MTIzMTA0MywicGx0IjotMX0.75S_T6OJLR6m8htIFxowjVtP7eptmpnwTjrFIbgrEpk; bili_ticket_expires=1761490243",
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
    ]
}
