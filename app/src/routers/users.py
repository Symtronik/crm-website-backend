from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..common.dependencies import get_db
from ..module.users.models import Role, User
from ..module.users.crud import *
from ..module.users.schemas import UserCreate, UserResponse, UserApplicationResponse, \
    UserApplicationCreate, RoleBase
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta
from app.src.config.settings import get_settings
from ..common.auth import get_current_user_with_role, get_current_application
from typing import List
import logging

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger("uvicorn.error")

@router.post("/login", tags=["users"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Pobierz wszystkie uprawnienia przypisane do roli użytkownika
    permissions = [perm.name for perm in user.role.permissions]

    # Dodaj role i uprawnienia do danych, które będą w tokenie JWT
    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.name, "permissions": permissions},
        expires_delta=access_token_expires
    )

    user.refresh_token = access_token
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/register", tags=["users"])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_email = get_email(db, email=user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = db.query(Role).filter(Role.id == user.role_id).first() if user.role_id else db.query(
        Role).filter(Role.name == "user").first()
    create_user(db=db, user=user, role_id=role.id)
    return {"status_code": 200, "detail": "User added"}


@router.get("/user-info/{username}", response_model=UserResponse, tags=["users"])
def read_user(username: str, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user_with_role)):

    if not current_user.has_permission("view_user_info"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    db_user = get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/user-info/{user_id}", tags=["users"])
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user_with_role)):
    try:
        updated_user = update_user_data(db=db, user_id=user_id, user_update=user_update)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/refresh-token", tags=["users"])
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    user = get_user_by_refresh_token(refresh_token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    roles = [role.name for role in user.roles]
    permissions = [perm.name for perm in user.permissions]

    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "roles": roles, "permissions": permissions},
        expires_delta=access_token_expires
    )

    user.refresh_token = access_token
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/applications", response_model=UserApplicationResponse, tags=["users"])
def create_application(application: UserApplicationCreate, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user_with_role)):


    try:
        new_application = create_application(
            db=db,
            application_name=application.application_name,
            user_id=application.user_id
        )
        return new_application
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/application-info/{application_id}", response_model=UserApplicationResponse, tags=["users"])
def read_application(application_id: int, db: Session = Depends(get_db),
                     current_application: UserApplication = Depends(get_current_application)):
    application = db.query(UserApplication).filter(UserApplication.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail=f'Application not found {application_id}')
    return application


@router.get("/roles", response_model=List[RoleBase], tags=["users"])
def read_roles(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_with_role)):
    return get_roles(db=db)


@router.post("/roles", response_model=RoleBase, tags=["users"])
def add_role(role: RoleBase, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user_with_role)):
    return create_role(db=db, role=role)


@router.post("/roles/{role_id}/permissions/{permission_id}", tags=["users"])
def assign_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db),
                              current_user: User = Depends(get_current_user_with_role)):
    role = add_permission_to_role(db, role_id, permission_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role or Permission not found")
    return role


@router.post("admin/register", tags=["admin"])
def register_user(user: UserCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user_with_role)):
    if current_user.role.name != "super_admin":
        raise HTTPException(status_code=403, detail="Not authorized to add users with roles")

    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    role = db.query(Role).filter(Role.id == user.role_id).first() if user.role_id else db.query(
        Role).filter(Role.name == "user").first()
    return create_user(db=db, user=user, role_id=role.id)


@router.get("/users", response_model=List[schemas.UserResponse], tags=["users"])
def read_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users


@router.get("/secure-endpoint")
def secure_action(current_user: User = Depends(get_current_user_with_role)):
    # Sprawdzanie, czy użytkownik ma uprawnienie do edytowania dokumentów
    if not current_user.has_permission("edit_documents"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )

    # Logika dla użytkownika z odpowiednimi uprawnieniami
    return {"message": "You have access to this action!"}


