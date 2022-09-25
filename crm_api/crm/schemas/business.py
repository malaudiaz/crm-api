"""coding=utf-8."""

from pydantic import BaseModel
from uuid import UUID
 
class BusineSchemaCreate(BaseModel):
    name: str
    description: str

class BusineSchema(BusineSchemaCreate):
    id: UUID
    is_active: bool
 
    class Config:
        orm_mode = True
