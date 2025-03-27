# @Version  : 1.0
# @Author   : 故河
from flask import Blueprint
picture = Blueprint("picture", __name__)

from picture_system import db, Picture, PictureGroup
from .picture import *