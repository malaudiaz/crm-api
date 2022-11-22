"""coding=utf-8."""
 
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class MovementBase(BaseModel):
    quantity: int
    measurement: str
    document_number: str
    status_id: int
    source: str
    destiny: str
    product_id: str

class MovementShema(MovementBase):
    id: UUID
    created_date: datetime
    updated_date: datetime
    # status_name: str
    # product_name: str
    # product_description: str
    # location_source: str
    # location_destiny: str
 
    class Config:
        orm_mode = True

class MovementLocShema(MovementBase):
    id: UUID
    created_date: datetime
    updated_date: datetime
    status_name: str
    product_name: str
    product_description: str
     
    class Config:
        orm_mode = True

class MovementProductShema(MovementBase):
    id: UUID
    created_date: datetime
    updated_date: datetime
    status_name: str
    location_source: str
    location_destiny: str
 
    class Config:
        orm_mode = True
        