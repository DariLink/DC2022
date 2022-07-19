import re
import spacy
import mariadb
import numpy as np
import pandas as pd
from gsdmm import MovieGroupProcess
from cleantext import clean
import random

"""
This module preprocesses text and allocate the words to k topics with the gsdmm module: 
https://github.com/rwalk/gsdmm
First topic modelling was tested with LDA but it seems like gsdmm is more suitable for short text
Result: k topics with 15 most common words.
"""


conn_params= {
    "user" : "user1",
    "password" : "karten",
    "host" : "localhost",
    "database" : "dc"
}

connection= mariadb.connect(**conn_params)
cursor= connection.cursor()

nlp = spacy.load('de_core_news_lg')



def selected_topics(model, vectorizer, top_n=10):
    for idx, topic in enumerate(model.components_):
        print("Topic %d:" % (idx))
        print([(vectorizer.get_feature_names()[i], topic[i])
                        for i in topic.argsort()[:-top_n - 1:-1]])


data = pd.read_sql("select text as comment_text from text_all where sentiment_final = -1 and source = 'facebook';", connection, index_col=None)


data = data.astype(str).apply(lambda x: x.str.encode('iso8859_15', 'ignore').str.decode('iso8859_15'))

#"""
# remove urls
data['comment_text_clean'] = data['comment_text'].apply(lambda x: re.sub(r'https?:\/\/\S+', '', x))
data['comment_text_clean'] = data.comment_text_clean.apply(lambda x: re.sub(r"www\.[a-z]?\.?(com)+|[a-z]+\.(com)", '', x))
data['comment_text_clean'] = data['comment_text_clean'].apply(lambda x: re.sub(r'{link}', '', x))
data['comment_text_clean'] = data['comment_text_clean'].apply(lambda x: re.sub(r"\[video\]", '', x))


# source: https://universaldependencies.org/docs/u/pos/

removal = ['ADV', 'PRON', 'CCONJ', 'PUNCT', 'PART', 'DET', 'ADP', 'SPACE', 'NUM', 'SYM']
tokens = []
remove = ['der', 'die', 'das', 'ein', 'kein', 'haben', 'ihr', 'machen', '..', 'mein', '', 'kommen', '#', ' ',
          'bahn','db' ,'deutsch' ,'deutschebahn' , '--', '_', '\n']

for summary in nlp.pipe(data['comment_text_clean']):
    proj_tok = [token.lemma_.lower() for token in summary if
                token.pos_ not in removal and token.is_stop is False and token.text not in remove and token.lemma_.lower() not in remove]
    tokens.append(proj_tok)

data['tokens'] = tokens
docs = data['tokens'].to_numpy()

vocab = set(x for doc in docs for x in doc)


# Train a new model 
random.seed(1000)
# Init of the Gibbs Sampling Dirichlet Mixture Model algorithm
mgp = MovieGroupProcess(K=10, alpha=0.1, beta=0.1, n_iters=30)
n_terms = len(vocab)
n_docs = len(docs)

# Fit the model on the data given the chosen seeds
y = mgp.fit(docs, n_terms)

doc_count = np.array(mgp.cluster_doc_count)
print('Number of documents per topic :', doc_count)

# Topics sorted by the number of document they are allocated to
top_index = doc_count.argsort()[-15:][::-1]
print('Most important clusters (by number of docs inside):', top_index)


# define function to get top words per topic
def top_words(cluster_word_distribution, top_cluster, values):
    for cluster in top_cluster:
        sort_dicts = sorted(cluster_word_distribution[cluster].items(), key=lambda k: k[1], reverse=True)[:values]
        print("\nCluster %s : %s" % (cluster, sort_dicts))


# get top words in topics
top_words(mgp.cluster_word_distribution, top_index, 15)


#"""
