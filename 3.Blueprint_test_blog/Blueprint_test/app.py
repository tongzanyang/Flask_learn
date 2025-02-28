# @Version  : 1.0
# @Author   : 故河
import os
from flask import Flask, render_template
# 导入蓝图
from .auth import auth
from .blog import blog
# 导入模型
from .models import db



app = Flask(__name__)

# 注册蓝图
# 将所有的路由前缀设置为 /auth,/blog。
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(blog, url_prefix='/blog')

# 加载配置文件
settings_path = os.path.join(os.path.dirname(__file__), 'settings.py')
app.config.from_pyfile(settings_path)


# 初始化 SQLAlchemy 实例,数据库实例与应用进行绑定
db.init_app(app)

# 创建数据库和表
with app.app_context():
    db.create_all()

# 网站首页
@app.route('/', methods=['POST','GET'])
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)