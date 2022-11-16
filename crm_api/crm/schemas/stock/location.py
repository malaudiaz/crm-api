"""coding=utf-8."""
 
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
# from crm.schemas.stock.warehouse import WarehouseBase 

class LocationBase(BaseModel):
    name: str
    corridor: int
    floor: int
    observation: Optional[str]
    warehouse_id: str
    
class UpdateLocation(LocationBase):
    is_active: bool
    
class LocationSchema(LocationBase):
    id: UUID
    is_active: bool
    created_date: datetime
    updated_date: datetime
    
    class Config:
        orm_mode = True
    
    
# class LocationShema(LocationBase):
#     id: UUID
#     is_active: bool
#     is_provider: bool
#     created_date: datetime
#     updated_date: datetime
 
#     class Config:
#         orm_mode = True