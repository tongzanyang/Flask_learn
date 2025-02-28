# @Version  : 1.0
# @Author   : 故河

# min_web静态
from flask import *

# 创建应用实例
# 指定静态文件访问路径和目录名称
app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()