# @Version  : 1.0
# @Author   : 故河
from blog import db

class Article(db.Model):
    __tablename__ = 'b_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True)
    content = db.Column(db.String(100))

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<article %r>' % self.title