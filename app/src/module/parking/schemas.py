from pydantic import BaseModel, EmailStr

class ParkingCreate(BaseModel):

    registation_number: str
    surname: str
    name: str
    email: str