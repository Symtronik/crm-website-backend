from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..common.dependencies import get_db
from ..module.users.crud import *
from ..module.users.schemas import UserCreate, UserResponse, UserApplicationResponse, UserApplicationCreate
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta
from app.src.config.settings import get_settings
from ..common.auth import get_current_user, get_current_application


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post("/login", tags=["users"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    user.refresh_token = access_token
    db.commit()

    return {"access_token": access_token,"token_type": "bearer"}


@router.post("/register", tags=["users"])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username alredy registered")

    return create_user(db=db, user=user)

@router.get("/user-info/{username}", response_model=UserResponse, tags=["users"])
def read_user(username: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_user = get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/user-info/{user_id}", tags=["users"])
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    try:
        # Sprawdzenie, czy aktualizowana rola to admin
        if user_update.role:
            admin_role_id = db.query(models.Role).filter(models.Role.name == "admin").first().id
            if user_update.role == admin_role_id and current_user.role.name != "admin":
                raise HTTPException(status_code=403, detail="You do not have permission to assign the admin role.")

        updated_user = update_user_data(db=db, user_id=user_id, user_update=user_update)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/roles", tags=["users"])
def get_roles(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Zwracaj wszystkie role, jeśli użytkownik jest adminem
    if current_user.role.name == "admin":
        roles = db.query(models.Role).all()
    else:
        roles = db.query(models.Role).filter(models.Role.name != "admin").all()

    return roles

@router.post("/refresh-token", tags=["users"])
def refresh_token(refresh_token: str, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    user = get_user_by_refresh_token(refresh_token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    user.refresh_token = access_token
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/applications", response_model=UserApplicationResponse, tags=["users"])
def create_application(application: UserApplicationCreate, db: Session = Depends(get_db),
                       current_user: str = Depends(get_current_user)):
    try:
        new_application = create_access_application(
            db=db,
            application_name=application.application_name,
            user_id=application.user_id
        )
        return new_application
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/application-info/{application_id}", response_model=UserApplicationResponse, tags=["users"])
def read_application(application_id: int, db: Session = Depends(get_db), current_application: UserApplication = Depends(get_current_application)):
    application = db.query(UserApplication).filter(UserApplication.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail=f'Application not found {application_id}')
    return application