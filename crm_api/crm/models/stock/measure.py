"""coding=utf-8."""

from datetime import datetime
from email.policy import default
import uuid
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.sql.sqltypes import String, Boolean, DateTime
from ...config.db import Base

class Measure(Base):
    """Measure Class contains standard information for a Unit Measure the Products and Movements"""
 
    __tablename__ = "measure"
    __table_args__ = {'schema' : 'stock'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True,index=True, nullable=False)
    description = Column(String(250))
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
        
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date            
        }
