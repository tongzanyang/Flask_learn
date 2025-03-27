# @Version  : 1.0
# @Author   : 故河
# API：1.获取所有的用户名，2.用户注册
from flask_restful import Api, Resource, fields, marshal_with, request, abort, marshal
from . import User, app, db
from werkzeug.security import generate_password_hash, check_password_hash

"""
思路分析
1.查询数据库所有的用户名
2.用户注册：获取请求中的用户密码，确认密码，重定位到register_auth进行注册操作
"""

api = Api(app)

# 序列化数据
resource_fields = {
    "id": fields.Integer,
    "username": fields.String,
}

class User_Register(Resource):
    @marshal_with(resource_fields)
    def get(self):
        all_user = User.query.all()
        return all_user

    def post(self):
        # 获取不同类型的请求数据
        form_data = request.form  # 表单数据
        json_data = request.json  # JSON 数据

        # 根据你的需求选择合适的数据来源
        new_username = None
        new_password = None

        # 优先从 JSON 数据中获取
        if json_data:
            new_username = json_data.get("username")
            new_password = json_data.get("password")
        # 如果没有 JSON 数据，从表单数据中获取
        elif form_data:
            new_username = form_data.get("username")
            new_password = form_data.get("password")

        # 注册验证
        if not new_username or not new_password:
            abort(400, message="用户名或密码为空")

        # 检查用户是否已存在
        if User.query.filter_by(username=new_username).first():
            abort(400, message="用户已经存在！")

        # 创建新用户
        hashed_password = generate_password_hash(new_password)
        new_user = User(username=new_username, password=hashed_password)
        # 提交会话
        db.session.add(new_user)
        db.session.commit()
        marshal(new_user, resource_fields)

        return {"message": f"用户{new_username}注册成功！"}, 201

api.add_resource(User_Register,"/api/v1/ac_user")



