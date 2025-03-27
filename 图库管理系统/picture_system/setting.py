# @Version  : 1.0
# @Author   : 故河
import os
DEBUG = True
SECRET_KEY = 't04241003+'
SQLALCHEMY_DATABASE_URI = 'sqlite:///picture_mg.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 文件上传配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size