"""coding=utf-8."""
 
from pydantic import BaseModel
from uuid import UUID
 
class UserBase(BaseModel):
    username: str
    fullname: str
    dni: str
    job: str
    email: str
    phone: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    password: str

class UserShema(UserCreate):
    id: UUID
    is_active: bool
    selected: bool = False
    sign_contracts: bool = False
 
    class Config:
        orm_mode = True
        
