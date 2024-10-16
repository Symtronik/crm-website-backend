# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from typing import List
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from ..common.dependencies import get_db
# from ..common.auth import get_current_user_with_role
# from ..module.documents import crud, schemas
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# router = APIRouter()
#
#
# @router.post("/documents", response_model=schemas.Document)
# def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
#     return crud.create_document(db=db, document=document)
#
#
# @router.get("/documents", response_model=List[schemas.Document])
# def read_documents(db: Session = Depends(get_db)):
#     return crud.get_documents(db=db)
#
#
# @router.post("/user-documents", response_model=schemas.UserDocument)
# def create_user_document(user_document: schemas.UserDocumentCreate, db: Session = Depends(get_db),
#                          current_user: int = Depends(get_current_user_with_role())):
#     return crud.create_user_document(db=db, user_document=user_document, user_id=current_user.id)
#
#
# @router.get("/user-documents", response_model=List[schemas.UserDocument])
# def read_user_documents(db: Session = Depends(get_db), current_user: int = Depends(get_current_user_with_role())):
#     return crud.get_user_documents(db=db, user_id=current_user.id)
