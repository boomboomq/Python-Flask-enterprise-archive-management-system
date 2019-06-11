# -*- coding=utf8 -*-
# 导入Flask库
import os
import base64
import time
from flask import Flask
import pymysql
from flask import request, redirect
from flask import render_template, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
db = SQLAlchemy()
import uuid
import logging
from flask import  Blueprint

# 导入MySQL库


app = Flask(__name__)
# 写好的数据库连接函数，
# 传入的是table，数据表的名称，
# 返回值是数据表中所有的数据，以元祖的格式返回


def get_table_data(table):                                # 定义获取数据库表的方法
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='lzq139520',
        db='new_schema', charset='utf8',
    )
    cur = conn.cursor()
    res = cur.execute("select * from " + table)
    res = cur.fetchmany(res)
    cur.close()
    conn.commit()
    conn.close()
    return res


# 启动服务器后运行的第一个函数，显示对应的网页内容
@app.route('/', methods=['GET', 'POST'])
def home():
    # return '<a href="/index"><h1 align="center">欢迎使用档案系统---点击进入</h1></a>'
    return render_template('login.html')


# 对登录的用户名和密码进行判断
@app.route('/login', methods=['POST'])
def login():
    # 需要从request对象读取表单内容：
    if request.form['username'] == 'em' and request.form['password'] == '1':
        return render_template('employee_index.html')
    if request.form['username'] == 'su' and request.form['password'] == '1':
        return render_template('supervisor_index.html')


@app.route('/employee_index', methods=['GET'])
def employee_index():
    return render_template('employee_index.html')


@app.route('/supervisor_index', methods=['GET'])
def supervisor_index():
    return render_template('supervisor_index.html')


@app.route('/supervisor', methods=['GET'])
def supervisor():
    return render_template('supervisor.html')


@app.route('/suparc', methods=['GET'])                   # 在管理员端获取职工档案信息
def suparc():
    # 调用数据库函数，获取数据
    data = get_table_data('emparc')
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        dict_data['e'] = value[4]
        dict_data['f'] = value[5]
        dict_data['g'] = value[6]
        dict_data['h'] = value[7]
        dict_data['i'] = value[8]
        dict_data['j'] = value[9]
        dict_data['k'] = value[10]
        dict_data['l'] = value[11]
        dict_data['m'] = value[12]
        posts.append(dict_data)
    # print posts
    return render_template('supervisor.html', posts=posts)


@app.route('/emarc', methods=['GET'])                               # 在职工端获取职工档案信息
def emarc():
    # 调用数据库函数，获取数据
    data = get_table_data('emparc')
    # 用列表的格式存放全部数据
    posts = []
    for value in data:            # 通过字典键值对把数据表中信息一列一列放到对应字典键中
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        dict_data['e'] = value[4]
        dict_data['f'] = value[5]
        dict_data['g'] = value[6]
        dict_data['h'] = value[7]
        dict_data['i'] = value[8]
        dict_data['j'] = value[9]
        dict_data['k'] = value[10]
        dict_data['l'] = value[11]
        dict_data['m'] = value[12]
        posts.append(dict_data)
    # print posts
    return render_template('employee.html', posts=posts)


@app.route('/empower', methods=['GET'])                   # 管理员端职位信息表
def empower():
    # 调用数据库函数，获取数据
    data = get_table_data('empower')
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        posts.append(dict_data)
    # print posts
    return render_template('empowerer.html', posts=posts)


@app.route('/lowempowerr', methods=['GET'])                    # 职工端职位信息表
def lowempowerr():
    # 调用数据库函数，获取数据
    data = get_table_data('empower')
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]

        posts.append(dict_data)
    # print posts
    return render_template('lowempower.html', posts=posts)


@app.route('/gongzi', methods=['GET'])                    # 职工端职位信息表
def gongzi():
    # 调用数据库函数，获取数据
    data = get_table_data('gongzi')
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        posts.append(dict_data)
    # print posts
    return render_template('gongzi.html', posts=posts)


@app.route('/powerman', methods=['GET'])              # 拥有管理员权限的职员表
def powerman():
    # 调用数据库函数，获取数据
    data = get_table_data('powerman')
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        dict_data['e'] = value[4]

        posts.append(dict_data)
    # print posts
    return render_template('powermanman.html', posts=posts)


@app.route('/upload', methods=['GET', 'POST'])               # 管理员上传文件到本地的功能
def upload():
    if request.method == 'POST':
        # 获取到用户上传的文件对象
        f = request.files['file']
        print(f.filename)
        # 获取当前项目所在目录位置；
        basepath = os.path.dirname(__file__)
        print(basepath)
        # 拼接路径， 存储文件到static/face/xxxx
        filename = os.path.join(basepath, 'static/uploads', f.filename)
        f.save(filename)
        return render_template('supervisor_index.html')


@app.route('/upload2', methods=['GET', 'POST'])               # 职工上传文件到本地
def upload2():
    if request.method == 'POST':
        # 获取到用户上传的文件对象
        f = request.files['file']
        print(f.filename)
        # 获取当前项目所在目录位置；
        basepath = os.path.dirname(__file__)
        print(basepath)
        # 拼接路径， 存储文件到static/face/xxxx
        filename = os.path.join(basepath, 'static/uploads', f.filename)
        f.save(filename)
        return render_template('employee_index.html')


@app.route('/update')                              # 跳转到添加信息页面
def update():
    return render_template('update.html')


