from flask import Flask,url_for,render_template,request,redirect,jsonify
from flask_wtf.csrf import CsrfProtect
from User import User
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user
import os
from Form import LoginForm,RegisterForm
import json

app = Flask(__name__)

app.secret_key = os.urandom(24)
# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login' # default login page
login_manager.init_app(app=app)

# reload User object，by session->user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# csrf protection
csrf = CsrfProtect()
csrf.init_app(app)


@app.route('/login',methods = ["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        dynamic = request.form.get('dynamic',None)
        user = User(user_name)
        if user.verify_password(password,dynamic):
            login_user(user)
            return jsonify({'status':'OK','msg':'login successfully'})
        else:
            return jsonify({'status':'ERR','msg':'password, password and OPT are not match'})
    return render_template('login.html',form = form)


@app.route("/test")
@login_required
def test_target():
    return "you are in"


@app.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        user = User(user_name)
        # if the register successfully, all info will save in profiles.json
        try:
            user.register_user(password)
        except Exception as e:
            return jsonify({'status':'ERR','msg':str(e)})

        return jsonify({'status':'OK','msg':'register successfully'})
    return render_template('register.html',form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
