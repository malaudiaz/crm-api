"""coding=utf-8."""
 
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, ValidationError, validator
from typing import Optional

from uuid import UUID
 
class PartnerBase(BaseModel):
    type: str
    name: str
    address: Optional[str]
    dni: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    mobile: Optional[str]
    nit: Optional[str]
    registration_number: int
    registration_user: Optional[str]
    registration_date: Optional[date] = None
    
    @validator('type')
    def partner_type(cls, type):
        if not type:
            raise ValueError('Tipo de Cliente es Requerido')
        if type not in ('JURIDICO', 'NATURAL'):
            raise ValueError('El tipo de cliente debe ser JURIDICO o NATURAL')
        return type
    
    @validator('name')
    def name_not_empty(cls, name):
        if not name:
            raise ValueError('Nombre de Cliente es Requerido')
        return name

class PartnerShema(PartnerBase):
    id: UUID
    is_active: bool
    is_provider: bool
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str
 
    class Config:
        orm_mode = True

