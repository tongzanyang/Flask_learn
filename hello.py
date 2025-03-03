# @Version  : 1.0
# @Author   : 故河

from flask import Flask, request, make_response, session

class config(object):
    SECRET_KEY = "t04241003+"

class config1(config):
    debug = True

# 创建一个Flask实例，指定当前工程目录
app = Flask(__name__)

# 1.
app.config.from_object(config1)

# 2.
# app.config.from_pyfile("settings.py")

# 3.环境变量


key = app.config["SECRET_KEY"]


@app.route("/")
def test():
    # 自定义响应信息
    response = make_response(f"<h1>Hello World{key}</h1>")
    response.headers['X-Custom-Header'] = 'Value'
    response.status = 200
    return response


@app.route('/get_data', methods=['POST','GET'])
def get_data():
    data = request.args.get('name')   # 记录请求的参数
    return f"{data}"


@app.route('/cookie')
def set_cookie():
    # 如何设置cookie,通过创建响应对象，在响应之前对响应内容进行cookie设置
    response = make_response("set cookie success")
    response.set_cookie('name', 'tzy', max_age=100)
    # response.delete_cookie()
    return response

@app.route("/get_cookie")
def get_cookie():
    cookies = request.cookies.get('name')
    return f"hello {cookies}"


# 设置session，前提设置一个secret key
@app.route('/set_session')
def set_session():
    session['name'] = 'tzy'
    return "set session success"

# 获取session
@app.route('/get_session')
def get_session():
    name = session.get('name')
    return f'get session name {name}'




if __name__ == '__main__':
    # debug模式运行
    app.run(debug=True)