"""coding=utf-8."""
 
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator
from ...schemas.stock.location import LocationWarehouseSchema
from uuid import UUID

class WarehouseBase(BaseModel):
    name: str
    code: str
    address: Optional[str]

    @validator("name")
    def name_is_not_null(cls, value):

        if not value:
            raise ValueError("Error, el almacén tiene que tener un nombre")

    @validator("code")
    def code_is_not_null(cls, value):

        if not value:
            raise ValueError("Error, el almacén tiene que tener un código")
    
class UpdateWarehouse(WarehouseBase):
    is_active: bool

class WarehouseSchema(WarehouseBase):
    id: UUID
    is_active: bool
    created_date: datetime
    updated_date: datetime
    locations: List[LocationWarehouseSchema] = []
    
    class Config:
        # arbitrary_types_allowed = True
        orm_mode = True
       
        
