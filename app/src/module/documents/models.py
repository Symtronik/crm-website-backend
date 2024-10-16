from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from ...config.database import DBBase
from datetime import datetime

class Document(DBBase):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    fields = relationship('DocumentField', back_populates='document')

class DocumentField(DBBase):
    __tablename__ = 'document_fields'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    field_type = Column(String)
    document_id = Column(Integer, ForeignKey('documents.id'))
    document = relationship('Document', back_populates='fields')

class UserDocument(DBBase):
    __tablename__ = 'user_documents'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    document_id = Column(Integer, ForeignKey('documents.id'))
    saved_at = Column(DateTime, default=datetime.utcnow)
    fields = relationship('UserDocumentFieldValue', back_populates='user_document')

class UserDocumentFieldValue(DBBase):
    __tablename__ = 'user_document_field_values'
    id = Column(Integer, primary_key=True, index=True)
    user_document_id = Column(Integer, ForeignKey('user_documents.id'))
    field_id = Column(Integer, ForeignKey('document_fields.id'))
    field_value = Column(Text)
    user_document = relationship('UserDocument', back_populates='fields')
