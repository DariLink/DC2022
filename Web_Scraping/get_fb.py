import logging
import sys
import time
from datetime import datetime
from random import randint

import facebook_scraper as fb
import mariadb
import pandas as pd
from mariadb import IntegrityError

"""
This script crawls comments from fb posts of deutsche bahn accounts: DeutscheBahn & DBPersonenverkehr
1. Get posts ids and save them in db
2. get comments from post ids and save them
"""


def get_credentials():
    f = open("account.txt", "r")
    lines = f.readlines()
    cookies_path = lines[0]
    user_db = lines[1]
    password_db = lines[2]
    user_ig = lines[3]
    password_ig = lines[4]
    f.close()
    return cookies_path, user_db, password_db, user_ig, password_ig


cookies_path, user_db, password_db, user_ig, password_ig = get_credentials

conn_params = {
    "user": user_db,
    "password": password_db,
    "host": "localhost",
    "database": "dc"
}

connection = mariadb.connect(**conn_params)
cursor = connection.cursor()

### get post by post id for later extracting the comments by the post ids####

'''
list_postids = []
#DBPersonenverkehr,
def get_post_ids():
    for pages in range(1,1000):
            for post in fb.get_posts('DBPersonenverkehr',
                                     cookies = cookies_path,
                                     page_limit=1000,
                                     ):
                try:
                    sql_hs = 'INSERT INTO fb_post_id (post_id,pages) VALUES (?,?)'
                    data = (post['post_id'], pages)
                    cursor.execute(sql_hs, data)
                    connection.commit()
                    print(post['post_id'])

                except IntegrityError:
                    pass
                    print('already in db')


get_post_ids()
'''

############# get comments by post id and save them in db ####

fb.set_cookies(cookies_path)
comments = []
start_url = None


def extract_info(comment, date_post):
    # extract info from a comment and return these in a list

    lst_reactions = ['like', 'haha', 'wow', 'yay', 'sad', 'angry', 'love']
    single_comment = []
    single_comment.append(comment['comment_id'])
    single_comment.append(comment['commenter_id'])
    single_comment.append(comment['comment_text'])

    if comment['comment_time'] is not None:  # if comment has no date, take the post date
        single_comment.append(comment['comment_time'].strftime("%Y-%m-%d %H:%M:%S"))
    else:
        single_comment.append(date_post.strftime("%Y-%m-%d %H:%M:%S"))
    if comment['comment_reactions'] != None:  # extract comment reactions
        for r in lst_reactions:
            single_comment.append(get_reaction(r, comment['comment_reactions']))
    else:
        for z in range(7): single_comment.append(0)
    return single_comment


def get_reaction(r, reaction_dict):
    if r in reaction_dict:
        return reaction_dict[r]  # get number of reactions for a particular reaction type
    else:
        return 0


def handle_pagination_url(url):
    global start_url
    start_url = url


counter_post = 0

# get post ids
post_id = pd.read_sql("select post_id from fb_post_id where post_id not in "
                      "(select distinct post_id from facebook where post_id is not null) "
                      "order by post_id desc ;  "
                      , connection, index_col=None)
post_ids = post_id.values.tolist()

for i in post_ids:
    for post in fb.get_posts(
            post_urls=i,
            options={
                "comments": "generator",
                "reactions": True,
            },
    ):
        try:
            comments_raw = post["comments_full"]
            date_post = post["time"]
            post_id = i[0]
            print(date_post)
            if date_post < datetime.strptime('2019-03-01', '%Y-%m-%d'):
                continue
            for comment in comments_raw:
                list_comment = extract_info(comment, date_post)
                # insert into mariadb
                try:
                    sql = 'INSERT INTO facebook (comment_id, commenter_id, comment_text, comment_time, r_like, ' \
                          'haha, wow, yay, sad, angry, love, post_id ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
                    data = (
                        list_comment[0], list_comment[1], list_comment[2], list_comment[3], list_comment[4],
                        list_comment[5],
                        list_comment[6], list_comment[7], list_comment[8], list_comment[9], list_comment[10], post_id)
                    cursor.execute(sql, data)
                    connection.commit()
                except IntegrityError:
                    pass
                    print('already in db')

                ### get also comments replies ####
                for k in comment['replies']:
                    list_comment = extract_info(k, date_post)
                    try:
                        sql = 'INSERT INTO facebook (comment_id, commenter_id, comment_text, comment_time, r_like, ' \
                              'haha, wow, yay, sad, angry, love ) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
                        data = (
                            list_comment[0], list_comment[1], list_comment[2], list_comment[3], list_comment[4],
                            list_comment[5],
                            list_comment[6], list_comment[7], list_comment[8], list_comment[9], list_comment[10])
                        cursor.execute(sql, data)
                        connection.commit()
                    except IntegrityError:
                        pass
                        print('already in db')

            time.sleep(randint(5, 15))
            logging.info("All done")
            counter_post += 1
            logging.info(i)
            print('post done')

        except fb.exceptions.TemporarilyBanned:
            print("Temporarily banned")
            sys.exit()
        except KeyError:
            continue
