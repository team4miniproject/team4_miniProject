from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://toyNews:toyNews@cluster0.opg0fml.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta


import requests
from bs4 import BeautifulSoup

# 헬스장 완료
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%ED%97%AC%EC%8A%A4%EC%9E%A5', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

gyms = soup.select('#loc-main-section-root > section > div > ul > li')
db.gym.delete_many({})

for gym in gyms:
    if gym != None:
        gymTitle= gym.select_one('div.ouxiq.icT4K > a:nth-child(1) > div > div > span.place_bluelink.YwYLL').text
        gymLocation= gym.select_one('div.rDx68 > div > span > a > span.hClKF').text
        gymDesc= gym.select_one('div.ouxiq.icT4K > a:nth-child(3) > div > div > span.XP3ml.A2p8S').text
        # gymImage= gym.select_one('div.TTfa9 > a > div > img')
        gymPhoneNumber= gym.select_one('div.ouxiq.icT4K > div.mqM2N.l8afP').text
                
        # if gymImage != None:
        #    gym_image = gymImage
        # else:
        #     gym_image =""
           
        # print(gymTitle)
        # print(gymLocation)
        # print(gymDesc)
        # print(gymPhoneNumber)
        # print(gym_image)

        doc ={
            'gym_Title':gymTitle,
            'gym_Location':gymLocation,
            'gym_Desc':gymDesc,
            'gym_PhoneNumber':gymPhoneNumber
             }


        db.gym.insert_one(doc)        
        

@app.route('/')
def home():
    return render_template('main.html')

# 
# gym get방식
@app.route("/gyms", methods=["GET"])
def gym_get():
    gymsList = list(db.gym.find({},{'_id':False}))
   
    print(gymsList)
     
    
    return jsonify({'gymsList':gymsList})    



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
        


# 전화번호
#loc-main-section-root > section > div > ul > li:nth-child(3) > div.ouxiq.icT4K > div.mqM2N.l8afP
#loc-main-section-root > section > div > ul > li:nth-child(4) > div.ouxiq.icT4K > div.mqM2N.l8afP

# 내용
#loc-main-section-root > section > div > ul > li:nth-child(1) > div.ouxiq.icT4K > a:nth-child(3) > div > div > span.XP3ml.A2p8S
#loc-main-section-root > section > div > ul > li:nth-child(6) > div.ouxiq.icT4K > a:nth-child(3) > div > div > span.XP3ml.A2p8S

# 이미지
#loc-main-section-root > section > div > ul > li:nth-child(3) > div.TTfa9 > a
#loc-main-section-root > section > div > ul > li:nth-child(4) > div.TTfa9 > a
#loc-main-section-root > section > div > ul > li:nth-child(3) > div.TTfa9 > a > div > img
#loc-main-section-root > section > div > ul > li:nth-child(3) > div.TTfa9 > a > div > img
#loc-main-section-root > section > div > ul > li:nth-child(5) > div.TTfa9 > a > div > img
#loc-main-section-root > section > div > ul > li:nth-child(1) > div.TTfa9 > a
#loc-main-section-root > section > div > ul > li:nth-child(1) > div.TTfa9 > a > div > img


# 타이틀
#loc-main-section-root > section > div > ul > li:nth-child(1) > div.ouxiq.icT4K > a:nth-child(1) > div.ApCpt > div > span.place_bluelink.YwYLL
#loc-main-section-root > section > div > ul > li:nth-child(2) > div.ouxiq.icT4K > a:nth-child(1) > div.ApCpt > div > span.place_bluelink.YwYLL
#loc-main-section-root > section > div > ul > li:nth-child(3) > div.ouxiq.icT4K > a:nth-child(1) > div > div > span.place_bluelink.YwYLL
#loc-main-section-root > section > div > ul > li:nth-child(3) > div.ouxiq.icT4K > a:nth-child(1) > div > div > span.place_bluelink.YwYLL
# 위치
#loc-main-section-root > section > div > ul > li:nth-child(2) > div.ouxiq > div.rDx68 > div > span > a > span.hClKF
#loc-main-section-root > section > div > ul > li:nth-child(3) > div.ouxiq.icT4K > div.rDx68 > div > span > a > span.hClKF
        # doc = {
        #     'politics_title':politicsTitle,
        #     'politics_link':politicsLink,
        #     'politics_image':politics_image,
        #     'politics_desc':politicsDesc
        #     }
        
        # db.gym.insert_one(doc)

# @app.route('/')
# def home():
#     return render_template('index.html')




    

