from file_manage import app, db
from file_manage.models.User import User
from flask import request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# 显示登录界面
@app.route("/login")
def login():
    return render_template("login.html")

# 登录验证
@app.route("/auth", methods=["POST"])
def auth():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not username or not password:
        flash('用户名和密码不能为空！', 'error')
        return redirect(url_for("login"))
    
    # 查询数据库中是否存在该用户
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        # 登录成功，设置session
        session['username'] = username
        flash('登录成功！', 'success')
        return redirect(url_for("index"))
    else:
        flash('用户名或密码错误！', 'error')
        return redirect(url_for("login"))

# 登出
@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('已成功登出！', 'success')
    return redirect(url_for("index"))

# 注册
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    
    if not username or not password:
        flash('用户名和密码不能为空！', 'error')
        return redirect(url_for("register"))
    
    if password != confirm_password:
        flash('两次输入的密码不一致！', 'error')
        return redirect(url_for("register"))
    
    # 检查用户是否已存在
    if User.query.filter_by(username=username).first():
        flash('用户名已存在！', 'error')
        return redirect(url_for("register"))
    
    # 创建新用户
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功！请登录', 'success')
        return redirect(url_for("login"))
    except Exception as e:
        db.session.rollback()
        flash('注册失败，请稍后重试！', 'error')
        return redirect(url_for("register"))