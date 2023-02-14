"""coding=utf-8."""

import uuid
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Boolean
from ...config.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class Users(Base):
    """Users Class contains standard information for a User."""
 
    __tablename__ = "users"
    __table_args__ = {'schema' : 'enterprise'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String(50), nullable=False, unique=True)
    fullname = Column(String(100), nullable=False)
    job = Column(String(50), nullable=False)
    dni = Column(String(11), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(8), nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    selected = Column(Boolean, nullable=False, default=False)
    sign_contracts = Column(Boolean, nullable=True, default=False)
    
    # skeleton_id = Column(String, ForeignKey("enterprise.skeleton.id"), comment="Departamento del Usuario")   # FK added    
        
    def dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "job": self.job,
            "dni": self.dni,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
            "is_active": self.is_active,
            "selected": self.selected,
            "sign_contracts": self.sign_contracts
        }
    
# Base.metadata.create_all(bind=engine)
