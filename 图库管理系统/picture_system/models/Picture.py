from datetime import datetime
from . import db

class Picture(db.Model):
    __tablename__ = 'pictures'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # 文件大小（字节）
    file_type = db.Column(db.String(50), nullable=False)  # 文件类型
    group_id = db.Column(db.Integer, db.ForeignKey('picture_groups.id'))  # 分组ID
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    upload_user = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    
    # 关联关系
    group = db.relationship('PictureGroup', backref=db.backref('pictures', lazy=True))
    user = db.relationship('User', backref=db.backref('pictures', lazy=True))

class PictureGroup(db.Model):
    __tablename__ = 'picture_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    create_user = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    
    # 关联关系
    user = db.relationship('User', backref=db.backref('picture_groups', lazy=True)) 