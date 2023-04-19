import pandas as pd
import plotly.express as px

# simple graphs for exploratory data analysis

###########################################################################################
# stacked bar chart per source with sentiments as relative fractions/stacks
# amounts of posts per sentiment per source

posts_amt = {
    "source": ["Facebook", "Facebook", "Facebook", "Instagram", "Instagram", "Instagram",
               "Twitter", "Twitter", "Twitter"],
    "sentiment": ["Negativ", "Neutral", "Positiv", "Negativ", "Neutral", "Positiv",
                  "Negativ", "Neutral", "Positiv"],
    "amount": [103060, 41613, 21169, 54350, 22356, 14729, 161510, 93017, 23798]
}

posts_amt_df = pd.DataFrame(
    data=posts_amt
)

fig_sentiment_amt = px.bar(
    posts_amt_df,
    x="source",
    y="amount",
    title="Anzahl der Beiträge pro Plattform und Sentiment",
    color_discrete_sequence=["#DC143C", "#DCDCDC", "#B0C4DE"],
    barmode="stack"
)
fig_sentiment_amt.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)"
}
)
fig_sentiment_amt.update_layout(
    title_x=0.5
)

# fig.update_traces(marker_color='green')
# fig_sentiment_amt.show()
###########################################################################################
# same data but sunburst diagram

fig_sb = px.sunburst(
    posts_amt_df,
    path=["source", "sentiment"],
    values="amount",
    color="sentiment",
    color_discrete_sequence=["#DC143C", "#DCDCDC", "#B0C4DE"],
    title="Anteil der Beiträge pro Plattform und Sentiment",
)
fig_sb.update_traces(
    textinfo="label+percent parent"
)
fig_sb.update_layout(
    autosize=False,
    height=500,
    width=500
)
fig_sb.update_layout(
    title_x=0.5
)
# fig_sb.show()

###########################################################################################
# simple graphs for the results of topic modelling
# facebook:
fb_negative = [
    ("Verspätung/Zuverlässigkeit", 33763),
    ("Ticketbuchung", 12425),
    ("Streik", 10905),
    ("Leder, Tierschutz", 10449),
    ("Service bei Problemen", 9806),
    ("Maskenpflicht", 8879),
    ("Fahrkomfort", 8566),
    ("Baustellen/Streckensperrungen", 8267)
]
fb_neutral = [
    ("Fragen zur Ticketbuchung", 11675),
    ("Maskenpflicht ", 6625),
    ("Stellenanzeigen", 5871),
    ("Fahrkomfort", 5586),
    ("Pressebeiträge", 3909),
    ("Fahrtverzögerungen", 3878),
    ("BFeiertagsbeiträge", 1930),
    ("Externe Links", 1096),
    ("Infos zum Konzern", 1043)
]
fb_positive = [
    ("Fahrkomfort", 7160),
    ("Service", 5661),
    ("Presse, PR", 2917),
    ("Bahnhöfe und Städte", 2341),
    ("Ticketbuchung, App", 3090)
]

# create dataframes for each sentiment
fb_negative_df = pd.DataFrame(fb_negative, columns=["Thema", "Anzahl der Beiträge"])
fb_negative_df["Sentiment"] = "Negativ"
fb_neutral_df = pd.DataFrame(fb_neutral, columns=["Thema", "Anzahl der Beiträge"])
fb_neutral_df["Sentiment"] = "Neutral"
fb_positive_df = pd.DataFrame(fb_positive, columns=["Thema", "Anzahl der Beiträge"])
fb_positive_df["Sentiment"] = "Positiv"

# concatenating the frames to one facebook frame
fb_frames = [fb_negative_df, fb_neutral_df, fb_positive_df]
fb_topics = pd.concat(fb_frames)
# print(fb_topics)

# sunburst chart
fig_fb = px.sunburst(
    fb_topics,
    path=["Sentiment", "Thema"],
    values="Anzahl der Beiträge",
    color_discrete_sequence=["#DC143C", "#DCDCDC", "#B0C4DE"],
    title="Sentiment und Themen auf Facebook",
)
fig_fb.update_traces(
    textinfo="label+percent parent"
)
fig_fb.update_layout(
    autosize=False,
    height=500,
    width=500
)
fig_fb.update_layout(
    title_x=0.5
)
# fig_fb.show()

###########################################################################################

