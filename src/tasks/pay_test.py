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


if __name__ == '__main__':
    # 测试支付链接生成
    # paylod = {
    #     "money": 100,  # 金额，单位分
    # }
    # get_pay_link(paylod)
    # md5str = hashlib.md5("15670339118".encode(encoding='utf-8')).hexdigest().upper()
    # print("md5str", md5str)

    # 检查订单
    check_order()

    # 扫码支付
    # native_code()