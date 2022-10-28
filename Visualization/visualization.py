import mariadb
import pandas as pd
import plotly.express as px

conn_params= {
    "user" : "user1",
    "password" : "karten",
    "host" : "localhost",
    "database" : "dc"
}

"""
visualization -> Bar Chart mit Hashtags
"""


connection= mariadb.connect(**conn_params)
cursor= connection.cursor()

df_neutral = pd.read_sql("select count(*) as count, 'neutral' as sentiment, Hashtags from  tweets_hashtags2 hs "
                         "join text_all tx on tx.id = hs.id and tx.sentiment_final = 0 "
                         "group by Hashtags, sentiment  "
                         "order by count(*) desc ;"
                         , connection, index_col=None)

df_positive = pd.read_sql("select count(*) as count, 'positive' as sentiment, Hashtags from  tweets_hashtags2 hs "
                         "join text_all tx on tx.id = hs.id and tx.sentiment_final = 1 "
                         "group by Hashtags, sentiment  "
                         "order by count(*) desc ;"
                         , connection, index_col=None)

df_negative = pd.read_sql("select count(*) as count, 'negative' as sentiment, Hashtags from  tweets_hashtags2 hs "
                         "join text_all tx on tx.id = hs.id and tx.sentiment_final = -1  "
                         "group by Hashtags, sentiment  "
                         "order by count(*) desc ;"
                         , connection, index_col=None)

# select only top 10 hashtags, rest sum as other
df_neutral.iloc[9:, 2] = 'other'
df_positive.iloc[9:, 2] = 'other'
df_negative.iloc[9:, 2] = 'other'

#print(df_neutral.groupby(['Hashtags', 'sentiment'])['count'].sum().reset_index(name ='count'))

# combine
frames = [df_neutral.groupby(['Hashtags', 'sentiment'])['count'].sum().reset_index(name ='count'),
          df_positive.groupby(['Hashtags', 'sentiment'])['count'].sum().reset_index(name ='count'),
          df_negative.groupby(['Hashtags', 'sentiment'])['count'].sum().reset_index(name ='count')
          ]

result = pd.concat(frames)
#print(result)

# visualize

#'''
fig = px.bar(result, x = 'sentiment', y = 'count' , color =
    'Hashtags', barmode = 'stack')

#fig.show()
#'''

# second figure text
df_all = pd.read_sql("select source, sentiment, count(text) as count from text_all group by source, sentiment;"
                         , connection, index_col=None)

color_discrete_map = {'neutral': 'rgb(234,182,118)', 'negative': 'rgb(97, 5, 20)', 'positive': 'rgb(8, 77, 57)'}

fig2 = px.bar(df_all, x = 'source', y = 'count' , color =
    'sentiment', color_discrete_map= color_discrete_map, barmode = 'stack')

fig2.show()
