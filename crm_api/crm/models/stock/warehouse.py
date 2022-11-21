"""coding=utf-8."""

from asyncio import tasks
from datetime import datetime
from email.policy import default
import uuid
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Boolean, DateTime
from ...config.db import Base
from ...models.stock.location import Location
from sqlalchemy.orm import relationship

def generate_uuid():
    return str(uuid.uuid4())

class Warehouse(Base):
    """Warehouse Class contains standard information for a Warehouse."""
 
    __tablename__ = "warehouse"
    __table_args__ = {'schema' : 'stock'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(250), unique=True,index=True, nullable=False)
    address = Column(String(400), nullable=True)
    code = Column(String(30), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    locations = relationship("Location", back_populates="warehouse")
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "code": self.code,
            "is_active": self.is_active,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date,
            "locations": self.locations
        }
