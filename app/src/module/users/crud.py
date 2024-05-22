from . import models, schemas
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.src.config.settings import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, name=user.name, surname=user.surname,
                   email=user.email)
    db.add(db_user)
    db.commit()
    return "complete"


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
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, get_settings().SECRET_KEY, algorithm=get_settings().HASHING_ALGORITHM)
    return encode_jwt

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()