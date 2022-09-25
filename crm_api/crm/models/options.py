"""coding=utf-8."""

from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String

from ..config.db import Base
from ..models.business import generate_uuid

class Options(Base):
    """Users Class contains standard information for options menu."""
        
    __tablename__ = "options"
    __table_args__ = {'schema' : 'enterprise'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(150), nullable=False)
    description = Column(String(255), nullable=False)
    parent = Column(String, nullable=True)
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "parent": self.parent
        }
