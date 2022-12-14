from flask import Flask, render_template, request, jsonify, session ,redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://toyNews:toyNews@cluster0.opg0fml.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

SECRET_KEY = 'project4'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime
import hashlib


############################################################################### 헬스장 크롤링
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%ED%97%AC%EC%8A%A4%EC%9E%A5', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

gyms = soup.select('#loc-main-section-root > section > div > ul > li')
db.gymtest.delete_many({})

for gym in gyms:
    if gym != None:
        gymTitle= gym.select_one('div.ouxiq.icT4K > a:nth-child(1) > div > div > span.place_bluelink.YwYLL').text
        gymLocation= gym.select_one('div.rDx68 > div > span > a > span.hClKF').text
        Desc= gym.select_one('div.ouxiq.icT4K > a:nth-child(3) > div > div > span.XP3ml.A2p8S')
        if Desc !=None:
            gymDesc = Desc.text
        else:
            gymDesc=""
        PhoneNumber= gym.select_one('div.ouxiq.icT4K > div.mqM2N.l8afP')
        if PhoneNumber !=None:
            gymPhoneNumber = PhoneNumber.text
        else:
            gymPhoneNumber=""

        category= 'gym'        
        doc ={
            'category': category,
            'Title':gymTitle,
            'Location':gymLocation,
            'Desc':gymDesc,
            'PhoneNumber':gymPhoneNumber
             }
        # 헬스장이름,위치,영업시간,전화번호 DB저장
        db.gymtest.insert_one(doc)  

################################################################################ 필라테스 크롤링
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%ED%95%84%EB%9D%BC%ED%85%8C%EC%8A%A4', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

pilateses = soup.select('#loc-main-section-root > section > div > ul > li')
# db.gymtest.delete_many({})

for pilates in pilateses:
    if pilates != None:
        pilatesTitle= pilates.select_one('div.ouxiq.icT4K > a:nth-child(1) > div > div > span.place_bluelink.YwYLL').text
        pilatesLocation= pilates.select_one('div.ouxiq.icT4K > div.rDx68 > div > span > a > span.hClKF').text
        Desc= pilates.select_one('div.ouxiq.icT4K > a:nth-child(3) > div > div > span:nth-child(2)')
        if Desc != None:
            pilatesDesc = Desc.text
        else:
            pilatesDesc = ""
        PhoneNumber= pilates.select_one('div.ouxiq.icT4K > div.mqM2N.l8afP')
        if PhoneNumber !=None:
            pilatesPhoneNumber = PhoneNumber.text
        else:
            pilatesPhoneNumber=""
        
        category= 'pilates'        
        doc ={
            'category': category,
            'Title':pilatesTitle,
            'Location':pilatesLocation,
            'Desc':pilatesDesc,
            'PhoneNumber':pilatesPhoneNumber
             }
        db.gymtest.insert_one(doc)

# 수영장 크롤링
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%88%98%EC%98%81%EC%9E%A5', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

swimming_pools = soup.select('#loc-main-section-root > section > div > ul > li')
# db.gymtest.delete_many({})

for swimming_pool in swimming_pools:
    if swimming_pool != None:
        swimming_poolTitle= swimming_pool.select_one('a:nth-child(1) > div > div > span.place_bluelink.YwYLL').text
        swimming_poolLocation= swimming_pool.select_one('div.rDx68 > div > span > a > span.hClKF').text
        Desc = swimming_pool.select_one('div.ouxiq.icT4K > a:nth-child(3) > div > div > span:nth-child(2)')
        if Desc is not None:
            swimming_poolDesc = Desc.text
        else:
            swimming_poolDesc = ""
        poolPhoneNumber = swimming_pool.select_one('div.mqM2N.l8afP')
        if poolPhoneNumber is not None:
            swimming_poolPhoneNumber = poolPhoneNumber.text
        else:
            swimming_poolPhoneNumber = ""
        category= 'swimming_pool'

        doc ={
            'category': category,
            'Title':swimming_poolTitle,
            'Location':swimming_poolLocation,
            'Desc':swimming_poolDesc,
            'PhoneNumber' : swimming_poolPhoneNumber
             }
        db.gymtest.insert_one(doc)

################################################################################ 크로스핏 크롤링
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%ED%81%AC%EB%A1%9C%EC%8A%A4%ED%95%8F&oquery=%ED%81%AC%EB%A1%9C%EC%8A%A4%ED%94%BD&tqi=hHju7wp0JywssdOuQplssssssgd-212890', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

crossfites = soup.select('#loc-main-section-root > section > div > ul > li')
# db.gymtest.delete_many({})

for crossfit in crossfites:
    if crossfit != None:
        crossfitTitle= crossfit.select_one('a:nth-child(1) > div > div > span.place_bluelink.YwYLL').text
        crossfitLocation= crossfit.select_one('div.rDx68 > div > span > a > span.hClKF').text
        Desc= crossfit.select_one('div.ouxiq.icT4K > a:nth-child(3) > div > div > span:nth-child(2)')
        if Desc != None:
            crossfitDesc = Desc.text
        else:
            crossfitDesc = ""
        PhoneNumber= crossfit.select_one('div.mqM2N.l8afP')
        if PhoneNumber !=None:
            crossfitPhoneNumber = PhoneNumber.text
        else:
            crossfitPhoneNumber=""
        
        category= 'crossfit'
        doc ={
            'category': category,
            'Title':crossfitTitle,
            'Location':crossfitLocation,
            'Desc':crossfitDesc,
            'PhoneNumber':crossfitPhoneNumber
             }
        db.gymtest.insert_one(doc)





