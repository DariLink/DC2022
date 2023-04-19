import re

import mariadb
import pandas as pd

from Web_Scraping.get_fb import get_credentials
from textblob_de import TextBlobDE as TextBlob

cookies_path, user_db, password_db, user_ig, password_ig = get_credentials

conn_params = {
    "user": user_db,
    "password": password_db,
    "host": "localhost",
    "database": "dc"
}

"""
This module preprocesses and does sentiment analysis with text-blob de from https://textblob.readthedocs.io/en/dev/
Textblob is lexicon based approach. The file with prior polarities was modified by us to account for the
polarities from emojis.
"""

connection = mariadb.connect(**conn_params)
cursor = connection.cursor()


def text_preprocess(text):
    text = text.replace("\n", " ")
    text = re.sub(r'https*\S+', '', text)
    text = re.sub(r'@\S+', '', text)
    text = ' '.join(text.split())
    return text


data = pd.read_sql("select id, text from text_all where textblob is null", connection, index_col=None)

for index, row in data.iterrows():
    text_pre = text_preprocess(row['text'])
    blob = TextBlob(text_pre)
    print(text_pre)
    print(round(blob.sentiment.polarity, 2))
    sql = "update text_all set textblob = ? where id = ?"
    data = (round(blob.sentiment.polarity, 2), str(row['id']))
    cursor.execute(sql, data)
    connection.commit()
