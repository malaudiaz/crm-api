"""coding=utf-8."""
 
from datetime import datetime, date
from pydantic import BaseModel, validator
from typing import Optional

from uuid import UUID
  
class ContractBase(BaseModel):
    number: str
    id_partner: str
    id_contact: str
    sign_by: Optional[str]
    sign_date: Optional[date]
    initial_aproved_import: float
    
    status_name: Optional[str] = 'DELIVERED'
    
    @validator('number')
    def number_not_empty(cls, number):
        if not number:
            raise ValueError('Numero de Contracto es Requerido')
        return number
    
    @validator('id_partner')
    def id_partner_not_empty(cls, id_partner):
        if not id_partner:
            raise ValueError('Numero de Cliente es Requerido')
        return id_partner
    
    @validator('id_contact')
    def id_contact_not_empty(cls, id_contact):
        if not id_contact:
            raise ValueError('Numero de Contacto es Requerido')
        return id_contact
    
    @validator('initial_aproved_import')
    def initial_aproved_import_not_empty(cls, initial_aproved_import):
        if not initial_aproved_import:
            raise ValueError('Monto del Contrato es Requerido')
        return initial_aproved_import

class ContractShema(ContractBase):
    id: UUID
    is_active: bool
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str
    
    real_aproved_import: float
    real_import: float
    is_supplement: bool
 
    class Config:
        orm_mode = True
