from . import models, schemas
from datetime import datetime
from sqlalchemy.orm import Session

def add_document(db:Session, documents: schemas.DocumentsCreate):
    db_document = models.Documents(
        **documents.dict()
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_documents(db:Session):
    documents = db.query(models.Documents).all()
    return [schemas.DocumentsCreate.from_orm(documents) for documents in documents]