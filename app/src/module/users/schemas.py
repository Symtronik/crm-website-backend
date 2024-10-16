from pydantic import BaseModel, EmailStr
from typing import Optional, List


class PermissionBase(BaseModel):
    name: str


class RoleBase(BaseModel):
    name: str
    permissions: List[PermissionBase] = []


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    username: str
    password: str
    role_id: Optional[int] = None

    class Config:
        orm_mode = True
        fields = {'role_id': {'exclude': True}}


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    username: str


class UserUpdate(BaseModel):
    surname: Optional[str]
    name: Optional[str]
    email: Optional[EmailStr]


class UserApplicationCreate(BaseModel):
    application_name: str
    user_id: int


class UserApplicationResponse(BaseModel):
    id: int
    application_name: str
    user_id: int

    class Config:
        orm_mode = True
