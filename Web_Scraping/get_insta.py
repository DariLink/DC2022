import logging
import pickle
from datetime import datetime

import mariadb
from instagrapi import Client, exceptions

logging.basicConfig(filename='insta.log', encoding='utf-8', level=logging.DEBUG)
import time
from random import randint
from get_fb import get_credentials

"""
This script crawls comments from instagram posts of deutsche bahn accounts: DeutscheBahn & DBPersonenverkehr
1. Get media ids and pickle them
2. get comments from media ids and save them
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

# extract list of media ids
cl = Client()
cl.login(user_ig, password_ig)

### Get list of Media ids for this account for scraping by id later ###

''' 
#user_id = cl.user_id_from_username("deutschebahn")
#userids: 7013356314, 485977342
medias = cl.user_medias(7013356314)
pickle.dump(medias, open( "save_ig_07.p", "wb" ))

#'''

media = pickle.load(open("save_ig_07.p", "rb"))
# print(media)
counter_done = 1

# '''
for i in media[0:]:
    try:
        media_id = str(i).split()[0].replace('pk=', '').replace("'", '')
        comment = cl.media_comments(media_id)

        for j in comment:
            comment_dict = dict(j)
            comment_id = comment_dict['pk']
            comment_time = comment_dict['created_at_utc'].strftime("%Y-%m-%d %H:%M:%S")
            comment_text = comment_dict['text']
            comment_user = str(comment_dict['user'])[4:14].replace("'", '')
            likes_count = comment_dict['like_count']
            print(comment_time)
            try:
                sql = 'INSERT INTO insta (comment_id, commentor_id, text, comment_time, likescount, media_id) VALUES (?,?,?,?,?,?)'
                data = (
                    comment_id, comment_user, comment_text, comment_time, likes_count, media_id)
                cursor.execute(sql, data)
                connection.commit()
            except:
                logging.info(datetime.now())
                logging.info(comment_dict)
                logging.exception("message")

        print('post done')
        counter_done += 1
        print(counter_done)
        time.sleep(randint(10, 40))
    except exceptions.PleaseWaitFewMinutes:
        print('banned, sleep')
        time.sleep(randint(600, 1200))

logging.shutdown()
#
# '''
