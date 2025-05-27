# app/schemas/user.py

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    full_name: str
    role: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
