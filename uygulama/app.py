# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.externals import joblib
from flask import Flask, request, jsonify, render_template,url_for,session,redirect
import pickle
import json 
import model2 as m
from werkzeug.security import check_password_hash
from pymongo import MongoClient
#import database

client = MongoClient()
client = MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb')
db = client['userDb']
collection = db['user']
app = Flask(__name__)
app.secret_key = 'secretKey'


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login',methods=['GET'])
def loginGet():
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def loginPost():
      
    username_ = request.form['username']
    password_= request.form['password']
    print(username_)
    user =collection.find_one({"username":username_})
    pass_=user['password']
    print("find_one",pass_)

    if user:
        if password_==pass_:

            return render_template('predict.html')
        else:
            return redirect(url_for('loginGet'))

    else:
        return redirect(url_for('loginGet'))



@app.route('/predict',methods=['POST'])
def predict():
    if m:
        
        data=request.form['data']
        print(data)
        sonuc=m.analizEt(data)
        print("sonuc",sonuc)
        if sonuc==True:
            return render_template('predict.html', analiz='Olumlu Yorum')
        else:
            return render_template('predict.html', analiz='Olumsuz Yorum')

        
    else:
        print ('Train the model first')
        return ('No model here to use')   




@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect(url_for('base'))
    else:
        return redirect(url_for('login'))

@app.route('/signUp',methods=['GET'])
def signUpGet():
    return render_template('signUp.html')
    
  
@app.route('/signUp',methods=['POST'])
def signUpPost():

    users=db.user
    name_=request.form['name']
    username_ = request.form['username']
    password_= request.form['password']
    kullanici =collection.find_one({"username":username_})
    if kullanici:
        result=jsonify({"error":"Bu kullanıcı adı alınmış"})
        return redirect(url_for('singUp'))
    else:
        users.insert({

            'name':name_,
            'username':username_,
            'password':password_
        })
        result=jsonify({"success":"Kayıt Başarılı"})
        return render_template('predict.html')









@app.route('/index',methods=['POST'])
def index():

    #prediction
    json_ = request.json
    print("aa:"+json.dumps(json_)+"\n")
    text=json.dumps(json_)
    prediction = text
    resp= jsonify({'prediction':str(prediction)})
    response = app.response_class(response=json.dumps(prediction),mimetype='application/json')
    return str(prediction)

    
 
if __name__ == '__main__':
    
    app.run(debug=True)   