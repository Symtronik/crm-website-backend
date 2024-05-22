from . import models, schemas

from sqlalchemy.orm import Session


def add_parking(db:Session, parking: schemas.ParkingCreate):
    db_parking = models.Parking(**parking.dict())
    db.add(db_parking)
    db.commit()
    db.refresh(db_parking)
    return db_parking

def get_parking(db:Session, skip: int=0, limit: int = 100):
    return db.query(models.Parking).offset(skip).limit(limit).all()