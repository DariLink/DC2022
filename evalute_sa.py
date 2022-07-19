import mariadb
from mariadb import IntegrityError
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

conn_params= {
    "user" : "user1",
    "password" : "karten",
    "host" : "localhost",
    "database" : "dc"
}


connection= mariadb.connect(**conn_params)
cursor= connection.cursor()

'''
pos = pd.read_sql("select  id,  text, '' as sentiment_annot from text_all where sentiment = 'positive'  and CHAR_LENGTH(text) > 50 limit 100;", connection, index_col=None)
neu = pd.read_sql("select id,  text, '' as sentiment_annot from text_all where sentiment = 'neutral' and CHAR_LENGTH(text) > 50 limit 100;", connection, index_col=None)
neg = pd.read_sql("select id,  text, '' as sentiment_annot  from text_all where sentiment = 'negative' and CHAR_LENGTH(text) > 50 limit 100;", connection, index_col=None)

df_all = pd.concat([pos, neu, neg])

# shuffle
df_all = df_all.sample(frac=1).reset_index(drop=True)
df_all.to_excel('to_annot.xlsx')

'''
df_annot = pd.read_excel('to_annot_done.xlsx')


df_orignal = pd.read_sql("select id, "
                          "case when germtwit = 'negative' or sentiment = 'negative' then -1 "
                         " when  sentiment = 'positive' or germval = 'positive'  then 1 "
                         "else 0 end as sentiment from "
                         "text_all;", connection, index_col=None)

"""

df_orignal = pd.read_sql("select id, "
                         "case when textblob > 0.2 then 1 "
                         "when textblob < 0 then -1 "
                         "else 0 "
                         "end as sentiment from text_all where textblob is not null;", connection, index_col=None)
"""


df_comparison = pd.merge(df_orignal, df_annot, on='id', how='inner')
pd.set_option('display.max_rows', None)
#print(df_comparison[['sentiment','sentiment_annot']])


acc = accuracy_score(df_comparison['sentiment_annot'], df_comparison['sentiment'] )
print(confusion_matrix(df_comparison['sentiment_annot'], df_comparison['sentiment'], labels=[-1, 0, 1]))
print(acc)
print(classification_report(df_comparison['sentiment_annot'], df_comparison['sentiment'], labels=[-1, 0, 1]))

#