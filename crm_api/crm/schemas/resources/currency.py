"""coding=utf-8."""
 
from datetime import datetime
from pydantic import BaseModel
   
class CurrencyBase(BaseModel):
    code: str
    name: str
    description: str
    
class CurrencyShema(CurrencyBase):
    created_by: str
    created_date: datetime = datetime.now()
    updated_by: str
    updated_date: datetime = datetime.now()
    
    is_active: bool = True
 
    class Config:
        orm_mode = True
