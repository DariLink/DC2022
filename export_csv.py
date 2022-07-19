import mariadb
from mariadb import IntegrityError
import pandas as pd

conn_params= {
    "user" : "user1",
    "password" : "karten",
    "host" : "localhost",
    "database" : "dc"
}


connection= mariadb.connect(**conn_params)
cursor= connection.cursor()


#data = pd.read_sql("select * from text_all;", connection, index_col=None)
#data.to_csv('data_all.csv', sep='¬', encoding = 'utf-8-sig')

data = pd.read_sql("select * from tweets_hashtags2;", connection, index_col=None)
data.to_csv('hs_all.csv', sep='¬', encoding = 'utf-8-sig')


'''
tweet = pd.read_sql("select * from tweets2;", connection, index_col=None)
fb = pd.read_sql("select * from facebook;", connection, index_col=None)
insta = pd.read_sql("select * from insta;", connection, index_col=None)


tweet.to_csv('tweet.csv', sep='¬')
fb.to_csv('fb.csv', sep='¬')
insta.to_csv('insta.csv', sep='¬')

'''

