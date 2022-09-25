"""coding=utf-8."""

import uuid
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Boolean
from sqlalchemy.orm import relationship
from ..config.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class Business(Base):
    """Business Class contains information for a Business."""
    __tablename__ = "business"
    __table_args__ = {'schema' : 'enterprise'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(150), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    skeleton_list = relationship('Skeleton', back_populates="business")    
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active
        }

# Base.metadata.create_all(bind=engine)
