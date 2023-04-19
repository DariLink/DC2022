import mariadb
import pandas as pd
import torch
from germansentiment import SentimentModel

from Web_Scraping.get_fb import get_credentials

"""
get sentiment for the stores tweets & comments with this BERT Model: 
https://github.com/oliverguhr/german-sentiment-lib
"""

cookies_path, user_db, password_db, user_ig, password_ig = get_credentials

conn_params = {
    "user": user_db,
    "password": password_db,
    "host": "localhost",
    "database": "dc"
}

connection = mariadb.connect(**conn_params)
cursor = connection.cursor()

model = SentimentModel()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# apply sentiment analysis to every row in table, store result in table
data = pd.read_sql(
    "select text as tweet, id as id from text_all where sentiment not in ('neutral', 'positive', 'negative');",
    connection, index_col=None)

for index, row in data.iterrows():
    print(row['tweet'])
    list_tweet = []
    list_tweet.append(str(row['tweet']))
    sentiment = model.predict_sentiment(list_tweet)
    sql = "update text_all set sentiment = ? where id = ?"
    data = (str(sentiment[0]), str(row['id']))
    cursor.execute(sql, data)
    connection.commit()

# '
