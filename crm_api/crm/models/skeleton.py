"""coding=utf-8."""

import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean
from sqlalchemy.orm import relationship
from ..config.db import Base
from ..models.business import generate_uuid

class Skeleton(Base):
    """User Class contains standard information for a Business Skeleton."""
    
    __tablename__ = "skeleton"
    __table_args__ = {'schema' : 'enterprise'}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(150), nullable=False)
    description = Column(String(255), nullable=False)
    parent = Column(String, nullable=True)
    business_id = Column(String, ForeignKey("enterprise.business.id"), comment='Negocio del Departamento')    # FK added
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationships
    business = relationship("Business", back_populates="skeleton_list")

    user_list = relationship("Users", backref='skeleton')    

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "parent": self.parent,
            "business_id": self.business_id,
            "is_active": self.is_active
        }

# Base.metadata.create_all(bind=engine)
