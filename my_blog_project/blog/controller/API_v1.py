# @Version  : 1.0
# @Author   : 故河
from flask_restful import Resource, marshal, fields
from blog.model.Article import Article
from blog import api

fields_data = {
    "id": fields.Integer,
    "title": fields.String,
    "content": fields.String
}

class GET_data(Resource):
    def get(self):
        articles = Article.query.all()
        return marshal(articles,fields_data,envelope="all_articles")

api.add_resource(GET_data,"/api/v1/articles", endpoint="articles")