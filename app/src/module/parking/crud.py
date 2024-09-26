from . import models, schemas
from sqlalchemy.orm import Session
from datetime import datetime

def add_parking(db: Session, parking: schemas.ParkingCreate, client_ip: str):
    db_parking = models.Parking(
        **parking.dict(),
        created_at=datetime.now(),
        client_ip=client_ip
    )
    db.add(db_parking)
    db.commit()
    db.refresh(db_parking)
    return db_parking

def get_parking(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Parking).offset(skip).limit(limit).all()