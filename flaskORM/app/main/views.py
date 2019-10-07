import os
import json
import hashlib
import datetime
import functools

from flask import jsonify
from flask import session
from flask import request
from flask import redirect
from flask import render_template

from app.models import *
from . import main
from .forms import TaskForm
from app import api
from flask_restful import Resource



class Calendar:
    """
    当前类实现日历功能
    1、返回列表嵌套列表的日历
    2、安装日历格式打印日历

    # 如果一号周周一那么第一行1-7号   0
        # 如果一号周周二那么第一行empty*1+1-6号  1
        # 如果一号周周三那么第一行empty*2+1-5号  2
        # 如果一号周周四那么第一行empty*3+1-4号  3
        # 如果一号周周五那么第一行empyt*4+1-3号  4
        # 如果一号周周六那么第一行empty*5+1-2号  5
        # 如果一号周日那么第一行empty*6+1号   6
        # 输入 1月
        # 得到1月1号是周几
        # [] 填充7个元素 索引0对应周一
        # 返回列表
        # day_range 1-30
    """
    def __init__(self,month = "now"):
        self.result = []

        big_month = [1, 3, 5, 7, 8, 10, 12]
        small_month = [4, 6, 9, 11]

        #获取当前月
        now = datetime.datetime.now()
        if month == "now":
            month = now.month
            first_date = datetime.datetime(now.year, now.month, 1, 0, 0)
            # 年 月 日 时 分
        else:
            #assert int(month) in range(1,13)
            first_date = datetime.datetime(now.year, month, 1, 0, 0)

        if month in big_month:
            day_range = range(1, 32)  # 指定月份的总天数
        elif month in small_month:
            day_range = range(1, 31)
        else:
            day_range = range(1, 29)

        # 获取指定月天数
        self.day_range = list(day_range)
        first_week = first_date.weekday()  # 获取指定月1号是周几 6

        line1 = []  # 第一行数据
        for e in range(first_week):
            line1.append("empty")
        for d in range(7 - first_week):
            line1.append(
                str(self.day_range.pop(0))+"—曼联--曼城"
                         )
        self.result.append(line1)
        while self.day_range:  # 如果总天数列表有值，就接着循环
            line = []  # 每个子列表
            for i in range(7):
                if len(line) < 7 and self.day_range:
                    line.append(str(self.day_range.pop(0))+"—曼联--曼城")
                else:
                    line.append("empty")
            self.result.append(line)
    def return_month(self):
        """
        返回列表嵌套列表的日历
        """
        return self.result
    def print_month(self):
        """
        安装日历格式打印日历
        """
        print("星期一  星期二  星期三  星期四  星期五  星期六  星期日")
        for line in self.result:
            for day in line:
                day = day.center(6)
                print(day, end="  ")
            print()

class Paginator:
    def __init__(self,data,page_size):
        self.data = data
        self.page_size = page_size
        self.is_start = False
        self.is_end = False
        self.page_count = len(self.data)
        self.next_page = 0
        self.previous_page = 0
        self.page_number = (len(self.data) + self.page_size -1)//self.page_size
        self.page_range = range(1,self.page_number+1)

    def page_data(self,page):
        self.next_page = int(page) + 1
        self.previous_page = int(page) - 1
        if page<= self.page_range[-1]:
            page_start = (page-1)*self.page_size
            page_end = page*self.page_size
            data = self.data[page_start:page_end]
            if page == 1:
                self.is_start = True
            if page == self.page_range[-1]:
                self.is_end = True
        else:
            data = ["没有数据"]
        return data

def loginValid(fun):
    @functools.wraps(fun)#保留原函数的名称
    def inner(*args,**kwargs):
        username = request.cookies.get("username")
        id = request.cookies.get("id","0")
        user = User.query.get(int(id))
        session_username = session.get("username")
        if user:
            if user.user_name == username and username == session_username:
                return fun(*args,**kwargs)
            else:
                return redirect("/login/")
        else:
            return redirect("/login/")
    return inner
@main.route("/")
def index():
    name = "laobian"
    return render_template("index.html",**locals())

@main.route("/login/",methods=["post","get"])
def login():
    error = ""
    if request.method == "POST":
        form_data = request.form
        email = form_data.get("email")
        password = form_data.get("password")

        user = User.query.filter_by(email = email).first()
        if user:
            db_password = user.password
            if password == db_password:
                response = redirect('/index/')
                response.set_cookie("username",user.user_name)
                response.set_cookie("email",user.email)
                response.set_cookie("id",str(user.id))
                session["username"] = user.user_name
                return response
            else:
                error = "密码错误"
        else:
            error = "用户名不存在"
    return render_template("login.html",error = error)

@main.route("/logout/")
def logout():
    response = redirect("/login/")
    response.delete_cookie("username")
    response.delete_cookie("email")
    response.delete_cookie("id")
    session.pop("username")
    return response

@main.route("/base/")
def base():
    return render_template("base.html")

@main.route("/index/",methods=["get","post"])
@loginValid
def exindex():
    # c = Curriculum()
    # c.c_id = "0001"
    # c.c_name = "python基础"
    # c.c_time = datetime.datetime.now()
    # c.save()
    curr_list = Curriculum.query.all()
    return render_template("index.html",curr_list = curr_list)
