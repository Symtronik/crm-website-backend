from . import models, schemas
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.src.config.settings import get_settings
from .models import User, UserApplication

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, name=user.name, surname=user.surname,
                          email=user.email)
    db.add(db_user)
    db.commit()
    return "complete"


def update_user_data(db: Session, user_id: int, user_update: schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    if "user_id" not in data:
        to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, get_settings().SECRET_KEY, algorithm=get_settings().HASHING_ALGORITHM)
    return encode_jwt


def get_user_by_refresh_token(refresh_token: str, db: Session):
    user = db.query(models.User).filter(models.User.refresh_token == refresh_token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_application(db: Session, application_name: str, user_id: int):
    application_data = {"sub": application_name, "user_id": user_id}
    token = create_access_token(data=application_data)


    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    new_application = UserApplication(application_name=application_name, application_token=token,
                                      user_id=user_id)

    db.add(new_application)

    db.commit()

    db.refresh(new_application)

    return new_application


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
