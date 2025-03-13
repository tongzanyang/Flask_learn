# @Version  : 1.0
# @Author   : 故河
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)

# 加载配置信息
app.config.from_pyfile("setting.py")

api = Api(app)

db = SQLAlchemy(app)



# 导入业务模块，此位置避免循环导入问题
from blog.controller import blog_message, API_v1