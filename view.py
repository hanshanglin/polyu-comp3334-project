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
    table = [('Website', 'Username', 'Password', 'Note'),
             ('1', '2', '3', '4')]

    print('mytable')
    data = json.dumps(table)
    print(data)
    return data


@app.route('/myform', methods=['POST'])
def myform():
    print('post')
    a = request.form['Website']
    b = request.form['Username']
    c = request.form['Password']
    d = request.form['Note']

    data = {'website': a,
            'Username': b,
            'Password': c,
            'Note': d}
    return jsonify(data)


if __name__ == '__main__':
    app.run()
