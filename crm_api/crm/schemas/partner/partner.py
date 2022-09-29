"""coding=utf-8."""
 
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
 
class PartnerBase(BaseModel):
    name: str
    address: str
    dni: str
    email: str
    phone: str
    mobile: str
    nit: str

class PartnerShema(PartnerBase):
    id: UUID
    is_active: bool
    is_provider: bool
    created_date: datetime
    updated_date: datetime
 
    class Config:
        orm_mode = True
        
