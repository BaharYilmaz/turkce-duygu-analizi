# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 13:25:59 2019

@author: BAHAR
"""

import numpy as np
import pandas as pd
import webScraping as scrab
from flask import Flask, request, jsonify, render_template,url_for,session,redirect
import json 

app=Flask(__name__,template_folder="templates")


@app.route('/')
def home():
    return render_template('yorumCek.html')

@app.route('/yorumCek',methods=['POST'])
def yorumCek():
    link=""
    json_=request.json[0]['link']
    leng=len(request.json[0]['link'])
    index = 0
    while index < leng:
        letter = json_[index]
        link+=letter
        index += 1
    print(link)
   
    yorum = scrab.getLink(link)
    yorumCek= jsonify(yorum)
    response = app.response_class(response=json.dumps(yorumCek),mimetype='application/json')
    return str(yorumCek)


       
if __name__ == '__main__':

    app.run(debug=True)  

