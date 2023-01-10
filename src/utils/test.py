from flask import Flask
from flask import request
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)


@app.route('/', methods=['GET', 'POST'])
def index():
    return '欢迎来到我的主页'


@app.route('/receive', methods=['GET', 'POST'])
def receive():
    print(f"receive-----{request.data}")
    # if request.method == 'POST':
    #     data = request.form
    #     print("-----")
    #     print(data)
    #     return 'success!'
    return 'success!'


if __name__ == '__main__':
    app.run(port=8888)
