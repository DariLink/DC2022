import mariadb
import matplotlib.colors
import matplotlib.pyplot as plt
import pandas as pd
from dython.nominal import associations
from scipy.stats import pointbiserialr

"""
This script processes the analysis for the H5. The decreased capacity is approximated by corona incidence.
This is only valid for the first lockdows in spring 2020. The comparison period is March to Mai 2019. 
Further independent variables are: 
Regio (is regio or RE[0-9] mentioned?), 
Maske (is Maske mentioned in text?)
holiday (is the post_date weekend or public holiday?)
likes: how many likes has this post?
For descriptic statistics: Heat Map to spot respective correlations
For the correlation between sentiment & incidency p-value (two-tailed) is calculated

"""

conn_params = {
    "user": "user1",
    "password": "karten",
    "host": "localhost",
    "database": "dc"
}

connection = mariadb.connect(**conn_params)
cursor = connection.cursor()

data = pd.read_sql("select case when sentiment_final = -1 then 0 else 1 end as sentiment, likes, "
                   "case when post_date < '2020-03-04' then 0 else cast(PS_COVID_Faelle as int) end as inzidenz,"
                   "regio, "
                   "case when text like '%Maske%' then 1 else 0 end as 'maske', "
                   "case when weekday(post_date) in (5,6) or cast(post_date as date)  "
                   "in (select holiday from holidays) then 1 else 0 end as 'frei' "
                   "from text_all t "
                   "left join rki_inz r on r.Datum = cast(post_date as date) "
                   "where (post_date between '2020-03-01' and '2020-06-01') "
                   "or (post_date between '2019-03-01' and '2019-06-01') and sentiment_final <> 0 "
                   ";", connection, index_col=None)

fig, ax = plt.subplots(figsize=(16, 8))
# custom db colours
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", "white"])
r = associations(data, ax=ax, cmap=cmap, filename='complete_correlation_2.png')

# quick test whether the calculated correlation matches point biserial correlation coefficient
# used to compute relationship between a continous and and a binary variable
pbc = pointbiserialr(data['inzidenz'], data['sentiment'])
# get p-value of relationship, p-value = 0 is signifficant relationship between incidency and sentiment
print(pbc)
