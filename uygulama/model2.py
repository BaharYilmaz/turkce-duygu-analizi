# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pickle

yorumOlumlu = pd.read_csv("olumlu.csv",sep=",",encoding ='utf-8')
yorumOlumsuz = pd.read_csv("olumsuz.csv",sep=",",encoding ='utf-8')

yorumEksi=yorumOlumsuz.iloc[:230]
yorumArtı=yorumOlumlu.iloc[:230]

yorumlar=pd.concat([yorumEksi,yorumArtı])

x=yorumlar["Yorum"].copy()
y= yorumlar.iloc[:,-1].values.reshape(-1,1)
#yorumlar.columns=column

def remove_stopwords(df_fon):
    stopwords = open('turkce-stop-words', 'r').read().split()
    df_fon['stopwords_removed'] = list(map(lambda doc:
        [word for word in doc if word not in stopwords], df_fon['Yorum']))

remove_stopwords(yorumlar)



from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state = 42)

from sklearn.feature_extraction.text import CountVectorizer
vect = CountVectorizer(encoding ='utf-8').fit(X_train)

X_train_vectorized = vect.transform(X_train)

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train_vectorized, y_train)

from sklearn.metrics import roc_auc_score
predictions = model.predict(vect.transform(X_test))
print('AUC: ', roc_auc_score(y_test, predictions))


feature_names = np.array(vect.get_feature_names())
sorted_coef_index = model.coef_[0].argsort()
print('Negatif: \n{}\n'.format(feature_names[sorted_coef_index[:10]]))
print('Pozitif: \n{}\n'.format(feature_names[sorted_coef_index[:-11:-1]]))

from sklearn.feature_extraction.text import TfidfVectorizer
vect = TfidfVectorizer(min_df = 5).fit(X_train)

X_train_vectorized = vect.transform(X_train)
model = LogisticRegression()
model.fit(X_train_vectorized, y_train)
predictions = model.predict(vect.transform(X_test))
print('AUC: ', roc_auc_score(y_test, predictions)) 

vect = CountVectorizer(min_df = 5, ngram_range = (1,2)).fit(X_train)
X_train_vectorized = vect.transform(X_train)


model = LogisticRegression()
model.fit(X_train_vectorized, y_train)
predictions = model.predict(vect.transform(X_test))
print('AUC: ', roc_auc_score(y_test, predictions))

feature_names = np.array(vect.get_feature_names())
sorted_coef_index = model.coef_[0].argsort()
print('Negatif: \n{}\n'.format(feature_names[sorted_coef_index][:10]))
print('Pozitif Coef: \n{}\n'.format(feature_names[sorted_coef_index][:-11:-1]))


# Saving model to disk
pickle.dump(model, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))

def analizEt(yorum):
    sonuc=model.predict(vect.transform([yorum]))
    if sonuc==0:
        return False
    else:
        return True

#analizEt(yorum)

# while(True):
#     yorum=input("Yorumunuz Nedir?(Programdan çıkmak için \'F\' yazınız)")
#     if(yorum == 'F' or yorum == 'f'):
#         break
#     else:
#         print(model.predict(vect.transform([yorum])))                                                                                                                           