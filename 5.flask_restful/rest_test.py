# @Version  : 1.0
# @Author   : 故河
from flask import Flask, Blueprint
from flask_restful import Resource, Api

app = Flask(__name__)

user_bp = Blueprint('user', __name__)


# 手收集类视图的注册信息（类视图和路由的绑定）
user_api = Api(app)
# user_api = Api(user_bp)

class HelloWorldResource(Resource):
    # 装饰器
    method_decorators = []

    def get(self):
        return {'hello': 'world'}

    def post(self):
        return {'msg': 'post hello world'}

# 视图与路由进行绑定
# endpoint:为路由起别名
user_api.add_resource(HelloWorldResource, '/', methods=['GET', 'POST'], endpoint='get')

# 注册蓝图
# app.register_blueprint(user_bp, url_prefix='/user')

