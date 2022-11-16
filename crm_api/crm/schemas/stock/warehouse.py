"""coding=utf-8."""
 
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
# from crm.schemas.stock.location import LocationBase
from ...models.stock.location import Location
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
    locations: List[Location] = []
    
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

# class WarehouseShema(WarehouseBase):
#     id: UUID
#     is_active: bool
#     created_date: datetime
#     updated_date: datetime
 
#     class Config:
#         orm_mode = True
        
        