@app.route('/tupian')                              # 跳转到添加信息页面
def tupian():
    return render_template('tupian.html')


@app.route('/save', methods={'post'})                     # 将添加的信息进行保存
def save():
    idd = request.form.get('id')
    a = request.form.get('a')
    b = request.form.get('b')
    c = request.form.get('c')
    d = request.form.get('d')
    e = request.form.get('e')
    f = request.form.get('f')
    g = request.form.get('g')
    h = request.form.get('h')
    i = request.form.get('i')
    k = request.form.get('k')
    lll = request.form.get('l')
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='lzq139520',
        db='new_schema', charset='utf8',
    )
    cur = conn.cursor()
    sql = "insert into emparc(id,a,b,c,d,e,f,g,h,i,k,l)values " \
          "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
          % (idd, a, b, c, d, e, f, g, h, i, k, lll)

    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    return render_template('supervisor_index.html')


@app.route('/delete', methods=('POST', 'GET'))                     # 管理员删除职工信息功能
def delete():
    li = request.args.get('a')
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='lzq139520',
        db='new_schema', charset='utf8',
    )
    cur = conn.cursor()
    sql = "delete from emparc where id = '%s'" % li
    sql2 = "delete from powerman where id = '%s'" % li
    cur.execute(sql)
    cur.execute(sql2)
    cur.close()
    conn.commit()
    conn.close()
    return render_template('supervisor_index.html')


@app.route('/deletep', methods=('POST', 'GET'))               # 管理员删除职位信息功能
def deletep():
    li = request.args.get('a')
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='lzq139520',
        db='new_schema', charset='utf8',
    )
    cur = conn.cursor()
    sql = "delete from empower where id = '%s'" % li
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    return render_template('supervisor_index.html')


@app.route('/edittest', methods=['GET'])                   # 在管理员端获取职工档案信息进行修改
def edittest():
    # 调用数据库函数，获取数据
    data = get_table_data('emparc')
    return render_template('edittest.html', posts=data)


@app.route('/edit', methods=['GET'])                   # 在管理员端获取职工档案信息进行修改
def edit():
    # 调用数据库函数，获取数据
    data = get_table_data('emparc')

    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        dict_data['e'] = value[4]
        dict_data['f'] = value[5]
        dict_data['g'] = value[6]
        dict_data['h'] = value[7]
        dict_data['i'] = value[8]
        dict_data['j'] = value[9]
        dict_data['k'] = value[10]
        dict_data['l'] = value[11]
        dict_data['m'] = value[12]
        posts.append(dict_data)
    # print posts
    return render_template('edit.html', posts=posts)


@app.route('/editsave', methods={'post'})                     # 将修改的信息进行保存
def editsave():
    idd = request.form.get('id')
    a = request.form.get('a')
    b = request.form.get('b')
    c = request.form.get('c')
    d = request.form.get('d')
    e = request.form.get('e')
    f = request.form.get('f')
    g = request.form.get('g')
    h = request.form.get('h')
    i = request.form.get('i')
    k = request.form.get('k')
    lll = request.form.get('l')

    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='lzq139520',
        db='new_schema', charset='utf8',
    )
    cur = conn.cursor()
    sql = "update emparc set a= '%s',b= '%s',c= '%s',d= '%s',e= '%s',f= '%s',g= '%s'," \
          "h= '%s',i= '%s',k= '%s',l= '%s' where id = '%s'" % (a, b, c, d, e, f, g, h, i, k, lll, idd)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    return render_template('supervisor_index.html')


@app.route('/search', methods=('POST', 'GET'))               # 管理员搜索职工信息功能
def search():
    s = request.form.get('s')
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='lzq139520',
        db='new_schema', charset='utf8',
    )
    cur = conn.cursor()
    sql = "select * from emparc where b like '%%%%%s%%%%'" % s
    res = cur.execute(sql)
    r = cur.fetchmany(res)
    posts = []
    for value in r:  # 通过字典键值对把数据表中信息一列一列放到对应字典键中
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        dict_data['e'] = value[4]
        dict_data['f'] = value[5]
        dict_data['g'] = value[6]
        dict_data['h'] = value[7]
        dict_data['i'] = value[8]
        dict_data['j'] = value[9]
        dict_data['k'] = value[10]
        dict_data['l'] = value[11]
        dict_data['m'] = value[12]
        posts.append(dict_data)
    cur.close()
    conn.commit()
    conn.close()
    return render_template('getsearch.html', posts=posts)


@app.route('/search2', methods=('POST', 'GET'))               # 职工搜索职工信息功能
def search2():
    s = request.form.get('s')
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='lzq139520',
        db='new_schema', charset='utf8',
    )
    cur = conn.cursor()
    sql = "select * from emparc where b like '%%%%%s%%%%'" % s
    res = cur.execute(sql)
    r = cur.fetchmany(res)
    posts = []
    for value in r:  # 通过字典键值对把数据表中信息一列一列放到对应字典键中
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        dict_data['e'] = value[4]
        dict_data['f'] = value[5]
        dict_data['g'] = value[6]
        dict_data['h'] = value[7]
        dict_data['i'] = value[8]
        dict_data['j'] = value[9]
        dict_data['k'] = value[10]
        dict_data['l'] = value[11]
        dict_data['m'] = value[12]
        posts.append(dict_data)
    cur.close()
    conn.commit()
    conn.close()
    return render_template('emgetsearch.html', posts=posts)


# 主函数
if __name__ == '__main__':
    # app.debug = True
    app.run()


