import re
from typing import List

import mariadb
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

"""
This module preprocess and does the sentiment analysis with the pretrained transfomer models from
hugging face
These Models are: deepset/bert-base-german-cased-sentiment-Germeval17
                and JP040/bert-german-sentiment-twitter
"""


class SentimentModel():
    def __init__(self, model_name):
        self.model_name = model_name
        if torch.cuda.is_available():
            self.device = 'cuda'
        else:
            self.device = 'cpu'

        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model = self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.clean_chars = re.compile(r'[^A-Za-züöäÖÜÄß ]', re.MULTILINE)
        self.clean_http_urls = re.compile(r'https*\S+', re.MULTILINE)
        self.clean_at_mentions = re.compile(r'@\S+', re.MULTILINE)

    def predict_sentiment(self, texts: List[str]) -> List[str]:
        texts = [self.clean_text(text) for text in texts]
        # Add special tokens takes care of adding [CLS], [SEP], <s>... tokens in the right way for each model.
        # truncation=True limits number of tokens to model's limitations (512)
        encoded = self.tokenizer.batch_encode_plus(texts, padding=True, add_special_tokens=True, truncation=True,
                                                   return_tensors="pt")
        encoded = encoded.to(self.device)
        with torch.no_grad():
            logits = self.model(**encoded)

        label_ids = torch.argmax(logits[0], axis=1)
        sm = torch.nn.Softmax(dim=1)
        return [self.model.config.id2label[label_id.item()] for label_id in label_ids]

    def replace_numbers(self, text: str) -> str:
        return text.replace("0", " null").replace("1", " eins").replace("2", " zwei") \
            .replace("3", " drei").replace("4", " vier").replace("5", " fünf") \
            .replace("6", " sechs").replace("7", " sieben").replace("8", " acht") \
            .replace("9", " neun")

    def clean_text(self, text: str) -> str:
        text = text.replace("\n", " ")
        text = self.clean_http_urls.sub('', text)
        text = self.clean_at_mentions.sub('', text)
        text = self.replace_numbers(text)
        text = self.clean_chars.sub('', text)  # use only text chars
        text = ' '.join(text.split())  # substitute multiple whitespace with single whitespace
        text = text.strip().lower()
        return text


# "deepset/bert-base-german-cased-sentiment-Germeval17"
model = SentimentModel('JP040/bert-german-sentiment-twitter')

# '''
conn_params = {
    "user": "user1",
    "password": "karten",
    "host": "localhost",
    "database": "dc"
}
connection = mariadb.connect(**conn_params)
cursor = connection.cursor()

# apply sentiment analysis to every row in table, store result in table
data = pd.read_sql("select text as tweet, id as id from text_all where germtwit is null order by post_date asc;",
                   connection, index_col=None)

for index, row in data.iterrows():
    list_tweet = []
    list_tweet.append(str(row['tweet']))
    sentiment = model.predict_sentiment(list_tweet)
    # sql = "update text_all set germval = ? where id = ?"
    sql = "update text_all set germtwit = ? where id = ?"
    data = (str(sentiment[0]), str(row['id']))
    cursor.execute(sql, data)
    connection.commit()
# '''
