import warnings

import mariadb
import pandas as pd
import spacy

warnings.filterwarnings('ignore')
from spacy.language import Language
from spacy_langdetect import LanguageDetector

'''
update entries where spacy cannot identify the language as german, 
these are excluded from topic modelling & sentiment Analysis
'''

conn_params = {
    "user": "user1",
    "password": "karten",
    "host": "localhost",
    "database": "dc"
}

connection = mariadb.connect(**conn_params)
cursor = connection.cursor()


@Language.factory("language_detector")
def get_lang_detector(nlp, name):
    return LanguageDetector()


# data = pd.read_sql("select tweet, id from tweets2 where lang is null;", connection, index_col=None)
# data = pd.read_sql("select text as tweet, comment_id as id from insta where lang is null;", connection, index_col=None)
data = pd.read_sql("select comment_text as tweet, comment_id as id from facebook where lang is null;", connection,
                   index_col=None)

nlp = spacy.load("de_core_news_lg")
nlp.add_pipe('language_detector', last=True)
#
for index, row in data.iterrows():
    if nlp(row['tweet'])._.language['language'] != 'de' and len(row['tweet']) > 50:
        # update
        lang = '0'
    else:
        lang = '1'

    # sql_hs = 'update tweets2 set lang = ? where id =?'
    sql_hs = 'update facebook set lang = ? where comment_id =?'
    # sql_hs = 'update insta set lang = ? where comment_id =?'
    data = (lang, row['id'])
    cursor.execute(sql_hs, data)
    connection.commit()
