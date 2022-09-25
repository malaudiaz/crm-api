"""coding=utf-8."""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean
from ..config.db import Base
from ..models.business import generate_uuid

class Users(Base):
    """Users Class contains standard information for a User."""
 
    __tablename__ = "users"
    __table_args__ = {'schema' : 'enterprise'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String(50), nullable=False, unique=True)
    fullname = Column(String(100), nullable=False)
    dni = Column(String(11), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(8), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    skeleton_id = Column(String, ForeignKey("enterprise.skeleton.id"), comment="Departamento del Usuario")   # FK added    
        
    def dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "dni": self.dni,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
            "skeleton_id": self.skeleton_id,
            "is_active": self.is_active
        }
    
# Base.metadata.create_all(bind=engine)
