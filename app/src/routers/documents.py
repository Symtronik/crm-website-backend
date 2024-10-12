from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..common.dependencies import get_db
from ..common.auth import get_current_user
from ..module.documents.crud import add_document, get_documents
from ..module.documents.schemas import DocumentsCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=DocumentsCreate, status_code=201)
def create_document(
        document: DocumentsCreate,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user),
):
    return add_document(db=db, documents=document)


@router.get("", response_model=List[DocumentsCreate])
def read_documents(
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user),
):
    documents = get_documents(db)
    return documents
