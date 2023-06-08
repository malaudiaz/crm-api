"""coding=utf-8."""
 
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator
from uuid import UUID

class OfferBase(BaseModel):
    code: str
    name: str
    description: str
    cost_price: Optional[float]
    sale_price: Optional[float]
    ledger_account: str

    @validator('name')
    def name_is_not_null(cls, name):

        if not name:
            raise ValueError("Error, la oferta tiene que tener un nombre")
        return name

    @validator('code')
    def code_is_not_null(cls, code):

        if not code:
            raise ValueError("Error, la oferta tiene que tener un código")
        return code

class OfferSchema(OfferBase):
    id: UUID
    is_active: bool
    created_date: datetime
    updated_date: datetime
        
    class Config:
        # arbitrary_types_allowed = True
        orm_mode = True

class OfferProductBase(BaseModel):
    offer_id: str
    product_id: str
    
    @validator('offer_id')
    def offer_id_not_empty(cls, offer_id):
        if not offer_id:
            raise ValueError('Id de Cliente es Requerido')
        return offer_id
    
    @validator('product_id')
    def product_id_not_empty(cls, product_id):
        if not product_id:
            raise ValueError('Id de Contacto es Requerido')
        return product_id
   
          
class OfferProductShema(OfferProductBase):
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str
 
    class Config:
        orm_mode = True
       
        
