"""coding=utf-8."""

from datetime import datetime
from email.policy import default
import uuid
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.sql.sqltypes import String, Boolean, DateTime, Date, Float
from ...config.db import Base
from sqlalchemy.orm import relationship

def generate_uuid():
    return str(uuid.uuid4())

class Contract(Base):
    """Contract Class contains standard information for a Contracts of Client."""
 
    __tablename__ = "contracts"
    __table_args__ = {'schema' : 'contract'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    number = Column(String(100), nullable=False)
    id_partner = Column(String, ForeignKey("partner.partners.id"), nullable=False)
    id_contact = Column(String, ForeignKey("partner.contacts.id"), nullable=False)
    sign_by = Column(String(400), nullable=True)
    sign_date = Column(Date, nullable=True, default=datetime.today())
    initial_aproved_import = Column(Float, default=float(0.00))
    real_aproved_import = Column(Float, default=float(0.00))
    real_import = Column(Float, default=float(0.00))
    is_supplement = Column(Boolean, nullable=False, default=False)
    contract_id = Column(String, ForeignKey("contract.contracts.id"), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    partner = relationship("Partner", back_populates="contracts")
    contact = relationship("Contact", back_populates="contracts")
    supplement = relationship("Contract") #, back_populates="suplements")
    
    status_name = Column(String(50), ForeignKey("resources.status_element.name"), nullable=True, default='DELIVERED')
            
    def dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "id_partner": self.id_partner,
            "id_contact": self.id_contact,
            "sign_by": self.sign_by,
            "sign_date": self.sign_date,
            "initial_aproved_import": self.initial_aproved_import,
            "real_aproved_import": self.real_aproved_import,
            "real_import": self.real_import,
            "is_active": self.is_active,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date,
            'status_name': self.status_name
        }
    
