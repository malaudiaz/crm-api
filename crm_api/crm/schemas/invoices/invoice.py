"""coding=utf-8."""
 
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
   
class InvoiceBase(BaseModel):
    invoice_number: str
    currency: str
    invoice_import: float
    real_import: float
    expire_date: datetime
    observation: str
    status: str

class InvoiceImports(BaseModel):
    invoice_import: float
    real_import: float
    
class InvoiceShema(InvoiceBase):
    id: UUID
    created_date: datetime
    updated_date: datetime
 
    class Config:
        orm_mode = True
        

        