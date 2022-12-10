from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca=certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.4ltayve.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.project4

SECRET_KEY = 'project4'

import datetime
import hashlib

@app.route('/')
def home():
    return render_template('join.html')

@app.route('/idcheck', methods=['POST'])
def idcheck():

    id_receive = request.form['id_give']
    idcheck = db.member.find_one({'id':id_receive},{'_id': False})

    if idcheck is None :
        id_duplicate_check = True
        return jsonify({'msg': '사용할 수 있는 아이디 입니다.', 'id_duplicate_check':id_duplicate_check})
    else:
        idcheck = idcheck['id']
        if idcheck == id_receive:
            id_duplicate_check = False
            return jsonify({'msg': '이미 존재하는 아이디입니다.','id_duplicate_check':id_duplicate_check})


@app.route('/signup', methods=['POST'])
def signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    db.member.insert_one({'id': id_receive, 'pw': pw_receive, 'nick': nickname_receive})

    return jsonify({'result': 'success'})

    return render_template('join.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)