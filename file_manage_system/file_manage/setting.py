# @Version  : 1.0
# @Author   : 故河
DEBUG = True
SECRET_KEY = 't04241003+'
SQLALCHEMY_DATABASE_URI = 'sqlite:///file_mg.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 文件目录
FILE_DIR = os.path.join(BASE_DIR, "files")
# 不登录时显示的文件目录
PUBLIC_FILE = os.path.join(FILE_DIR, "public")

# 确保目录存在
os.makedirs(FILE_DIR, exist_ok=True)
os.makedirs(PUBLIC_FILE, exist_ok=True)
