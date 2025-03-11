# @Version  : 1.0
# @Author   : 故河

# 在类视图添加装饰器
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

# 定义装饰器
def decorator1(func):
    def wrapper(*args, **kwargs):
        print("decorator1")
        return func(*args, **kwargs)

    return wrapper


def decorator2(func):
    def wrapper(*args, **kwargs):
        print("decorator2")
        return func(*args, **kwargs)

    return wrapper


class Decorator(Resource):
    # 为类方法添加装饰器
    method_decorators = {
        "get": [decorator1, decorator2],
        "post": [decorator2]
    }

    def get(self):
        return {'hello': 'world'}

    def post(self):
        return {'msg': 'post hello world'}


api.add_resource(Decorator, '/', methods=["GET", "POST"])