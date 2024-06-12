from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    username: str
    password: str

class UserUpdate(BaseModel):
    surname: Optional[str]
    name: Optional[str]
    email: Optional[EmailStr]
    # permission: Optional[int]
    # is_active: Optional[bool]

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    username: str


class UserApplicationCreate(BaseModel):
    application_name: str
    user_id: int


class UserApplicationResponse(BaseModel):
    id: int
    application_name: str
    user_id: int

    class Config:
        orm_mode = True
