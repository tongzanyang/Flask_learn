# @Version  : 1.0
# @Author   : 故河
from blog import db

class User(db.Model):
    __tablename__ = 'b_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.username