# -*- coding: utf-8 -*-
"""url_phishing_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FHFPyx2LKXnqi868SdYED2BSKK7gQZjQ

# **Pendahuluan**


---

Phising Detected adalah proyek model machine learning untuk mengidentifikasi website phising. Phising merupakan suatu kejahatan yang cukup sering terjadi dimanapun. Salah satu penyebabnya adalah kurangnya pengetahuan dan kesadaran masyarakat dalam membedakan antara website resmi dan website phising. Oleh karena itu diperlukan suatu media yang dapat mengidentifikasi website phising untuk masyarakat. Salah satu media yang dapat digunakan adalah sebuah website phising detected yang dapat diakses melalui desktop maupun smartphone dan menurut kami ini adalah kesempatan yang baik untuk mengedukasi masyarakat melalui website ini karena mudah untuk diakses oleh siapapun

# **Data Understanding**
---
Data yang digunakan pada model ini adalah data web phishing dari kaggle.

kaggle datasets download -d taruntiwarihp/phishing-site-urlskaggle datasets

Url sumber data : [Dataset kaggle : Phishing Site Urls](https://www.kaggle.com/taruntiwarihp/phishing-site-urls)

### Import Library
---
Pada bagian ini kami mengimport semua library yang dibutuhkan pada pembuatan model prediksi.
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
import time
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import networkx as next
import pickle
import warnings
warnings.filterwarnings('ignore')

"""### Mempersiapkan Dataset
---
Pada bagian ini saya mendownload dataset langsung dari kaggle kemudian menampilkannya, dataset yang saya gunakan yaitu phishing_site_urls.csv
"""

drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/Dataset_Phishing.csv')
df

"""# **Exploratory Data Analysis**
---
tahap eksplorasi dilakukan untuk mendapatkan insight dari dataset

### Deskripsi Variabel
---
Pada dataset ini terdapat 2 variabel yaitu URL merepresentasikan alamat link dan Label merepresentasikan apakah link dikategorikan bad/good.

**Penjelasan** : `df.describe()` dan `df.info()` digunakan untuk mendapatkan informasi dataframe.
"""

df.info()

df.describe()

"""### Visualisasi Data
---

untuk masalah klasifikasi kita melakukan pengecekan terlebih dahulu, apakah kelasnya seimbang atau tidak.
"""

label_counts = pd.DataFrame(df.Label.value_counts())

sns.set_style('darkgrid')
sns.barplot(label_counts.index,label_counts.Label)

"""# **Data Preparation**
---

### Menangani Missing Value
---
"""

df.isnull().sum()

"""setelah melakukan pengecekan missing value, tidak ada data yang hilang pada dataset yang digunakan.

### Tokenizer
---

