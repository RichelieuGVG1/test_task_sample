from elasticsearch import Elasticsearch
import pandas as pd

es = Elasticsearch()

def create_index():
    es.indices.create(index='documents', ignore=400)

def index_documents(df):
    for _, row in df.iterrows():
        es.index(index='documents', id=row['id'], document={'text': row['text']})

# Загрузка данных
df = pd.read_csv('posts.csv')
create_index()
index_documents(df)
