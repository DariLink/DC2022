import twint
import pandas as pd
from datetime import datetime
from datetime import timedelta
import logging
logging.basicConfig(filename='Twitter.log', encoding='utf-8', level=logging.DEBUG)
from random import randint
import time
import mariadb


"""
Get tweets from twitter
1. by hashtag: #deutschebahn or #db 
2. by referred account to: @DB_Bahn, @DB_Presse, @DB_Info
"""

conn_params= {
    "user" : "user1",
    "password" : "karten",
    "host" : "localhost",
    "database" : "dc"
}

connection= mariadb.connect(**conn_params)
cursor= connection.cursor()

#@DB_Bahn, @DB_Presse, @DB_Info, @DB_Karriere  # accounts to be excluded in the analysis
#39999078, 18565652, 14330924, 19482674
c = twint.Config()
c.Username = "DB_Info"
#twint.run.Lookup(c)



def get_tweets_by_date(date, b_hashtag, hashtag, to, cursor, connection):
    c = twint.Config()
    if b_hashtag == True:
        c.Search = hashtag
    else:
        c.To = to
    c.Store_object = True
    c.Since = date
    c.Lang = 'de'
    c.Until = str(datetime.strptime(date, '%Y-%m-%d')+ timedelta(days=1))[:10]
    c.Pandas =True
    c.Proxy_host = 'tor'
    c.Tor_control_port = 9051
    c.Tor_control_password = "16:9AEBD4E3F882CD29603CA439DE7A629D49C81DD432A73EF56029A70A28"
    #c.Limit = 10

    twint.run.Search(c)

    df_tweet = twint.storage.panda.Tweets_df

    df_clean =  df_tweet[["id","conversation_id","date", "tweet","hashtags","user_id",
                    "retweet","nlikes","nreplies","nretweets","near","geo"]]
    df_clean = df_clean.astype({'id': int, 'conversation_id': int, 'user_id': int, 'nlikes': int, 'nreplies': int})

    for index, row in df_clean.iterrows():
        id = row["id"]
        conversation_id = row["conversation_id"]
        date = str(row["date"])
        tweet = str(row["tweet"])
        user_id = row["user_id"]
        retweet = row["retweet"]
        nlikes = row["nlikes"]
        nreplies = row["nreplies"]
        nretweets = row["nretweets"]
        near = str(row["near"])
        geo = str(row["geo"])

        try:
            sql = 'INSERT INTO tweets2 (id, conversation_id, tweet_date, tweet, user_id, retweet, nlikes, nreplies, nretweets,' \
                  'near, geo) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
            data = (id, conversation_id, date, tweet, user_id, retweet, nlikes, nreplies, nretweets, near, geo)
            cursor.execute(sql, data)
            connection.commit()

            # insert hashtags
            for i in list(row["hashtags"]):
                sql_hs = 'INSERT INTO tweets_hashtags2 (id, Hashtags) VALUES (?,?)'
                data = (id, i)
                cursor.execute(sql_hs, data)
                connection.commit()
        except:
            logging.info(datetime.now())
            logging.info(id)
            logging.exception("message")


# accounts: @DB_Bahn, @DB_Presse, @DB_Info
# hashtags: #deutschebahn, #db

#hashtag = '(#DB) lang:de'

date = '2022-06-04'
b_hashtag = False
hashtag = '(#DB) lang:de'
to = '@DB_Bahn'
#'''
while datetime.strptime(date, '%Y-%m-%d') < datetime.now():
    try:
        get_tweets_by_date(date, b_hashtag, hashtag, to, cursor, connection)
        date = str(datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1))[:10]
    except:
        time.sleep(randint(30, 100))



logging.shutdown()



