# @Version  : 1.0
# @Author   : 故河
from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with , marshal

app = Flask(__name__)

api = Api(app)

class User(object):
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age

# 声明需要序列化的数据
resource_fields = {
    "user_id": fields.Integer,
    "name": fields.String,
}

class Demo1Resource(Resource):
    @marshal_with(resource_fields, envelope="data1")
    def get(self):
        user = User(1,"tzy",21)
        return user

class Demo2Resource(Resource):
    def get(self):
        user = User(2,"lz",22)
        return marshal(user, resource_fields, envelope="data2")

api.add_resource(Demo1Resource, "/demo1")
api.add_resource(Demo2Resource, "/demo2")

if __name__ == '__main__':
    app.run(debug=True)