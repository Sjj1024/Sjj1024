import base64
import requests
import json
from flask import Flask, request
from flask_sock import Sock


def get_token(appid, secret):
    url = "https://developer.toutiao.com/api/apps/v2/token"
    payload = json.dumps({
        "appid": appid,
        "secret": secret,
        "grant_type": "client_credential"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res_json = response.json()
    token = res_json.get("data").get("access_token")
    print("x_token-----", token)
    return token


def get_live_id(x_token, game_token):
    url = "http://webcast.bytedance.com/api/webcastmate/info"
    payload = json.dumps({
        "token": game_token
    })
    headers = {
        'X-Token': x_token,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print("response", response.text)
    res_json = response.json()
    print("get_live_id res_json", res_json)
    live_id = res_json.get("data").get("info").get("room_id")
    print("live_id---", live_id)
    return live_id


def start_task(appid, live_id, x_token):
    print("开启直播推送任务appid", appid)
    print("开启直播推送任务live_id", live_id)
    print("开启直播推送任务x_token", x_token)
    task_list = ["live_comment", "live_gift", "live_like"]
    for t in task_list:
        print("task", t)
        url = "https://webcast.bytedance.com/api/live_data/task/start"
        payload = json.dumps({
            "roomid": str(live_id),
            "appid": appid,
            "msg_type": "live_comment"
        })
        headers = {
            'access-token': x_token,
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)


def live_run(game_token):
    print("main game token", game_token)
    appid = "1"
    secret = "1"
    x_token = get_token(appid, secret)
    live_id = get_live_id(x_token, game_token)
    # live_id = "7342348234029340923"
    start_task(appid, live_id, x_token)
    return live_id


# Initialize Flask-Sock
app = Flask(__name__)
sock = Sock(app)
# 创建全局的ws对象数组
ws_list = []
ws_closed = []


# @app.route('/dy')
# def handle_token():
#     # 从查询参数中获取 token
#     token = request.args.get('token')
#     if token:
#         # 打印 token 到控制台
#         print(f"Received game token: {token}")
#         decode_token = base64.b64decode(token).decode('utf-8')
#         live_id = "1342348234029340923"
#         try:
#             live_id = live_run(decode_token)
#         except Exception as e:
#             print("live run error", e)
#         return str(live_id)
#     else:
#         return "No token provided in the request.", 400
#

@app.route('/dy')
def handle_token():
    # 从查询参数中获取 token
    token = request.args.get('token')
    if token:
        # 打印 token 到控制台
        print(f"Received game token: {token}")
        decode_token = base64.b64decode(token).decode('utf-8')
        live_id = "1342348234029340923"
        try:
            live_id = live_run(decode_token)
        except Exception as e:
            print("live run error", e)
        return str(live_id)
    else:
        return "No token provided in the request.", 400


# 接收抖音数据推送
@app.route('/dy/webhook-dv', methods=['POST'])
def handle_push():
    # 获取请求体中的数据
    try:
        data = request.get_data()
        # 打印接收到的数据
        print(f"Received data: {data}")
        # json
        json_data = request.get_json()
        print("json_data", json_data)
    except Exception as e:
        print("Error parsing request data:", e)
    return "ok", 200


def handle_sync(data, self):
    # 同步各端ws消息
    for ws in ws_list:
        if not ws.connected:
            ws_closed.append(ws)
        elif data and ws != self:
            ws.send(data)
    # 删除已断开的链接
    for cl in ws_closed:
        ws_list.remove(cl)
    ws_closed.clear()
    print(f"live num: {len(ws_list)}, done num: {len(ws_closed)}")


# WebSocket endpoint
@sock.route('/dy/ws')
def echo(self):
    global ws_list
    ws_list.append(self)
    while True:
        print(f"global ws list: {len(ws_list)}")
        # 判断是断开连接还是还在链接
        data = self.receive()
        self.send(data)
        # 同步消息和关闭ws clear


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8087, debug=True)
