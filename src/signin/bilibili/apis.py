class BiliBiliAPI:
    # 获取视频信息地址
    VIDEO_INFO = "https://api.bilibili.com/x/web-interface/view"
    # 获取用户信息
    PERSONAL_INFO = "http://api.bilibili.com/x/space/myinfo"
    # 直播签到
    LIVE_BROADCAST = "https://api.live.bilibili.com/sign/doSign"
    # 漫画签到
    COMICS = "https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn"
    # 漫画签到信息
    COMICS_INFO = "https://manga.bilibili.com/twirp/activity.v1.Activity/GetClockInInfo"
    # 获取热门推荐
    RECOMMAND = "https://api.bilibili.com/x/web-interface/popular"
    # 客户端分享视频
    VIDEO_SHARE = "https://api.bilibili.com/x/web-interface/share/add"
    # 投币
    COIN = "https://api.bilibili.com/x/web-interface/coin/add"
    # 看视频
    VIDEO_CLICK = "https://api.bilibili.com/x/click-interface/click/web/h5"
    VIDEO_HEARTBEAT = "https://api.bilibili.com/x/click-interface/web/heartbeat"
    # 兑换硬币
    TO_COIN = "https://api.live.bilibili.com/xlive/revenue/v1/wallet/silver2coin"
