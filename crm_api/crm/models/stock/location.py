"""coding=utf-8."""

from datetime import datetime
from email.policy import default
import uuid
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.sql.sqltypes import String, Boolean, DateTime
from ...config.db import Base
from sqlalchemy.orm import relationship

def generate_uuid():
    return str(uuid.uuid4())

class Location(Base):
    """Location Class contains standard information for a Localities in WareHouse"""
 
    __tablename__ = "location"
    __table_args__ = {'schema' : 'stock'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(250), unique=True,index=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    corridor = Column(Integer, nullable=True)
    floor = Column(Integer, nullable=True)
    observation = Column(String(500), nullable=True)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    warehouse_id = Column(String, ForeignKey("stock.warehouse.id"))
    
    warehouse = relationship("Warehouse", back_populates="locations")
    # movements = relationship("Movement")

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active,
            "corridor": self.corridor,
            "floor": self.floor,
            "observation": self.observation,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date,
            # "movements": self.movements,
            "warehouse_id": self.warehouse_id,
            "warehouse_name": self.warehouse.name
        }
