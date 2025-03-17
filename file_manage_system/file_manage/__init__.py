# @Version  : 1.0
# @Author   : 故河
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile("setting.py")

api = Api(app)

db = SQLAlchemy(app)

# 辅助函数：获取文件大小
def get_file_size(filename):
    if app.config.get('TESTING', False):
        return '0 B'
    
    try:
        file_path = os.path.join(app.config['FILE_DIR'], filename)
        if not os.path.exists(file_path):
            file_path = os.path.join(app.config['PUBLIC_FILE'], filename)
        
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    except:
        return '未知'

# 辅助函数：获取文件修改时间
def get_file_mtime(filename):
    if app.config.get('TESTING', False):
        return '未知'
    
    try:
        file_path = os.path.join(app.config['FILE_DIR'], filename)
        if not os.path.exists(file_path):
            file_path = os.path.join(app.config['PUBLIC_FILE'], filename)
        
        mtime = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return '未知'

# 注册辅助函数为模板过滤器
app.jinja_env.globals.update(get_file_size=get_file_size)
app.jinja_env.globals.update(get_file_mtime=get_file_mtime)

# 导入视图函数
from .controller import file_action, login_auth, api_v1

# 导入模型
from .models.User import User

# 创建数据库表
with app.app_context():
    db.create_all()



