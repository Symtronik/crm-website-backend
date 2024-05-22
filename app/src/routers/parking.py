from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from ..common.dependencies import get_db
from ..common.auth import get_current_user
from ..module.parking.crud import add_parking, get_parking
from ..module.parking.schemas import ParkingCreate



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")





router = APIRouter(
    prefix="/parking",
    tags=["parking"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ParkingCreate, status_code=201)
def create_parking(parking: ParkingCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return add_parking(db=db, parking=parking)


@router.get("/", response_model=List[ParkingCreate])
def read_parkings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Dodanie zależności do aktualnego użytkownika
):
    # Tylko zalogowani użytkownicy mogą przeglądać parkingi
    parking = get_parking(db, skip=skip, limit=limit)
    return parking