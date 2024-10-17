from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..config.settings import get_settings
from ..module.users.crud import get_user
from ..module.users.models import UserApplication, User
# from ..module.admin.crud import get_admin_user
from . import dependencies
from datetime import datetime
from typing import Union


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_current_application(token: str = Depends(oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().HASHING_ALGORITHM])
        application_name: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if application_name is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    application = db.query(UserApplication).filter(UserApplication.application_token == token).first()
    if application is None:
        raise credentials_exception
    return application


def get_current_user_with_role(token: str = Depends(oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().HASHING_ALGORITHM])
        username: str = payload.get("sub")
        # user_permissions: list = payload.get("permissions", [])
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception


    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception


    return user




