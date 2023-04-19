import mariadb
import pandas as pd

from Web_Scraping.get_fb import get_credentials

"""
this module get hashtags from instragramm and facebook and stores them in hastags table
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

data = pd.read_sql("select * from text_all where source <> 'twitter' and text like '%#%';", connection, index_col=None)

for index, row in data.iterrows():
    for word in str(row['text']).split():
        if word[0] == '#':
            try:
                sql = "INSERT INTO tweets_hashtags2 (id, Hashtags) VALUES (?,?)"
                data = (str(row['id']), word[1:])
                cursor.execute(sql, data)
                connection.commit()
            except:  # pk error, pass
                pass

# Clean hashtags for synonyms
sql = "update IGNORE tweets_hashtags2 set Hashtags = replace(Hashtags, '9euro','neuneuro');"
cursor.execute(sql)
connection.commit()
sql = "update IGNORE tweets_hashtags2 set Hashtags = replace(Hashtags, 'bahnstreik','streik');"
cursor.execute(sql)
connection.commit()
sql = "update IGNORE tweets_hashtags2 set Hashtags = replace(Hashtags, 'gdlstreik','streik');"
cursor.execute(sql)
connection.commit()
sql = "update ignore tweets_hashtags2 set Hashtags = 'verspätung' where Hashtags = 'verspätungen';"
cursor.execute(sql)
connection.commit()
sql = "update ignore tweets_hashtags2 set Hashtags = 'zugausfall' where Hashtags = 'zugausfälle';"
cursor.execute(sql)
connection.commit()
sql = "update ignore  tweets_hashtags2 set Hashtags = 'stuttgart21' where Hashtags = 's21';"
cursor.execute(sql)
connection.commit()
sql = "update IGNORE tweets_hashtags2 set Hashtags = replace(Hashtags, 'mobilitätswende','verkehrswende');"
cursor.execute(sql)
connection.commit()
sql = "update ignore tweets_hashtags2 set Hashtags = 'neuneuroticket' where Hashtags = 'neuneurotickets';"
cursor.execute(sql)
connection.commit()
sql = "update ignore tweets_hashtags2 set Hashtags = 'deutschebahn' where Hashtags = 'db';"
cursor.execute(sql)
connection.commit()
sql = "update ignore tweets_hashtags2 set Hashtags = 'digitaletransformation' where Hashtags = 'digitalisierung';"
cursor.execute(sql)
connection.commit()
sql = "update ignore tweets_hashtags2 set Hashtags = 'gretathunberg' where Hashtags = 'greta';"
cursor.execute(sql)
connection.commit()
