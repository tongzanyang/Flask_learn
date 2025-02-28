# @Version  : 1.0
# @Author   : 故河
from flask import render_template, request, redirect, url_for
from .. import models
from . import auth


# 登录响应
@auth.route('/login', methods=['POST','GET'])
def login():
    return render_template('login.html')


# 检查表单数据，通过则重定向到blog
@auth.route('/login_check', methods=['POST', 'GET'])
def login_check():
    # 获取表单数据
    username = request.form.get("username")
    password = request.form.get("password")

    # 不为空
    if username and password:
        exist_username = models.User.query.filter_by(username=username).first()

        # 验证是否为真
        if exist_username and password == exist_username.password:
            return redirect(url_for('blog.index'))   # 对应另一个蓝图的函数
        else:
            return '<h1>用户名或密码不正确，请重新输入</h1>', 400
    else:
        return '用户名或密码为空，请输入完整', 400


# 注册
@auth.route('/register', methods=['GET','POST'])
def register():
    return render_template('templates/register.html')


# 注册通过则重定向到登录
@auth.route('/register_check', methods=['POST','GET'])
def register_check():
    new_username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    email = request.form.get('email')

    # 确保输入完整
    if new_username and password and password2 and email:
        exist_username = models.User.query.filter_by(username=new_username).first()
        exist_email = models.User.query.filter_by(email=email).first()

        if exist_username:
            return f'用户名{new_username}已经存在！',  400
        elif exist_email:
            return f'邮箱号{email}已经注册过了！', 400
        elif password != password2:
            return f'两次输入密码不一致，请重新输入', 400
        else:
            new_user = models.User(username=new_username, password=password, email=email)
            # 添加到数据表
            models.db.session.add(new_user)
            # 提交事务
            models.db.session.commit()
            return redirect(url_for('auth.login'))




