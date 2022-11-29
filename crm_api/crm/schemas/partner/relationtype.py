"""coding=utf-8."""
 
from datetime import datetime
from pydantic import BaseModel
   
class RelationTypeBase(BaseModel):
    name: str
    description: str
    
class RelationTypeShema(RelationTypeBase):
    id: int
    created_by: str
    created_date: datetime
    updated_by: str
    updated_date: datetime
 
    class Config:
        orm_mode = True