membuat vektor URL menggunaka CountVectorizer dan mengumpulkan kata-kata dengan tokenizer.
"""

tokenizer = RegexpTokenizer(r'[A-Za-z]+')

df.URL[0]

tokenizer.tokenize(df.URL[0])

print('Mengumpulkan kata...')
t0= time.perf_counter()
df['text_tokenized'] = df.URL.map(lambda t: tokenizer.tokenize(t)) # doing with all rows
t1 = time.perf_counter() - t0
print('Waktu yang dibutuhkan',t1 ,'detik')

df.sample(10)

stemmer = SnowballStemmer("english")

print('Mengumpulkan kata...')
t0= time.perf_counter()
df['text_stemmed'] = df['text_tokenized'].map(lambda l: [stemmer.stem(word) for word in l])
t1= time.perf_counter() - t0
print('Waktu yang dibutuhkan',t1 ,'detik')

df.sample(10)

print('Mengumpulkan kata...')
t0= time.perf_counter()
df['text_sent'] = df['text_stemmed'].map(lambda l: ' '.join(l))
t1= time.perf_counter() - t0
print('Waktu yang dibutuhkan',t1 ,'detik')

df.sample(10)

bad_sites = df[df.Label == 'bad']
good_sites = df[df.Label == 'good']

bad_sites.head()

good_sites.head()

def plot_wordcloud(text, mask=None, max_words=400, max_font_size=120, figure_size=(24.0,16.0), 
                   title = None, title_size=40, image_color=False):
    stopwords = set(STOPWORDS)
    more_stopwords = {'com','http'}
    stopwords = stopwords.union(more_stopwords)

    wordcloud = WordCloud(background_color='white',
                    stopwords = stopwords,
                    max_words = max_words,
                    max_font_size = max_font_size, 
                    random_state = 42,
                    mask = mask)
    wordcloud.generate(text)
    
    plt.figure(figsize=figure_size)
    if image_color:
        image_colors = ImageColorGenerator(mask);
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear");
        plt.title(title, fontdict={'size': title_size,  
                                  'verticalalignment': 'bottom'})
    else:
        plt.imshow(wordcloud);
        plt.title(title, fontdict={'size': title_size, 'color': 'green', 
                                  'verticalalignment': 'bottom'})
    plt.axis('off');
    plt.tight_layout()

data = good_sites.text_sent
data.reset_index(drop=True, inplace=True)

data = bad_sites.text_sent
data.reset_index(drop=True, inplace=True)

"""# **Modelling**
---
Pada tahap ini saya mengembangkan model dengan menggunakan algoritma `logistic regression` dan `Multinomial Naive Bayes`.
"""

cv = CountVectorizer()

feature = cv.fit_transform(df.text_sent)

feature[:5].toarray()

trainX, testX, trainY, testY = train_test_split(feature, df.Label)

"""<H3> Logistic Regression"""

lr = LogisticRegression()
lr.fit(trainX,trainY)

lr.score(testX,testY)

Scores_ml = {}
Scores_ml['Logistic Regression'] = np.round(lr.score(testX,testY),2)

print('Training Accuracy :',lr.score(trainX,trainY))
print('Testing Accuracy :',lr.score(testX,testY))
con_mat = pd.DataFrame(confusion_matrix(lr.predict(testX), testY),
            columns = ['Predicted:Bad', 'Predicted:Good'],
            index = ['Actual:Bad', 'Actual:Good'])

print('\nCLASSIFICATION REPORT\n')
print(classification_report(lr.predict(testX), testY,
                            target_names =['Bad','Good']))

print('\nCONFUSION MATRIX')
plt.figure(figsize= (6,4))
sns.heatmap(con_mat, annot = True,fmt='d',cmap="YlGnBu")

"""<H3>Multinomial Naive Bayes"""

mnb = MultinomialNB()
mnb.fit(trainX,trainY)

mnb.score(testX,testY)

Scores_ml['MultinomialNB'] = np.round(mnb.score(testX,testY),2)

print('Training Accuracy :',mnb.score(trainX,trainY))
print('Testing Accuracy :',mnb.score(testX,testY))
con_mat = pd.DataFrame(confusion_matrix(mnb.predict(testX), testY),
            columns = ['Predicted:Bad', 'Predicted:Good'],
            index = ['Actual:Bad', 'Actual:Good'])

print('\nCLASSIFICATION REPORT\n')
print(classification_report(mnb.predict(testX), testY,
                            target_names =['Bad','Good']))

print('\nCONFUSION MATRIX')
plt.figure(figsize= (6,4))
sns.heatmap(con_mat, annot = True,fmt='d',cmap="YlGnBu")

"""<H3> S V M"""

supp = SVC()
supp.fit(trainX,trainY)

supp.score(testX,testY)

Scores_ml['SVC'] = np.round(supp.score(testX,testY),2)

print('Training Accuracy :',supp.score(trainX,trainY))
print('Testing Accuracy :',supp.score(testX,testY))
con_mat = pd.DataFrame(confusion_matrix(supp.predict(testX), testY),
            columns = ['Predicted:Bad', 'Predicted:Good'],
            index = ['Actual:Bad', 'Actual:Good'])

print('\nCLASSIFICATION REPORT\n')
print(classification_report(supp.predict(testX), testY,
                            target_names =['Bad','Good']))

print('\nCONFUSION MATRIX')
plt.figure(figsize= (6,4))
sns.heatmap(con_mat, annot = True,fmt='d',cmap="YlGnBu")

"""<H3>Decesion Tree"""

dtc = DecisionTreeClassifier()
dtc.fit(trainX,trainY)

dtc.score(testX,testY)

Scores_ml['C.45'] = np.round(dtc.score(testX,testY),2)

print('Training Accuracy :',dtc.score(trainX,trainY))
print('Testing Accuracy :',dtc.score(testX,testY))
con_mat = pd.DataFrame(confusion_matrix(dtc.predict(testX), testY),
            columns = ['Predicted:Bad', 'Predicted:Good'],
            index = ['Actual:Bad', 'Actual:Good'])

print('\nCLASSIFICATION REPORT\n')
print(classification_report(dtc.predict(testX), testY,
                            target_names =['Bad','Good']))

print('\nCONFUSION MATRIX')
plt.figure(figsize= (6,4))
sns.heatmap(con_mat, annot = True,fmt='d',cmap="YlGnBu")

"""<H3> Neural Network"""

nn = MLPClassifier()
nn.fit(trainX,trainY)

nn.score(testX,testY)

Scores_ml['Neural Network'] = np.round(nn.score(testX,testY),2)

print('Training Accuracy :',nn.score(trainX,trainY))
print('Testing Accuracy :',nn.score(testX,testY))
con_mat = pd.DataFrame(confusion_matrix(nn.predict(testX), testY),
            columns = ['Predicted:Bad', 'Predicted:Good'],
            index = ['Actual:Bad', 'Actual:Good'])

print('\nCLASSIFICATION REPORT\n')
print(classification_report(dtc.predict(testX), testY,
                            target_names =['Bad','Good']))

print('\nCONFUSION MATRIX')
plt.figure(figsize= (6,4))
sns.heatmap(con_mat, annot = True,fmt='d',cmap="YlGnBu")

"""<H3> K-Nearst Neighbor"""

knn = KNeighborsClassifier()
knn.fit(trainX,trainY)

knn.score(testX,testY)

Scores_ml['KNN'] = np.round(knn.score(testX,testY),2)

print('Training Accuracy :',knn.score(trainX,trainY))
print('Testing Accuracy :',knn.score(testX,testY))
con_mat = pd.DataFrame(confusion_matrix(knn.predict(testX), testY),
            columns = ['Predicted:Bad', 'Predicted:Good'],
            index = ['Actual:Bad', 'Actual:Good'])

print('\nCLASSIFICATION REPORT\n')
print(classification_report(dtc.predict(testX), testY,
                            target_names =['Bad','Good']))

print('\nCONFUSION MATRIX')
plt.figure(figsize= (6,4))
sns.heatmap(con_mat, annot = True,fmt='d',cmap="YlGnBu")

acc = pd.DataFrame.from_dict(Scores_ml,orient = 'index',columns=['Accuracy'])
sns.set_style('darkgrid')
sns.barplot(acc.index,acc.Accuracy)

pipeline_ls = make_pipeline(CountVectorizer(tokenizer = RegexpTokenizer(r'[A-Za-z]+').tokenize,stop_words='english'), MLPClassifier())

trainX, testX, trainY, testY = train_test_split(df.URL, df.Label)

pipeline_ls.fit(trainX,trainY)

pipeline_ls.score(testX,testY)

print('Training Accuracy :',pipeline_ls.score(trainX,trainY))
print('Testing Accuracy :',pipeline_ls.score(testX,testY))
con_mat = pd.DataFrame(confusion_matrix(pipeline_ls.predict(testX), testY),
            columns = ['Predicted:Bad', 'Predicted:Good'],
            index = ['Actual:Bad', 'Actual:Good'])

print('\nCLASSIFICATION REPORT\n')
print(classification_report(pipeline_ls.predict(testX), testY,
                            target_names =['Bad','Good']))

print('\nCONFUSION MATRIX')
plt.figure(figsize= (6,4))
sns.heatmap(con_mat, annot = True,fmt='d',cmap="YlGnBu")

pickle.dump(pipeline_ls,open('web_phishing.pkl','wb'))

loaded_model = pickle.load(open('web_phishing.pkl', 'rb'))
result = loaded_model.score(testX,testY)
print(result)

predict_bad = ['http://www.paypal.com.it.webscr.logq.gtw.pl/?cmd=_run-check-cookie-submit&redirectCmd=_login-submit','facebook-support-tech.com','facebook.activation.inactive-scure.com','instagram-verify-support.com']
predict_good = ['https://instagram.com','https://facebook.com','tokopedia.com','www.paypal.com']
loaded_model = pickle.load(open('web_phishing.pkl', 'rb'))

result = loaded_model.predict(predict_bad)
result2 = loaded_model.predict(predict_good)
print(result)
print("*"*30)
print(result2)