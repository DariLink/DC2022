import torch
import mariadb
import pandas as pd
from germansentiment import SentimentModel

"""
get sentiment for the stores tweets & comments with this BERT Model: 
https://github.com/oliverguhr/german-sentiment-lib
"""

model = SentimentModel()

conn_params= {
    "user" : "user1",
    "password" : "karten",
    "host" : "localhost",
    "database" : "dc"
}
connection= mariadb.connect(**conn_params)
cursor= connection.cursor()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# apply sentiment analysis to every row in table, store result in table
data = pd.read_sql("select text as tweet, id as id from text_all where sentiment not in ('neutral', 'positive', 'negative');", connection, index_col=None)

for index, row in data.iterrows():
    print(row['tweet'])
    list_tweet = []
    list_tweet.append(str(row['tweet']))
    sentiment = model.predict_sentiment(list_tweet)
    sql = "update text_all set sentiment = ? where id = ?"
    data = (str(sentiment[0]), str(row['id']))
    cursor.execute(sql, data)
    connection.commit()



#'
