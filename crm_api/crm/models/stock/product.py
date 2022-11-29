"""coding=utf-8."""

from datetime import datetime
from email.policy import default
import uuid
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.sql.sqltypes import String, Boolean, DateTime
from ...config.db import Base
from ...models.stock.movement import Movement
from sqlalchemy.orm import relationship

def generate_uuid():
    return str(uuid.uuid4())

class Product(Base):
    """Product Class contains standard information for a Warehouse."""
 
    __tablename__ = "products"
    __table_args__ = {'schema' : 'stock'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    code = Column(String(24), nullable=False)
    name = Column(String(250), nullable=False)
    description = Column(String(200), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    measurement = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=True)
    sale_price = Column(Float, nullable=True)
    ledger_account = Column(String(250), nullable=True)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
        
    movements = relationship("Movement")

    def dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "measurement": self.measurement,
            "unit_price": self.unit_price,
            "cost_price": self.cost_price,
            "sale_price": self.sale_price,
            "ledger_account": self.ledger_account,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date,
            "movements": self.movements
        }
