# @Version  : 1.0
# @Author   : 故河
# 请求钩子

from flask import Flask, request

app = Flask(__name__)

# 每次请求前执行
@app.before_request
def before_first_request():
    print("before_request")

# 没有抛出错误，在每次请求后执行，需要返回一个响应对象
@app.after_request
def after_request(response):
    print("after_request")
    return response

# exception 参数，用于处理请求处理过程中发生的异常。
@app.teardown_request
def teardown_request(exception=None):
    print("teardown_request")

@app.route('/')
def index():
    print("hello world")
    return "<h1>hello world</h1>"

if __name__ == '__main__':
    app.run(debug=True)