import time
@main.route("/userinfo/")
def userinfo():
    calendar = Calendar().return_month()
    now = datetime.datetime.now()
    return render_template("userinfo.html",**locals())

@main.route("/register/",methods=["GET","POST"])
def register():
    """
    form 表单提交的数据由request.form接受
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        user = User()
        user.user_name = username
        user.password = password
        user.email = email
        user.save()
    return render_template("register.html")

@main.route("/vacationTip/",methods=["post","get"])
# @csrf.exempt
def vacationTip():
    if request.method == "POST":
        id = request.form.get("id")
        username = request.form.get("vacation_name")
        vacation_type = request.form.get("vacation_type")
        vacation_start = request.form.get("vacation_start")
        vacation_deadline = request.form.get("vacation_deadline")
        vacation_day = request.form.get("vacation_day")
        vacation_phone = request.form.get("vacation_phone")
        vacation_description = request.form.get("vacation_description")

        tip = VacationTip()
        tip.vacation_id = request.cookies.get("id")
        tip.vacation_name = username
        tip.vacation_type = vacation_type
        tip.vacation_start = vacation_start
        tip.vacation_deadline = vacation_deadline
        tip.vacation_day = vacation_day
        tip.vacation_phone = vacation_phone
        tip.vacation_status = "0"
        tip.vacation_description = vacation_description
        tip.save()
        return redirect("/vacationTip_list/")
    return render_template("vacationTip.html")

@main.route("/vacationTip_list/<int:page>/")
@loginValid
def vacationTip_list(page):
    tips = VacationTip.query.all()
    paginators = Paginator(tips,2)
    page_data = paginators.page_data(page)
    return render_template("vacationTip_list.html",**locals())

@main.route("/add_task/",methods=["GET","POST"])
def add_task():
    """
    print(task.errors)表单校验错误
    print(task.validate_on_submit()) 判断是否是一个有效的post请求
    print(task.validate()) 判断是否是一个合法的post请求
    print(task.data) 提交的数据
    :return:
    """
    error = ""
    task = TaskForm()
    if request.method == "POST":
        if task.validate_on_submit():#判断是否是一个有效的post请求
            formData = task.data
        else:
            errors_list = list(task.errors.keys())
            errors = task.errors
            print(errors)
    return render_template("add_task.html",**locals())


import json
from flask import jsonify

@main.route("/cancel/",methods=["GET","POST"])
def cancel():
    id = request.form.get("vacation_id")#通过args接受get请求数据
    vacationtip = VacationTip.query.get(int(id))
    vacationtip.delete()
    return jsonify({"data":"删除成功"}) #返回json数据

@api.resource("/Api/vacationTip/")
class VacationTipApi(Resource):
    def __init__(self):
        super(VacationTipApi,self).__init__()
        self.result = {
            "version":"1.0",
            "data":""
        }
    def set_data(self,vacationTip):
        result_data = {
            "vacation_name":vacationTip.vacation_name,
            "vacation_type":vacationTip.vacation_type,
            "vacation_start":vacationTip.vacation_start,
            "vacation_deadline":vacationTip.vacation_deadline,
            "vacation_description":vacationTip.vacation_description,
            "vacation_phone":vacationTip.vacation_phone
        }
        return result_data

    def get(self):
        data = request.args
        id = data.get("id")
        if id:
            vacationtip = VacationTip.query.get(int(id))
            result_data = self.set_data(vacationtip)
        else:
            vacationtips = VacationTip.query.all()
            result_data = []
            for vacationtip in vacationtips:
                result_data.append(self.set_data(vacationtip))
        self.result["data"] = result_data
        return self.result
    def post(self):
        data = request.form
        vacation_id = data.get("vacation_id")
        vacation_name = data.get("vacation_name")
        vacation_type = data.get("vacation_type")
        vacation_start = data.get("vacation_start")
        vacation_deadline = data.get("vacation_deadline")
        vacation_description = data.get("vacation_description")
        vacation_phone = data.get("vacation_phone")

        vacationtip = VacationTip()
        vacationtip.vacation_id = vacation_id
        vacationtip.vacation_name = vacation_name
        vacationtip.vacation_type = vacation_type
        vacationtip.vacation_start = vacation_start
        vacationtip.vacation_deadline = vacation_deadline
        vacationtip.vacation_description = vacation_description
        vacationtip.vacation_phone = vacation_phone
        vacationtip.save()
        self.result["data"] = self.set_data(data)
        return self.result


    def put(self):
        data = request.form #请求数据
        id = data.get("id") #data的里id
        vacationtip = VacationTip.query.get(int(id))
        for key,value in data.items():
            if key != "id":
                setattr(vacationtip,key,value)
        vacationtip.save()
        self.result["data"] = self.set_data(vacationtip)
        return self.result
    def delete(self):
        data = request.form #请求数据，类字典对象
        id = data.get("id") #data里面的id
        vacationtip = VacationTip.query.get(int(id))
        vacationtip.delete()
        self.result["data"] = "%s删除成功"%id
        return self.result


@main.route("/tests/")
def tests():
    return render_template("tests.html")



