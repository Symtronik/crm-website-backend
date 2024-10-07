from . import models, schemas
from datetime import datetime
from sqlalchemy.orm import Session

def add_parking(db: Session, parking: schemas.ParkingCreate):
    db_parking = models.Parking(
        **parking.dict(),
        created_at=datetime.utcnow(),  # Ustawienie aktualnego czasu
    )
    db.add(db_parking)
    db.commit()
    db.refresh(db_parking)
    return db_parking

def get_parking(db: Session):
    # Pobiera wszystkie rekordy z bazy danych
    parkings = db.query(models.Parking).all()
    # Używa from_orm do konwersji każdego rekordu na schemat ParkingResponse
    return [schemas.ParkingResponse.from_orm(parking) for parking in parkings]

def put_parking(db: Session, parking_id:int, parking_update: schemas.ParkingUpdate):
    db_parking = db.query(models.Parking).filter(models.Parking.id == parking_id).first()

    if not db_parking:
        return None

    for key, value in parking_update.dict(exclude_unset=True).items():
        setattr(db_parking, key, value)

    db.commit()
    db.refresh(db_parking)

    return db_parking