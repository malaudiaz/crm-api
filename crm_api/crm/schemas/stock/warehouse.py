"""coding=utf-8."""
 
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from ...schemas.stock.location import LocationWarehouseSchema
from uuid import UUID

class WarehouseBase(BaseModel):
    name: str
    code: str
    address: Optional[str]
    
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
       
        
