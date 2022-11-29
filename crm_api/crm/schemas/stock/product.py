"""coding=utf-8."""
 
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator
from ...schemas.stock.movement import MovementProductShema
from uuid import UUID

class ProductBase(BaseModel):
    code: str
    name: str
    description: str
    measurement: str
    unit_price: float
    cost_price: Optional[float]
    sale_price: Optional[float]
    ledger_account: str

    @validator("name")
    def name_is_not_null(cls, value):

        if not value:
            raise ValueError("Error, el almacén tiene que tener un nombre")

    @validator("code")
    def code_is_not_null(cls, value):

        if not value:
            raise ValueError("Error, el almacén tiene que tener un código")
    

class ProductSchema(ProductBase):
    id: UUID
    is_active: bool
    created_date: datetime
    updated_date: datetime
    movements: List[MovementProductShema] = []
    
    class Config:
        # arbitrary_types_allowed = True
        orm_mode = True
       
        
