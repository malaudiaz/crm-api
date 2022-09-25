"""coding=utf-8."""
 
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
 
class UserBase(BaseModel):
    username: str
    fullname: str
    dni: str
    email: str
    phone: str
    skeleton_id: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    password: str

class UserShema(UserCreate):
    id: UUID
    is_active: bool
 
    class Config:
        orm_mode = True
        
