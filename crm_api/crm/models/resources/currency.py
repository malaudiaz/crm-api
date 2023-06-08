"""coding=utf-8."""

from email.policy import default
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, DateTime, Integer, Boolean
from ...config.db import Base

class Currency(Base):
    """Currency Class contains standard information for a Currency."""
 
    __tablename__ = "currencies"
    __table_args__ = {'schema' : 'resources'}
    
    code = Column(String(3), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(50), nullable=False, default='foo')
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False, default='foo')
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    def dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active
        }