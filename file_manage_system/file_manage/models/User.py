# @Version  : 1.0
# @Author   : 故河
from file_manage import db
from werkzeug.security import generate_password_hash, check_password_hash

# 定义模型类
class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # 增加长度以存储哈希后的密码

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def set_password(self, password):
        """设置密码，将明文密码转换为哈希值"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """验证密码是否正确"""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'