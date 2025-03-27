# @Version  : 1.0
# @Author   : 故河
from flask import request, render_template, flash, redirect, url_for, session
from . import auth, db, User
from werkzeug.security import generate_password_hash, check_password_hash

@auth.route("/login")
def login():
    return render_template("login.html")


# 认证
@auth.route("/login_auths", methods=["POST"])
def login_auths():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("用户名和密码不能为空", 'error')
        return redirect(url_for("auth.login"))

    # 查询数据库中是否存在该用户
    user = User.query.filter_by(username=username).first()
    # 密码校验
    if user and check_password_hash(user.password, password):
        session["username"] = username
        flash("登录成功！", "success")
        return redirect(url_for("index"))
    else:
        flash('用户名或密码错误！', 'error')
        return redirect(url_for("auth.login"))


# 登出
@auth.route("/logout")
def logout():
    session.pop('username', None)
    flash('已成功登出！', 'success')
    return redirect(url_for("index"))


# 注册
@auth.route("/register", methods=["GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")

@auth.route("/register_auth", methods=["POST"])
def register_auth():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if not username or not password:
        flash('用户名和密码不能为空！', 'error')
        return redirect(url_for("auth.register"))

    if password != confirm_password:
        flash('两次输入的密码不一致！', 'error')
        return redirect(url_for("auth.register"))

    # 检查用户是否已存在
    if User.query.filter_by(username=username).first():
        flash('用户名已存在！', 'error')
        return redirect(url_for("auth.register"))

    # 创建新用户
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功！请登录', 'success')
        return redirect(url_for("auth.login"))

    except Exception as e:
        db.session.rollback()
        flash('注册失败，请稍后重试！', 'error')
        return redirect(url_for("auth.register"))



# ADUC

