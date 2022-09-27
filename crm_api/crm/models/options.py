"""coding=utf-8."""

import uuid
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String
from ..config.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class Options(Base):
    """Users Class contains standard information for options menu."""
        
    __tablename__ = "options"
    __table_args__ = {'schema' : 'enterprise'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(150), nullable=False)
    description = Column(String(255), nullable=False)
    text = Column(String(20), nullable=False)
    route = Column(String(30), nullable=True)
    parent = Column(String, nullable=True)
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "text": self.text,
            "route": self.route,
            "parent": self.parent
        }
