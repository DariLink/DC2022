import mariadb
import pandas as pd

from Web_Scraping.get_fb import get_credentials

cookies_path, user_db, password_db, user_ig, password_ig = get_credentials

conn_params = {
    "user": user_db,
    "password": password_db,
    "host": "localhost",
    "database": "dc"
}

connection = mariadb.connect(**conn_params)
cursor = connection.cursor()

# data = pd.read_sql("select * from text_all;", connection, index_col=None)
# data.to_csv('data_all.csv', sep='¬', encoding = 'utf-8-sig')

data = pd.read_sql("select * from tweets_hashtags2;", connection, index_col=None)
data.to_csv('hs_all.csv', sep='¬', encoding='utf-8-sig')

'''
tweet = pd.read_sql("select * from tweets2;", connection, index_col=None)
fb = pd.read_sql("select * from facebook;", connection, index_col=None)
insta = pd.read_sql("select * from insta;", connection, index_col=None)


tweet.to_csv('tweet.csv', sep='¬')
fb.to_csv('fb.csv', sep='¬')
insta.to_csv('insta.csv', sep='¬')

'''
