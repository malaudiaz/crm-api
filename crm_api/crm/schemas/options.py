"""coding=utf-8."""

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
 
class OptionSchemaCreate(BaseModel):
    name: str
    description: str
    parent: Optional[str] = None
    
class OptionSchema(OptionSchemaCreate):
    id: UUID
 
    class Config:
        orm_mode = True
