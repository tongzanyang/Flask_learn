# @Version  : 1.0
# @Author   : 故河

from flask import Flask, request, render_template

class config(object):
    SECREY_KEY = "t04241003+"

class config1(config):
    debug = True

# 创建一个Flask实例，指定当前工程目录
app = Flask(__name__)

# 1.
app.config.from_object(config1)

# 2.
# app.config.from_pyfile("settings.py")

# 3.环境变量


key = app.config["SECREY_KEY"]




@app.route("/")
def test():
    return f"<h1>Hello World{key}</h1>"

if __name__ == '__main__':
    app.run()

