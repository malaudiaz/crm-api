"""coding=utf-8."""
 
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class MeasureBase(BaseModel):
    name: str
    description: Optional[str]    
    
class MeasureSchema(MeasureBase):
    id: int
    is_active: bool
    created_date: datetime
    updated_date: datetime
    
    class Config:
        orm_mode = True

