# @Version  : 1.0
# @Author   : 故河
from flask import Blueprint

blog = Blueprint('blog', __name__, template_folder='templates')

from .routes import *