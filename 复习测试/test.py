from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, fields, marshal_with, marshal

'''
思路分析
一个呼获取数据，添加数据的API
1.连接数据库配置信息
2.查询出数据库表中所有的数据
3.序列化数据为特定格式marshal，返回数据
4.绑定路由/api/v1/user_info  GET请求
5.POST请求上传数据时，组织数据存储到数据表
'''

app = Flask(__name__)

# 配置数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:t04241003+@localhost:3306/flask_test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义数据库模型
class User_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self): 
        return f'<User {self.username}>'

# 定义序列化格式
resource_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
}

# 创建数据库表
with app.app_context():
    db.create_all()

# 初始化 API
api = Api(app)

class Data_info(Resource):
    @marshal_with(resource_fields, envelope="get_info")
    def get(self):
        # 查询所有用户信息
        data = User_info.query.all()
        return data

    def post(self):
        # 获取 POST 请求中的 JSON 数据
        data = request.get_json()
        new_username = data.get("username")
        new_email = data.get("email")

        # 创建新用户
        new_user = User_info(username=new_username, email=new_email)
        db.session.add(new_user)
        db.session.commit()

        # 返回新创建的用户数据
        return marshal(new_user, resource_fields, envelope="post_info")

# 添加资源
api.add_resource(Data_info, "/api/v1/user_info")



if __name__ == '__main__':
    app.run(debug=True)