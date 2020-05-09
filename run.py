from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
from User import User
from Form import RegisterForm
import json
import os


Userdict = {}


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def loginpage():
    return render_template('logintest.html')


@app.route('/register')
def register():
    #form = RegisterForm()
    # if form.validate_on_submit():
    #   user_name = request.form.get('username', None)
    #    password = request.form.get('password', None)
    #    user = User(user_name)
    #    user.password(password)
    #    return redirect(url_for('login'))
    # return render_template('registert.html',form = form)
    return render_template('registertest.html')


@app.route('/indextest')
def index():
    return render_template('indextest.html')


@app.route('/check', methods=['POST'])
def login():
    #print('post')
    #print(Userdict)
    # dataform {'username': 'xxx', 'password': 'xxx'}
    username = request.form['username']
    password = request.form['password']
    if (username in Userdict.keys() and Userdict[username] == password):
        print('suc')
        s = {'status': 'success', 'msg': 'login successfully'}
        return jsonify(s)
    else:
        print('fail')
        f = {'status': 'fail', 'msg': 'login fail'}
        return jsonify(f)


@app.route('/regist', methods=['POST'])
def regist():
    #print('regist')
    # dataform {'username': 'xxx', 'password': 'xxx', 'repassword': 'xxx'}
    username = request.form['username']
    password = request.form['password']
    repassword = request.form['repassword']
    if (password != repassword):
        print('fail')
        f = {'status': 'fail', 'msg': 'different password'}
        return jsonify(f)
    if (username in Userdict.keys()):
        print('fail')
        f = {'status': 'fail', 'msg': 'user exist'}
        return jsonify(f)
    Userdict[username] = password
    return {'status': 'success', 'msg': 'regist successfully'}




if __name__ == '__main__':
    app.run()
