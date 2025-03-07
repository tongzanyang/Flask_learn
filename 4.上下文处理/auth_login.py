# @Version  : 1.0
# @Author   : 故河
# 综合请求钩子和g对象
from flask import Flask, request, g, abort

app = Flask(__name__)

# 构建认证机制,Flask上下文综合实践
'''
1.装饰器，对于特定函数强制要求用户登录
函数嵌套，通过user是否为空判断用户是否 登录
2.定义请求钩子，对所有视图尝试尝试获取用户认证后的身份信息。
如果用id不为空则获取身份信息。
'''

# 请求钩子,定义用户
@app.before_request
def authentication():
    # user = request.args.get("user")
    # if user is None:
    #     g.user = None
    # else:
    g.user = None    # 定义用户
    print(g.user)

    # 通过user是否为空判断用户是否登录


def request_login(out_fun):
    def inner():
        if g.user is None:
            abort(401)
        else:
            return out_fun()
    return inner

@app.route('/')
def index():
    return f'欢迎用户{g.user}'

@app.route('/profile')
@request_login
def get_user_profile():
    return f"user = {g.user}"