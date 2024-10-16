from sqlalchemy.orm import Session
from . import models, schemas

# Create a document
def create_document(db: Session, document: schemas.DocumentCreate):
    db_document = models.Document(title=document.title, description=document.description)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    for field in document.fields:
        db_field = models.DocumentField(name=field.name, field_type=field.field_type, document_id=db_document.id)
        db.add(db_field)

    db.commit()
    db.refresh(db_document)
    return db_document

# Get all documents
def get_documents(db: Session):
    return db.query(models.Document).all()

# Create a user document (user fills out the form)
def create_user_document(db: Session, user_document: schemas.UserDocumentCreate, user_id: int):
    db_user_document = models.UserDocument(user_id=user_id, document_id=user_document.document_id)
    db.add(db_user_document)
    db.commit()
    db.refresh(db_user_document)

    for field in user_document.fields:
        db_field_value = models.UserDocumentFieldValue(user_document_id=db_user_document.id, field_id=field.field_id, field_value=field.field_value)
        db.add(db_field_value)

    db.commit()
    return db_user_document

# Get user documents
def get_user_documents(db: Session, user_id: int):
    return db.query(models.UserDocument).filter(models.UserDocument.user_id == user_id).all()
