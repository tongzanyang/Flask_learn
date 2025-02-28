# @Version  : 1.0
# @Author   : 故河
# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 定义模型类
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'