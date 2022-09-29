"""coding=utf-8."""

from datetime import datetime
from email.policy import default
import uuid
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Boolean, DateTime
from ...config.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class Partner(Base):
    """Partner Class contains standard information for a Partner."""
 
    __tablename__ = "partners"
    __table_args__ = {'schema' : 'partner'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(400), nullable=False)
    address = Column(String(400), nullable=True)
    dni = Column(String(30), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(8), nullable=True)
    mobile = Column(String(8), nullable=True)
    nit = Column(String(11), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    is_provider = Column(Boolean, nullable=False, default=False)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    # skeleton_id = Column(String, ForeignKey("enterprise.skeleton.id"), comment="Departamento del Usuario")   # FK added    
        
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "dni": self.dni,
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "nit": self.nit,
            "is_active": self.is_active,
            "is_provider": self.is_provider,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date,
        }
    
# Base.metadata.create_all(bind=engine)
