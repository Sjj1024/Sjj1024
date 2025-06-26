import json
import time
import requests
import hashlib
from urllib.parse import urlencode, unquote


# 构造签名函数
def pay_sign(attributes, key):
    attributes_list = list(attributes)
    for a in attributes_list:
        if attributes[a] == '':
            attributes.pop(a)
    attributes_new = {k: attributes[k] for k in sorted(attributes.keys())}
    return hashlib.md5((unquote(urlencode(attributes_new)) + '&key=' + key)
                       .encode(encoding='utf-8')).hexdigest().upper()


def get_pay_link(paylod):
    mchid = ''  # PAYJS 商户号
    key = ''  # 通信密钥
    # 构造订单参数
    money = paylod.get("money")
    pay_type = paylod.get("payType", None)
    time_str = str(int(time.time()))
    # 1024 小神支付使用的就是这种方式，然后将 url 生成二维码，即可支付
    # 默认微信支付，如果是支付宝需要添加："type":"alipay"
    # order = {
    #     'mchid': mchid,
    #     'body': '我是一个测试订单标题',  # 订单标题
    #     'total_fee': money,  # 金额,单位:分
    #     'out_trade_no': 'payjs_jspay_demo*' + time_str,  # 订单号
    #     "auto": 1,
    #     "hide": 1,
    #     "type": pay_type  # 微信支付无需填写
    # }

    order = {
        "mchid": '1593541201',
        "body": '测试订单标题',
        "total_fee": 1000,
        "out_trade_no": 'payjs_jspay_demo_2323923',
        "auto": 1,
        "hide": 1,
    }
    # 添加数据签名
    order['sign'] = pay_sign(order, key)
    # 9A7A0FC368F738C0F39A739C6CDBA062
    # 9A7A0FC368F738C0F39A739C6CDBA062
    print(f"生成订单: {order}")
    # 浏览器跳转到收银台
    url = 'https://payjs.cn/api/cashier?' + str(urlencode(order))
    # web.open(url,new=0,autoraise=True)
    print("url", url)


def check_order():
    '''
    订单查询接口
    '''
    payjs_order_id = ''  # PAYJS 平台订单号
    key = ''  # 填写通信密钥
    order = {
        'payjs_order_id': payjs_order_id
    }

    # 构造签名函数
    def sign(attributes, key):
        attributes_new = {k: attributes[k] for k in sorted(attributes.keys())}
        return hashlib.md5((unquote(urlencode(attributes_new)) + '&key=' + key)
                           .encode(encoding='utf-8')).hexdigest().upper()

    order['sign'] = sign(order, key)
    request_url = "https://payjs.cn/api/check"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=order, headers=headers)
    if response:
        print(response.json())


def native_code():
    '''
    扫码支付（主扫）
    '''
    key = ''  # 填写通信密钥
    mchid = ''  # 特写商户号
    order = {
        'body': 'test',  # 订单标题
        'out_trade_no': "32342323423234",  # 订单号
        'total_fee': 120,  # 金额,单位:分
        'mchid': mchid
    }

    # 构造签名函数
    def sign(attributes):
        attributes_new = {k: attributes[k] for k in sorted(attributes.keys())}
        return hashlib.md5((unquote(urlencode(attributes_new)) + '&key=' + key)
                           .encode(encoding='utf-8')).hexdigest().upper()

    order['sign'] = sign(order)
    request_url = "https://payjs.cn/api/native"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=order, headers=headers)
    if response:
        print(response.json())


# 构造签名函数
def sign_pay(attributes, sign_key):
    attributes_new = {k: attributes[k] for k in sorted(attributes.keys())}
    return hashlib.md5((unquote(urlencode(attributes_new)) + '&key=' + sign_key)
                       .encode(encoding='utf-8')).hexdigest().upper()


def get_sign(params_dict, key):
    # 按字典键名排序
    params_dict = {k: params_dict[k] for k in sorted(params_dict.keys())}
    params_str = "&".join(
        f'{key}={params_dict[key]}' for key in params_dict.keys()) + "&key=" + key
    md5 = hashlib.md5()
    md5.update(params_str.encode('utf-8'))
    sign = md5.hexdigest().upper()  # 加密转换为大写
    return sign


def yun_native_code():
    '''
    扫码支付（主扫）
    '''
    timestamp_us = int(time.time() * 1_000_000)
    key = ''  # 填写通信密钥
    mchid = ''  # 特写商户号
    # order = {
    #     'body': 'test yunpay',  # 订单标题
    #     'out_trade_no': timestamp_us,  # 订单号
    #     'total_fee': 10,  # 金额,单位:分
    #     'mch_id': mchid
    # }
    order = {"body": "YUN支付订单", "out_trade_no": timestamp_us, "total_fee": 10, "mch_id": ""}
    order['sign'] = get_sign(order, key)
    request_url = "https://api.pay.yungouos.com/api/pay/wxpay/nativePay"
    response = requests.post(request_url, data=order)
    if response:
        print(response.json())


def yun_js_pay():
    key = ''
    url = "https://zpayz.cn/mapi.php"
    payload = {
        "body": "YUN支付订单",
        "out_trade_no": "yunpay_demo_1750765774411",
        "total_fee": "10",
        "mch_id": "",
        "sign": ""
    }
    print("请求参数:", payload)
    response = requests.request("POST", url, data=payload)
    print(response.text)


def yun_order_check():
    print("检查订单号")
    key = ''  # 填写通信密钥
    mchid = ''  # 特写商户号
    order = {
        'out_trade_no': "1750752437809532",  # 订单号
        'mch_id': mchid
    }
    order['sign'] = get_sign(order, key)
    request_url = "https://api.pay.yungouos.com/api/system/order/getPayOrderInfo"
    response = requests.get(request_url, params=order)
    if response:
        print(response.json())


# z pay
def z_pay_test():
    sign_key = ""
    timestamp_us = int(time.time() * 1_000_000)
    order = {
        "pid": "",
        "type": "alipay",
        "out_trade_no": "zpay_" + str(timestamp_us),
        "notify_url": "https://juejin.cn/",
        "name": "VIP会员",
        "money": "10",
        "clientip": "192.168.1.100",
        "sign_type": "MD5"
    }
    order['sign'] = get_sign(order, sign_key)
    print("请求参数:", order)
    url = "https://zpayz.cn/mapi.php"
    response = requests.post(url, data=order)
    if response:
        print(response.json())


# z pay check
def z_pay_check():
    sign_key = ""
    order = {
        "act": "order",
        "pid": "",
        "key": sign_key,
        "out_trade_no": "zpay_1750927043587469"
    }
    url = "https://zpayz.cn/api.php"
    response = requests.get(url, params=order)
    if response:
        print(response.json())


if __name__ == '__main__':
    # 测试支付链接生成
    # paylod = {
    #     "money": 100,  # 金额，单位分
    # }
    # get_pay_link(paylod)
    # md5str = hashlib.md5("15670339118".encode(encoding='utf-8')).hexdigest().upper()
    # print("md5str", md5str)

    # 检查订单
    # check_order()

    # 扫码支付
    # yun_native_code()
    # yun_js_pay()

    # 检查订单
    # yun_order_check()

    # 扫码支付
    # native_code()

    # 支付测试
    # z_pay_test()

    # 检查订单号
    z_pay_check()