# instagram:
ig_negative = [
    ("Verspätung/Zuverlässigkeit", 22538),
    ("Umgang mit Fahrgästen", 7478),
    ("Ticketbuchung", 5464),
    ("Fahrkomfort", 5007),
    ("Presse", 3918),
    ("Maske/Benehmen", 3575),
    ("Umwelt/Müll", 3378),
    ("PR Aktionen", 2992)
]
ig_neutral = [
    ("Online Service", 3783),
    ("Bahnreise allgemein", 13122),
    ("Kleidung", 1666),
    ("Nutzerdiskussionen", 1481),
    ("Zuverlässigkeit", 1233),
    ("Umwelt", 1071)
]
ig_positive = [
    ("Ausstattung der Züge", 3836),
    ("Fahrkomfort", 7031),
    ("Service und Pünktlichkeit", 1409),
    ("Kleidung", 1153),
    ("Kommentare über Beiträge", 708),
    ("Bahnhöfe", 592)
]

# create dataframes for each sentiment
ig_negative_df = pd.DataFrame(ig_negative, columns=["Thema", "Anzahl der Beiträge"])
ig_negative_df["Sentiment"] = "Negativ"
ig_neutral_df = pd.DataFrame(ig_neutral, columns=["Thema", "Anzahl der Beiträge"])
ig_neutral_df["Sentiment"] = "Neutral"
ig_positive_df = pd.DataFrame(ig_positive, columns=["Thema", "Anzahl der Beiträge"])
ig_positive_df["Sentiment"] = "Positiv"

# concatenating the frames to one instagram frame
ig_frames = [ig_negative_df, ig_neutral_df, ig_positive_df]
ig_topics = pd.concat(ig_frames)
# print(ig_topics)

# sunburst chart
fig_ig = px.sunburst(
    ig_topics,
    path=["Sentiment", "Thema"],
    values="Anzahl der Beiträge",
    color_discrete_sequence=["#DC143C", "#DCDCDC", "#B0C4DE"],
    title="Sentiment und Themen auf Instagram",
)
fig_ig.update_traces(
    textinfo="label+percent parent"
)
fig_ig.update_layout(
    autosize=False,
    height=500,
    width=500
)
fig_ig.update_layout(
    title_x=0.5
)
# fig_ig.show()
###########################################################################################

# twitter
tw_negative = [
    ("Verspätung/Zuverlässigkeit", 62329),
    ("Ticketbuchung", 31754),
    ("Maskenpflicht", 22315),
    ("PR Beiträge", 17869),
    ("Preis-/Leistungsverhältnis", 12145),
    ("Bauarbeiten/Streckensperrungen", 5931),
    ("Ironische Beiträge", 5518),
    ("Streik", 3649)
]
tw_neutral = [
    ("Kundenservice", 41868),
    ("Preis-/Leistungsverhältnis", 12923),
    ("Pressebeiträge (allgemein)", 12142),
    ("Pressebeiträge (Umwelt)", 17999),
    ("Stellenausschreibungen", 4535),
    ("Petitionen", 2303),
    ("Digitalisierung", 1247)
]
tw_positive = [
    ("Kundenservice", 10159),
    ("Fahrkomfort/Ausstattung/Personal", 9564),
    ("Ticketbuchung", 2356),
    ("Modernisierung Bahnhöfe und Streckennetz", 1719)
]

# create dataframes for each sentiment
tw_negative_df = pd.DataFrame(tw_negative, columns=["Thema", "Anzahl der Beiträge"])
tw_negative_df["Sentiment"] = "Negativ"
tw_neutral_df = pd.DataFrame(tw_neutral, columns=["Thema", "Anzahl der Beiträge"])
tw_neutral_df["Sentiment"] = "Neutral"
tw_positive_df = pd.DataFrame(tw_positive, columns=["Thema", "Anzahl der Beiträge"])
tw_positive_df["Sentiment"] = "Positiv"

# concatenating the frames to one instagram frame
tw_frames = [tw_negative_df, tw_neutral_df, tw_positive_df]
tw_topics = pd.concat(tw_frames)
# print(tw_topics)

# sunburst chart
fig_tw = px.sunburst(
    tw_topics,
    path=["Sentiment", "Thema"],
    values="Anzahl der Beiträge",
    color_discrete_sequence=["#DC143C", "#DCDCDC", "#B0C4DE"],
    title="Sentiment und Themen auf Twitter",
)
fig_tw.update_traces(
    textinfo="label+percent parent"
)
fig_tw.update_layout(
    autosize=False,
    height=500,
    width=500
)
fig_tw.update_layout(
    title_x=0.5
)
# fig_tw.show()
###########################################################################################
