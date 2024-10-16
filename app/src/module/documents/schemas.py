from pydantic import BaseModel
from typing import List, Optional


class DocumentFieldBase(BaseModel):
    name: str
    field_type: str


class DocumentFieldCreate(DocumentFieldBase):
    pass


class DocumentField(DocumentFieldBase):
    id: int
    document_id: int

    class Config:
        orm_mode = True


class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None


class DocumentCreate(DocumentBase):
    fields: List[DocumentFieldCreate]


class Document(DocumentBase):
    id: int
    fields: List[DocumentField] = []

    class Config:
        orm_mode = True


class UserDocumentFieldValueBase(BaseModel):
    field_id: int
    field_value: str


class UserDocumentFieldValueCreate(UserDocumentFieldValueBase):
    pass


class UserDocumentFieldValue(UserDocumentFieldValueBase):
    id: int
    user_document_id: int

    class Config:
        orm_mode = True


class UserDocumentBase(BaseModel):
    document_id: int


class UserDocumentCreate(UserDocumentBase):
    fields: List[UserDocumentFieldValueCreate]


class UserDocument(UserDocumentBase):
    id: int
    fields: List[UserDocumentFieldValue] = []
    saved_at: Optional[str] = None

    class Config:
        orm_mode = True
