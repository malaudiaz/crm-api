"""coding=utf-8."""

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
 
class SkeletonSchemaCreate(BaseModel):
    name: str
    description: str
    parent: str
    business_id: Optional[str] = None
    
class SkeletonSchema(SkeletonSchemaCreate):
    id: UUID
    is_active: bool
 
    class Config:
        orm_mode = True
