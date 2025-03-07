# @Version  : 1.0
# @Author   : 故河
from flask import Blueprint, current_app

# 创建蓝图对象
bp = Blueprint('test', __name__)

# 定义蓝图中的路由
@bp.route('/bp_index')
def bp_index():
    # current_app：代理对象，用于访问当前应用的实例。
    print(current_app.redis_cli)
    return 'ok'