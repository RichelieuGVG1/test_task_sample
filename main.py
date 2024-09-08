from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from elasticsearch import Elasticsearch
from datetime import datetime
from database import SessionLocal, Document
import pandas as pd

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
    documents = db.query(Document).filter(Document.id.in_(ids)).all()
    return documents

@app.delete("/delete/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    es.delete(index='documents', id=doc_id)
    db.query(Document).filter(Document.id == doc_id).delete()
    db.commit()
    return {"status": "deleted"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
