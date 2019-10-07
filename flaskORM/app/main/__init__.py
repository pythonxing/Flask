from flask import Blueprint
main = Blueprint("main",__name__)#创建蓝图
from . import views#这个导入执行之后，会执行整个views
