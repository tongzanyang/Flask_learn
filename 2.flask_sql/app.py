# @Version  : 1.0
# @Author   : 故河
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 统一资源标识符
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:t04241003+@localhost:3306/flask_test'
# Postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:t04241003+@localhost:5432/flask_test'
# 是否跟踪对象的修改，并发出信号
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义模型类
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# 创建管理数据库和表
with app.app_context():
    db.create_all()

# 首页
@app.route('/')
def index():
    return render_template("index.html")

# 注册界面
@app.route('/register')
def register():
    return render_template("register.html")

# 增加用户
@app.route('/add_user', methods=['POST'])
def add_user():
    # 获取表单数据
    username = request.form.get("username")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    email = request.form.get("email")

    # 检查所有必要字段是否都存在
    if username and password and password2 and email:
        if password == password2:
            # 检查用户名是否已存在
            existing_username = User.query.filter_by(username=username).first()
            if existing_username:
                return "该用户名已被注册，请更换用户名", 400
            # 检查邮箱是否已存在
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                return "该邮箱已被注册，请更换邮箱", 400

            try:
                new_user = User(username=username, password=password, email=email)
                # 添加到数据表
                db.session.add(new_user)
                # 提交事务
                db.session.commit()
                return f"注册成功，欢迎用户：{username}", 200

            except Exception as e:
                # 出现异常时回滚数据库会话
                db.session.rollback()
                return f"注册失败，原因：{str(e)}", 500
        else:
            return "前后两次密码不一致,请重新输入", 400
    else:
        return "请填写完整的注册信息", 400


# 删除用户
@app.route('/delete_user', methods=['GET'])
def delete_user():
    user_id = request.form.get('user_id')
    if user_id:
        try:
            user = User.query.get(int(user_id))
            if user:
                db.session.delete(user)
                db.session.commit()
                return f"用户 {user.username} 删除成功", 200
            else:
                return "未找到该用户", 404
        except Exception as e:
            db.session.rollback()
            return f"删除用户失败，原因：{str(e)}", 500
    else:
        return "请提供用户ID", 400


# 修改用户
@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form.get('user_id')
    if user_id:
        try:
            user = User.query.get(int(user_id))
            if user:
                new_username = request.form.get('username')
                new_password = request.form.get('password')
                new_email = request.form.get('email')
                if new_username:
                    existing_username = User.query.filter_by(username=new_username).first()
                    if existing_username and existing_username.id != user.id:
                        return "该用户名已被使用，请更换", 400
                    user.username = new_username
                if new_password:
                    user.password = new_password
                if new_email:
                    existing_email = User.query.filter_by(email=new_email).first()
                    if existing_email and existing_email.id != user.id:
                        return "该邮箱已被使用，请更换", 400
                    user.email = new_email
                db.session.commit()
                return f"用户 {user.username} 信息更新成功", 200
            else:
                return "未找到该用户", 404
        except Exception as e:
            db.session.rollback()
            return f"更新用户信息失败，原因：{str(e)}", 500
    else:
        return "请提供用户ID", 400


# 查找用户
@app.route('/search_user', methods=['POST'])
def search_user(user_id):
    user_id = request.form.get("user_id")
    if user_id:
        user = User.query.filter_by(int(user_id))
        if user:
            return f"用户ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}", 200
        else:
            return "未找到该用户", 404
    else:
        return "请提供用户ID", 400


@app.route('/all')
def search():
    users = User.query.filter_by(username='admin').all()
    if users:
        return "用户存在"
    else:
        return "用户不存在"



if __name__ == '__main__':
    app.run(debug=True)

