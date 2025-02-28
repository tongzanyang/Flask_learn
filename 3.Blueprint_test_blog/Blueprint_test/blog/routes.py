# @Version  : 1.0
# @Author   : 故河
from flask import render_template
from . import blog


@blog.route('/index', methods=['POST','GET'])
def index():
    return render_template("index1.html")


