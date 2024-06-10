from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..config.settings import get_settings
from ..module.users.crud import get_user
from . import dependencies


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def verify_token(token: str, credentials_exception):
#     try:
#         # Dekodowanie tokena
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#
#         # Pobranie identyfikatora użytkownika z payload
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#
#         # Sprawdzenie ważności tokena (opcjonalnie)
#         expire = payload.get("exp")
#         if expire:
#             expire = datetime.fromtimestamp(expire)
#             if datetime.utcnow() > expire:
#                 raise credentials_exception
#
#         return user_id  # lub zwróć obiekt użytkownika, jeśli potrzebujesz więcej informacji
#     except JWTError:
#         raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().HASHING_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user