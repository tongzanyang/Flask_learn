# @Version  : 1.0
# @Author   : 故河
import os
from flask import Flask, render_template,  redirect, url_for,request
from flask_wtf import FlaskForm
# (分别用于创建文本输入框、电子邮件输入框和提交按钮。)
from wtforms import StringField, PasswordField,EmailField, SubmitField
# 分别用于验证字段是否为空和输入是否为有效的电子邮件地址。
from wtforms.validators import DataRequired, Email # (Email依赖于email_validator库)
from flask_sqlalchemy import SQLAlchemy
import bcrypt   # 加密算法


app = Flask(__name__)
app.secret_key = 't04241003+'   # 密钥保护,防止CSRF跨站请求伪造
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制文件大小为16MB

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 定义表单的结构
class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def form():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data.encode('utf-8')  # 将密码转换为字节类型
        email = form.email.data
        # 使用 bcrypt 进行密码加密
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return f'Name: {name}, 加密密码: <{hashed.decode("utf-8")}>, Email: {email}', 200
    return render_template('form.html', form=form)


# 文件上传
@app.route('/upload', methods=['POST'])
def upload():
    path = app.config['UPLOAD_FOLDER']
    file = request.files.get("file")
    if file:
        filename = file.filename
        file.save(os.path.join(path,filename))
        return f'文件保存成功：{filename}', 200
    return "没有文件上传。"


if __name__ == '__main__':
    app.run(debug=True)
