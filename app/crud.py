from sqlalchemy.orm import Session
from .models import Document

def get_documents_by_ids(db: Session, ids: list):
    return db.query(Document).filter(Document.id.in_(ids)).all()

def delete_document_by_id(db: Session, doc_id: int):
    db.query(Document).filter(Document.id == doc_id).delete()
    db.commit()
