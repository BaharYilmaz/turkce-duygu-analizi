# -*- coding: utf-8 -*-


import pandas as pd
from bs4 import BeautifulSoup 
import requests
import csv

yorumlar=[]

def getLink(link):
    
    pageCount =1
      
    link  = link + "-yorumlari?sayfa=" +str(pageCount)
    r = requests.get(link)
    
    
    soup = BeautifulSoup(r.content,"html.parser")
    gelen_veri2 = soup.find("div",{"class":"reviews-row"}).find("ul").find_all("li")
    sayi = len(gelen_veri2)
    
    while pageCount<sayi:
                    
        gelen_veri = soup.find_all("p",{"class":"review-text"})
        
        for yorum in gelen_veri:
            yorumlar.append(yorum.text)
            
        pageCount+=1
        link  = link + "-yorumlari?sayfa="
        link = link + str(pageCount)
        r = requests.get(link)
        
        soup = BeautifulSoup(r.content,"html.parser")
    
    print(yorumlar)
    
    appendYorum(yorumlar)
    return yorumlar
   
    #yeni df ve csv oluşturma
    #icerik=[]
    #icerik=1
    #urldata = pd.DataFrame(yorumlar)
    #urldata.columns = ["Yorum"]
    #urldata["Icerik"]=icerik
    #urldata = urldata.drop_duplicates()
    #urldata.to_csv('urldata.csv')
    
    
   
def appendYorum(yorumlar):
        with open('urldata.csv','w',newline='') as f:
            fieldname=['Yorum','Duygu']
            theWriter = csv.DictWriter(f,fieldnames=fieldname)
            
            
            theWriter.writeheader()
            for word in yorumlar:
                theWriter.writerow({'Yorum' : word , 'Duygu' : 1})
            yorumlar =[]
      
  
    
    
    
#url='https://www.hepsiburada.com/my-valice-diamond-abs-buyuk-boy-valiz-siyah-p-HBV00000E5K51'
#getLink(url)


  

    #yorum = pd.read_csv("urldata.csv",sep=",",encoding = "latin")
    #yorum = yorum.drop(['Index'], axis = 1)


