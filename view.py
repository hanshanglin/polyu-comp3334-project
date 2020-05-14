from flask import Flask, render_template, request
from flask import jsonify
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "123123"


@app.route('/')
def view():
    return render_template('view.html')


@app.route('/mytable')
def mytable():
    table = [('ID', 'Website', 'Username', 'Password', 'Note'),
             ('xxxxx', '1', '2', '3', '4')]

    data = json.dumps(table)
    print(data)
    return data


@app.route('/add', methods=['POST'])
def myform():
    a = request.form['Website']
    b = request.form['Username']
    c = request.form['Password']
    d = request.form['Note']

    data = {'website': a,
            'username': b,
            'password': c,
            'note': d}
    return jsonify(data)


@app.route('/delete', methods=['POST'])
def delete():
    uuid = request.form['Id']
    return jsonify({'uuid': uuid})

@app.route('/modify', methods=['POST'])
def modify():
    a = request.form['MWebsite']
    b = request.form['MUsername']
    c = request.form['MPassword']
    d = request.form['MNote']
    uuid = request.form['MId']

    data = {'uuid': uuid,
            'website':a,
            'username': b,
            'password': c,
            'note': d}
    return jsonify(data)

if __name__ == '__main__':
    app.run()
