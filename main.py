from flask import Flask,url_for,render_template,request,redirect,jsonify,current_app
from flask_wtf.csrf import CsrfProtect
from User import User
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user
import os
from Form import LoginForm,RegisterForm
import json
from keychain import KeyChainStorage

app = Flask(__name__)

app.secret_key = os.urandom(24)
# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login' # default login page
login_manager.init_app(app=app)
login_manager.login_message=u'please login before'
login_manager.login_message_category='info'


# reload User object，by session->user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# csrf protection
csrf = CsrfProtect()
csrf.init_app(app)


@app.route('/',methods = ["POST","GET"])
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
    return render_template('login.html',form = form,User = current_user.is_authenticated )


@app.route("/test")
@login_required
def test_target():
    return "you are in"


@app.route('/getOtp/<filename>',methods = ["POST","GET"])
def OTP_download(filename):
    file_path = ".\\temp\\"+filename
    file_handle = open(file_path, 'r')

    def stream_and_remove_file():
        yield from file_handle
        file_handle.close()
        os.remove(file_path)

    return current_app.response_class(
        stream_and_remove_file(),
        headers={'Content-Disposition': 'attachment', 'filename': filename}
    )

@app.route('/view',methods=['POST','GET'])
@login_required
def view_page():
    return render_template("view.html")

@csrf.exempt
@app.route('/getKeyChain',methods=['POST','GET'])
@login_required
def request_key_chain():
    user = current_user._get_current_object()
    l = KeyChainStorage.get_keychain_item_list(user.keychain)
    res = {'status':"OK"}
    li = []
    for uuid,weburl,username,password,comment in l:
        tmp = {
            'uuid':uuid,
            'weburl':weburl,
            'username':username,
            'password':password,
            'comment':comment
        }
        li.append(tmp)
    res['data'] = li
    return jsonify(res)

@csrf.exempt
@app.route('/updateKeyChain',methods=['POST','GET'])
@login_required
def update_key_chain():
    user = current_user._get_current_object()
    des = user.keychain
    l = request.get_json()
    if l==None:
        return jsonify({'status':'ERR', 'msg':"No data found"})
    res = {'status':"ERR"}
    if l['type'] == 'ADD':
        # add
        uuid = KeyChainStorage.add_keychain_item(des,l['weburl'],l['username'],l['password'],l['comment'])
        return jsonify({
            'uuid':uuid,
            'weburl':l['weburl'],
            'username':l['username'],
            'password':l['password'],
            'comment':l['comment']
        }) 
    elif l['type'] == 'DEL':
        # del
        KeyChainStorage.delete_keychain_item(des,l['uuid'])
        return jsonify({}) 
    elif l['type'] == 'EDI':
        # update
        KeyChainStorage.update_keychain_item(des,l['uuid'],l['weburl'],l['username'],l['password'],l['comment'])
        return jsonify({
            'uuid':l['uuid'],
            'weburl':l['weburl'],
            'username':l['username'],
            'password':l['password'],
            'comment':l['comment']
        }) 
    return jsonify(res)

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
        return jsonify({'status':'OK','win':url_for("OTP_download",filename=user_name+".py"),'android':url_for('OTP_download',filename=user_name+'.apk')})
    return render_template('register.html',form = form,User = current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
