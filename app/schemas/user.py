# app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: Optional[EmailStr]

class UserCreate(UserBase):
    username: Optional[str]
    password: str
    is_superuser: Optional[bool] = None

class UserLogin(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str
    
class UserRead(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserPublic(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str