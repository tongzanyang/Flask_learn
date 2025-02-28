# 视图函数
# 接收参数，处理请求，自定义响应，获取表单参数，

from flask import *
# 导入自定义表单处理模块
from flask_wtf import FlaskForm
# 导入构建输入筐类型
from wtforms import StringField, PasswordField, SubmitField
# 验证方法
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = 't04241003+'   # 密钥保护,防止CSRF跨站请求伪造

users = {
    'admin':'t04241003+',
    'tzy':'123.com',
}

class MyForm(FlaskForm):
    name = StringField('用户名:', validators=[DataRequired()])
    password = PasswordField('密码:', validators=[DataRequired()])
    submit = SubmitField('登录')

# 登录
@app.route('/', methods=['POST','GET'])
def login():
    form = MyForm()
    if form.validate_on_submit():   # 如果已经submit了
        # 获取用户输入的信息
        name = form.name.data
        password = form.password.data
        if name in users.keys() and password == users[name]:
            return f"欢迎{name}登录！", 200
        else:
            return f"用户名或者密码错误", 401
    # 没有则返回表单
    return render_template('form.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)

