# @Version  : 1.0
# @Author   : 故河
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

# 创建 Flask 应用
app = Flask(__name__)
api = Api(app)

# 创建RequestParser对像
parser = reqparse.RequestParser()
# 需要验证或转换的参数声明
parser.add_argument('name', type=str, location='args', action="append", default='admin')


def decorator(func):
    def wear(*args, **kwargs):
        print("decorator1")
        return func(*args, **kwargs)
    return wear

class Request_parser(Resource):
    method_decorators = {
        'get': [decorator],
    }
    def get(self):
        # 启动验证
        # name = request.args.get('name')
        # if not name:
        #     pass
        req = parser.parse_args()
        return {'message':f'{req}'}, 200    # 返回json

# 绑定路由
api.add_resource(Request_parser,'/hello')

if __name__ == '__main__':
    app.run(debug=True)

