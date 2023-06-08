"""coding=utf-8."""
 
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator
from ...schemas.stock.movement import MovementProductShema
from ...schemas.stock.measure import MeasureSchema
from uuid import UUID

class ProductBase(BaseModel):
    code: str
    name: str
    description: str
    measure_id: int
    unit_price: float
    cost_price: Optional[float]
    sale_price: Optional[float]
    ledger_account: str

    @validator('name')
    def name_is_not_null(cls, name):

        if not name:
            raise ValueError("Error, el almacén tiene que tener un nombre")
        return name

    @validator('code')
    def code_is_not_null(cls, code):

        if not code:
            raise ValueError("Error, el almacén tiene que tener un código")
        return code

class ProductSchema(ProductBase):
    id: UUID
    is_active: bool
    created_date: datetime
    updated_date: datetime
    measure: MeasureSchema
    movements: List[MovementProductShema] = []
    
    class Config:
        # arbitrary_types_allowed = True
        orm_mode = True

       
        