# 클라이밍 크롤링
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%ED%81%B4%EB%9D%BC%EC%9D%B4%EB%B0%8D', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

climbings = soup.select('#loc-main-section-root > section > div > ul > li')
# db.gymtest.delete_many({})

for climbing in climbings:
    if climbing != None:
        climbingTitle= climbing.select_one('a:nth-child(1) > div > div > span.place_bluelink.YwYLL').text
        climbingLocation= climbing.select_one('div.rDx68 > div > span > a > span.hClKF').text
        Desc= climbing.select_one('div.ouxiq.icT4K > a:nth-child(3) > div > div > span:nth-child(2)')
        if Desc != None:
            climbingDesc = Desc.text
        else:
            climbingDesc = ""
        PhoneNumber= climbing.select_one('div.mqM2N.l8afP')
        if PhoneNumber !=None:
            climbingPhoneNumber = PhoneNumber.text
        else:
            climbingPhoneNumber=""     
        
        category= 'climbing'
        doc ={
            'category': category,
            'Title':climbingTitle,
            'Location':climbingLocation,
            'Desc':climbingDesc,
            'PhoneNumber':climbingPhoneNumber
             }
        db.gymtest.insert_one(doc)











# 시작페이지=로그인페이지
@app.route('/')
def home():
    return render_template('login.html')

# /회원가입페이지
@app.route('/join')
def join():
    return render_template('join.html')
# 메인페이지
@app.route('/main')
def main():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.member.find_one({"id": payload['id']})
        return render_template('main.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("join", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("join", msg="로그인 정보가 존재하지 않습니다."))
    
    # return render_template('main.html')        


#############################################################################로그인
# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST','GET'])
def api_login():
    if request.method == 'POST' :
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']

        # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

        # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
        result = db.member.find_one({'id': id_receive, 'pw': pw_hash})

        # 찾으면 JWT 토큰을 만들어 발급합니다.
        if result is not None:
            # JWT 토큰에는, payload와 시크릿키가 필요합니다.
            # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
            # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
            # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
            payload = {
                'id': id_receive,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes= 300)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            # token을 줍니다.
            return jsonify({'result': 'success', 'token': token})
        # 찾지 못하면
        else:
            return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
    else : return render_template('login.html')


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.member.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})        


#############################################################################회원가입
# 아이디체크
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


# 회원가입등록
@app.route('/signup', methods=['POST'])
def signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.member.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})

######################################################################## 헬스장 리스트표시
@app.route("/gyms", methods=["GET"])
def gym_get():
    gymsList = list(db.gymtest.find({'category':'gym'},{'_id':False}))
    
    
    return jsonify({'gymsList':gymsList})



######################################################################## 필라테스 리스트표시
@app.route("/pilates", methods=["GET"])
def pilates_get():
    pilatesList = list(db.gymtest.find({'category':'pilates'},{'_id':False}))
    
    
    return jsonify({'gymsList':pilatesList})


######################################################################## 크로스핏 리스트표시
@app.route("/crossfit", methods=["GET"])
def crossfit_get():
    crossfitList = list(db.gymtest.find({'category':'crossfit'},{'_id':False}))
    
    
    return jsonify({'gymsList':crossfitList})


########################################################################### 수영장 리스트표시
@app.route("/swimming_pool", methods=["GET"])
def swimming_pool_get():
    swimming_poolList = list(db.gymtest.find({'category':'swimming_pool'},{'_id':False}))
    
    
    return jsonify({'gymsList':swimming_poolList})


#####FIXME:################################################################### 클라이밍 리스트표시
@app.route("/climbing", methods=["GET"])
def climbing_get():
    climbingList = list(db.gymtest.find({'category':'climbing'},{'_id':False}))
    
    
    return jsonify({'gymsList':climbingList})    


#####################################################이름,코멘트 저장,로그인닉네임 
@app.route('/comment', methods=['POST'])
def comment_save():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    nick_receive = request.form['nick_give']
    category_receive = request.form['category_give']
    doc = {'category':category_receive,'title': title_receive,'comment':comment_receive,'nick':nick_receive}
    db.gymComment.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

####################################################### 헬스장 id,코멘트 표시
@app.route("/comment", methods=["GET"])
def gym_comment_show():
    gymCommentList = list(db.gymComment.find({'category':'gym'},{'_id':False}))
    
    return jsonify({'gymCommentList':gymCommentList})    


####################################################### 필라테스 id,코멘트 표시
@app.route("/pila_comment", methods=["GET"])
def pilates_comment_show():
    gymCommentList = list(db.gymComment.find({'category':'pilates'},{'_id':False}))
    
    return jsonify({'gymCommentList':gymCommentList})

####################################################### 크로스핏 id,코멘트 표시
@app.route("/crossfit_comment", methods=["GET"])
def crossfit_comment_show():
    gymCommentList = list(db.gymComment.find({'category':'crossfit'},{'_id':False}))
    
    return jsonify({'gymCommentList':gymCommentList})


####################################################### 크로스핏 id,코멘트 표시
@app.route("/swimming_pool_comment", methods=["GET"])
def swimming_pool_comment_show():
    gymCommentList = list(db.gymComment.find({'category':'swimming_pool'},{'_id':False}))
    
    return jsonify({'gymCommentList':gymCommentList})


####################################################### 크로스핏 id,코멘트 표시
@app.route("/climbing_comment", methods=["GET"])
def climbing_comment_show():
    gymCommentList = list(db.gymComment.find({'category':'climbing'},{'_id':False}))
    
    return jsonify({'gymCommentList':gymCommentList})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)