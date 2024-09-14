from sqlalchemy import Column, Integer, String, DateTime, Text
from .database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    rubrics = Column(Text, nullable=False)
    created_date = Column(DateTime, nullable=False)
