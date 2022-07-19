import mariadb
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
de = spacy.load('de_core_news_sm')
stopwords = de.Defaults.stop_words
from sklearn.feature_selection import chi2
import numpy as np
from scipy.stats import f_oneway, logistic
import plotly.express as px

conn_params= {
    "user" : "user1",
    "password" : "karten",
    "host" : "localhost",
    "database" : "dc"
}


connection= mariadb.connect(**conn_params)
cursor= connection.cursor()

data = pd.read_sql("select sentiment_final  as sentiment, likes, "
                   "case when post_date < '2020-03-04' then 0 else cast(PS_COVID_Faelle as int) end as inzidenz,"
                   "regio, "
                   "case when text like '%Maske%' then 1 else 0 end as 'maske', "
                   "case when weekday(post_date) in (5,6) or cast(post_date as date)  "
                   "in (select holiday from holidays) then 1 else 0 end as 'frei' "
                   "from text_all t "
                   "left join rki_inz r on r.Datum = cast(post_date as date) "
                   "where (post_date between '2020-03-01' and '2020-06-01') "
                   "or (post_date between '2019-03-01' and '2019-06-01') and sentiment_final <> 0 "
                   ";", connection, index_col=None)

from dython.nominal import associations
complete_correlation= associations(data, filename= 'complete_correlation.png', figsize=(10,10))
df_complete_corr=complete_correlation['corr']
df_complete_corr.dropna(axis=1, how='all').dropna(axis=0, how='all').style.background_gradient(cmap='coolwarm', axis=None).set_precision(2)





from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as  LDA
from sklearn.preprocessing import StandardScaler

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

x = data.iloc[:, 1:]#.to_numpy()
y = data.iloc[:, 0]#.to_numpy()

'''
sc = StandardScaler()
x = sc.fit_transform(x)
y = sc.transform(y)

'''

import seaborn as sns
import matplotlib.pyplot as plt

#get correlations of each features in dataset
#corrmat = data_new.corr()
#top_corr_features = corrmat.index
#plt.figure(figsize=(20,20))
#plot heat map
#g=sns.heatmap(data_new[top_corr_features].corr(),annot=True,cmap="RdYlGn")
#plt.show()

'''
from scipy.stats import mannwhitneyu

# Carrying out the Wilcoxon–Mann–Whitney test
x = data[data.post_date > '2019-06-01']['frei']
y = data[data.post_date < '2019-06-01']['frei']
#print(x)
#print(y)

results = mannwhitneyu(x =x,y = y, alternative = 'two-sided')
print(results)
'''
# signiffikanter Unterschied zwischen beidengruppen
# correlation zwischen inz und sentiment




