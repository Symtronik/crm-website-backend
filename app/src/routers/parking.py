from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..common.dependencies import get_db
from ..common.auth import get_current_user
from ..module.parking.crud import add_parking, get_parking, put_parking
from ..module.parking.schemas import ParkingCreate, ParkingResponse, ParkingUpdate



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")





router = APIRouter(
    prefix="/parking",
    tags=["parking"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=ParkingCreate, status_code=201)
def create_parking(
        parking: ParkingCreate,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
):
    return add_parking(db=db, parking=parking)


@router.get("", response_model=List[ParkingResponse])
def read_parkings(

    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),

):
    # Tylko zalogowani użytkownicy mogą przeglądać parkingi
    parking = get_parking(db)
    return parking

@router.put("/{parking_id}", response_model=ParkingResponse)
def update_parking(
        parking_id: int,
        parking_update: ParkingUpdate,
        db:  Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
):
    updated_parking = put_parking(db=db, parking_id=parking_id, parking_update=parking_update)

    if updated_parking is None:
        raise HTTPException(status_code=404, detail="Parking not found")

    return updated_parking