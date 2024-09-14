from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from elasticsearch import Elasticsearch
from .database import get_db
from .models import Document
from .crud import get_documents_by_ids, delete_document_by_id
import pandas as pd
from datetime import datetime

app = FastAPI()
es = Elasticsearch()

class SearchQuery(BaseModel):
    query: str

@app.post("/search/", response_model=List[Document])
def search_documents(search_query: SearchQuery, db: Session = Depends(get_db)):
    query = {
        "query": {
            "match": {
                "text": search_query.query
            }
        },
        "sort": [
            {"created_date": {"order": "desc"}}
        ]
    }
    res = es.search(index="documents", body=query, size=20)
    ids = [hit['_id'] for hit in res['hits']['hits']]
    documents = get_documents_by_ids(db, ids)
    return documents

@app.delete("/delete/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    es.delete(index='documents', id=doc_id)
    delete_document_by_id(db, doc_id)
    return {"status": "deleted"}


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Читаем загруженный файл как DataFrame
    contents = await file.read()
    df = pd.read_csv(pd.compat.StringIO(contents.decode('utf-8')))

    # Индексация данных в Elasticsearch и сохранение в PostgreSQL
    for index, row in df.iterrows():
        # Создание записи для базы данных
        document = Document(
            text=row['text'],
            rubrics=row['rubrics'],
            created_date=datetime.strptime(row['created_date'], '%Y-%m-%d')
        )
        db.add(document)
        db.commit()

        # Индексация в Elasticsearch
        es.index(index='documents', id=document.id, document={'text': document.text})

    return {"status": "success", "message": f"{len(df)} документов загружено и проиндексировано"}

