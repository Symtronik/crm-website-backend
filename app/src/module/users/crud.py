from . import models, schemas
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.src.config.settings import get_settings
from .models import User, UserApplication, Role, Permission

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Tworzenie użytkownika
def create_user(db: Session, user: schemas.UserCreate, role_id: int):
    hashed_password = pwd_context.hash(user.password)

    # Pobieranie roli za pomocą role_id
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Rola nie znaleziona")

    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        name=user.name,
        surname=user.surname,
        email=user.email,
        role_id=role.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Aktualizacja danych użytkownika
def update_user_data(db: Session, user_id: int, user_update: schemas.UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("Użytkownik nie znaleziony")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


# Autentykacja użytkownika
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


# Tworzenie tokenu JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_settings().SECRET_KEY, algorithm=get_settings().HASHING_ALGORITHM)
    return encoded_jwt


# Pobieranie użytkownika za pomocą tokenu odświeżającego
def get_user_by_refresh_token(refresh_token: str, db: Session):
    user = db.query(User).filter(User.refresh_token == refresh_token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Błędny token odświeżający",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# Tworzenie aplikacji z tokenem
def create_application(db: Session, application_name: str, user_id: int):
    application_data = {"sub": application_name, "user_id": user_id}
    token = create_access_token(data=application_data)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("Użytkownik nie znaleziony")

    new_application = UserApplication(application_name=application_name, application_token=token, user_id=user_id)

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


# Pobieranie wszystkich użytkowników
def get_all_users(db: Session):
    return db.query(User).all()


# Pobieranie użytkownika za pomocą nazwy użytkownika
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# Pobieranie wszystkich ról
def get_roles(db: Session):
    return db.query(Role).all()


# Tworzenie nowej roli
def create_role(db: Session, role: schemas.RoleBase):
    db_role = Role(name=role.name)
    for perm in role.permissions:
        permission = db.query(Permission).filter(Permission.name == perm.name).first()
        if permission:
            db_role.permissions.append(permission)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


# Dodanie uprawnienia do roli
def add_permission_to_role(db: Session, role_id: int, permission_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if role and permission:
        role.permissions.append(permission)
        db.commit()
        return role
    return None
