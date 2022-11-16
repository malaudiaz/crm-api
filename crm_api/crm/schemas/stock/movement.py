"""coding=utf-8."""
 
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
# from ...models
 
    # id = Column(String, primary_key=True, default=generate_uuid)
    # product_id = Column(String, ForeignKey("stock.products.id"), nullable=False)
    # quantity = Column(Integer, nullable=False)
    # status_id = Column(Integer, ForeignKey("resources.status_element.id"), nullable=False)
    # source = Column(String, ForeignKey("stock.location.id"), nullable=False)
    # destiny = Column(String, ForeignKey("stock.location.id"), nullable=False)
    # measurement = Column(String, nullable=True)
    # document_number = Column(String(100), nullable=True)
    # created_by = Column(String(50), nullable=False)
    # created_date = Column(DateTime, nullable=False, default=datetime.now())
    # updated_by = Column(String(50), nullable=False)
    # updated_date = Column(DateTime, nullable=False, default=datetime.now())
        
    # location_source = relationship("Location", back_populates="movements")
    # location_destiny = relationship("Location", back_populates="movements")

class MovementBase(BaseModel):
    quantity: int
    measurement: str
    document_number: str
        
class Movement(MovementBase):
    status_id: int
    source: str
    destiny:str
    
class MovementShema(MovementBase):
    id: UUID
    created_date: datetime
    updated_date: datetime
 
    class Config:
        orm_mode = True