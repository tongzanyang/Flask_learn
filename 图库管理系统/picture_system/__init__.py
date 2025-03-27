# @Version  : 1.0
# @Author   : 故河
# 图库管理系统
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# 加载配置信息
app.config.from_pyfile("setting.py")

db = SQLAlchemy(app)

# 首先导入User模型
from .models.User import User

# 然后导入Picture模型
from .models.Picture import Picture, PictureGroup

# 创建数据库和表
with app.app_context():
    db.create_all()
    
    # 创建上传目录
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

from .auth_sys import auth, api_v1
from .picture import picture
# 注册蓝图
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(picture, url_prefix='/picture')


@app.route("/")
def index():
    return render_template("index.html")

