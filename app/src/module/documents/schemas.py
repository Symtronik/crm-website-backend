from pydantic import BaseModel
from datetime import date
from typing import Optional


class DocumentsCreate(BaseModel):
    document_name: str

    class Config:
        from_attributes = True


class DocumentsResponse(BaseModel):
    id: int
    document_name: str
    # created_at: date

    class Config:
        from_attributes = True
