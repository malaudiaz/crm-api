"""coding=utf-8."""
 
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, ValidationError, validator
from typing import Optional

from uuid import UUID
    
class ContactBase(BaseModel):
    name: str
    address: Optional[str]
    dni: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    mobile: Optional[str]
    job: Optional[str]
    
    @validator('name')
    def name_not_empty(cls, name):
        if not name:
            raise ValueError('Nombre de Contacto es Requerido')
        return name

class ContactShema(ContactBase):
    id: UUID
    is_active: bool
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str
 
    class Config:
        orm_mode = True

class ContactCreate(ContactBase):
    id: str
    
    class Config:
        orm_mode = True
    
class PartnerContactRelation(BaseModel):
    id_partner: str
    id_contact: str
    
    @validator('id_partner')
    def partner_id_not_empty(cls, id_partner):
        if not id_partner:
            raise ValueError('Id de Cliente es Requerido')
        return id_partner
    
    @validator('id_contact')
    def contact_id_not_empty(cls, id_contact):
        if not id_contact:
            raise ValueError('Id de Contacto es Requerido')
        return id_contact
    
class PartnerContactBase(PartnerContactRelation):
    id_relationtype: int
    
    @validator('id_relationtype')
    def id_relationtype_id_not_empty(cls, id_relationtype):
        if not id_relationtype:
            raise ValueError('Tipo de Relación es Requerido')
        return id_relationtype
           
class PartnerContactShema(PartnerContactBase):
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str
 
    class Config:
        orm_mode = True
