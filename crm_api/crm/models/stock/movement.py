"""coding=utf-8."""

from datetime import datetime
from email.policy import default
import uuid
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.sql.sqltypes import String, Boolean, DateTime
from ...config.db import Base
from sqlalchemy.orm import relationship
from ...models.stock.location import Location
from ...models.resources.status import StatusElement
from ...models.stock.measure import Measure

def generate_uuid():
    return str(uuid.uuid4())

class Movement(Base):
    """Movement Class contains standard information for a Warehouse."""
 
    __tablename__ = "movements"
    __table_args__ = {'schema' : 'stock'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    product_id = Column(String, ForeignKey("stock.products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status_id = Column(Integer, ForeignKey("resources.status_element.id"), nullable=False)
    source = Column(String, ForeignKey("stock.location.id"), nullable=False)
    destiny = Column(String, ForeignKey("stock.location.id"), nullable=False)
    measure_id = Column(Integer, ForeignKey("stock.measure.id"), nullable=False)
    document_number = Column(String(100), nullable=True)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
        
    location_source = relationship("Location", foreign_keys=[source])
    location_destiny = relationship("Location", foreign_keys=[destiny])
    status = relationship("StatusElement")
    measure = relationship("Measure")
    product = relationship("Product", back_populates="movements")

    def dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "status_id": self.status_id,
            "source": self.source,
            "destiny": self.destiny,
            "measure_id": self.measure_id,
            "document_number": self.document_number,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date,
            "location_source": self.location_source,
            "location_destiny": self.location_destiny,
            "status": self.status,
            "measure": self.measure,
            # "status_name": self.status.name,
            "product": self.product,
            "product_name": self.product.name,
            "product_description": self.product.description
        }
