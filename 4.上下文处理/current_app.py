# @Version  : 1.0
# @Author   : 故河
from flask import Flask, request, abort, current_app, g
from blueprint_test import bp  # 确保导入的是蓝图对象

app = Flask(__name__)
app1 = Flask(__name__)

app.redis_cli = 'redis_cli'
app1.redis_cli = 'redis_cli'

# app.register_blueprint(bp, url_prefix='/bp')  # 注册蓝图

@app.route('/index')
def index():
    username = request.args.get('name')
    print(app.redis_cli)
    if username is None:
        abort(400)

    return f"欢迎{username}来到我的主页", 200

@app1.route('/app1')
def app1_fun():
    return f"{current_app.redis_cli}"

# 模拟一个数据库连接
# g.db：在 get_db 函数中，我们检查 g 对象中是否已经存储了数据库连接。如果没有，
# 则创建一个新的连接并存储到 g 中。
def get_db():
    if 'db' not in g:
        g.db = "Database connection"  # 模拟数据库连接
    return g.db

@app.route('/db')
def db_example():
    db = get_db()
    return f"Database connection: {db}"



if __name__ == '__main__':
    app.run(debug=True)



