import hashlib
import requests


# 发起支付请求
def pay(money, name, notify_url, out_trade_no, payType, pid, return_url, webName, key):
    # money = ''               # 金额
    # name = ''                # 商品名称
    # notify_url = ''          # 服务器异步通知地址
    # out_trade_no = ''        # 商户订单号
    # pid = ''                 # 商户ID
    # return_url = ''          # 页面跳转通知地址
    # webName = ''             # 网站名称
    # payType = ''             # 支付方式:alipay:支付宝,wxpay:微信支付,qqpay:QQ钱包,tenpay:财付通,
    # key = ''                 # 密钥,易支付注册会提供pid和秘钥

    # 对参数进行排序，生成待签名字符串--(具体看支付宝)
    sg = 'money=' + money + '&name=' + name + '&notify_url=' + notify_url + '&out_trade_no=' + out_trade_no + '&pid=' + pid + '&return_url=' + return_url + '&sitename=' + webName + '&type=' + payType
    # MD5加密--进行签名
    sign = hashlib.md5((sg + key).encode(encoding='UTF-8')).hexdigest()  # 签名计算
    # 最后要将参数返回给前端，前端访问url发起支付
    url = 'https://z-pay.cn/submit.php?' + sg + '&sign=' + sign + '&sign_type=MD5'
    res = requests.post(url).content.decode()
    return res


# 查询商户信息与结算规则
def act(pid, key):
    url = 'https://z-pay.cn/api.php?act=query&pid=' + pid + '&key=' + key
    res = requests.get(url).content.decode()
    return res


# 修改结算账号
def change(pid, key, account, username):
    url = 'https://z-pay.cn/api.php?act=change&pid=' + pid + '&key=' + key + '&account=' + account + '&username=' + username
    res = requests.get(url).content.decode()
    return res


# 查询结算记录
def settle(pid, key):
    url = 'https://z-pay.cn/api.php?act=settle&pid=' + pid + '&key=' + key
    res = requests.get(url).content.decode()
    return res


# 查询单个订单
def order(pid, key, out_trade_no):
    url = 'https://z-pay.cn/api.php?act=order&pid=' + pid + '&key=' + key + '&out_trade_no=' + out_trade_no
    res = requests.get(url).content.decode()
    return res


# 批量查询订单
def orders(pid, key, limit):
    url = 'https://z-pay.cn/api.php?act=orders&pid=' + pid + '&key=' + key
    res = requests.get(url).content.decode()
    return res


if __name__ == '__main__':
    money = '0.01'  # 金额
    name = ''  # 商品名称
    notify_url = 'https://juejin.cn/'  # 服务器异步通知地址
    out_trade_no = ''  # 商户订单号
    payType = ''  # 支付方式:alipay:支付宝,wxpay:微信支付,qqpay:QQ钱包,tenpay:财付通
    pid = ''  # 商户ID
    return_url = 'https://juejin.cn/'  # 页面跳转通知地址
    webName = 'PakePlus'  # 网站名称
    key = ''

    res = pay(money, name, notify_url, out_trade_no, payType, pid, return_url, webName, key)
    print(res)
    # act(pid, key)
    # print(settle(pid, key))
    # print(order(pid, key, out_trade_no))
    # limit = '50'
    # print(orders(pid, key, limit))
