# @Version  : 1.0
# @Author   : 故河
from flask import Blueprint
auth = Blueprint("auth", __name__)

from picture_system import db, User, app
from .auth import *