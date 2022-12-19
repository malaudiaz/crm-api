"""coding=utf-8."""

from datetime import datetime
from email.policy import default
import uuid
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.sql.sqltypes import String, Boolean, DateTime
from ...config.db import Base
from sqlalchemy.orm import relationship

def generate_uuid():
    return str(uuid.uuid4())
 
 
class Contact(Base):
    """Contact Class contains standard information for a Partner."""
 
    __tablename__ = "contacts"
    __table_args__ = {'schema' : 'partner'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(400), nullable=False)
    address = Column(String(400), nullable=True)
    dni = Column(String(30), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(60), nullable=True)
    mobile = Column(String(60), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    job = Column(String(50), nullable=False)
    
    contacts = relationship("PartnerContact", back_populates="contact")
    contracts = relationship("Contract", back_populates="contact")
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "job": self.job,
            "dni": self.dni,
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "is_active": self.is_active,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date
            }
  
        
class PartnerContact(Base):
    """Asociación entre Cliente y Contactos"""
 
    __tablename__ = "partners_contacts"
    __table_args__ = {'schema' : 'partner'}
    
    id_partner = Column(String, ForeignKey("partner.partners.id"), primary_key=True)
    id_contact = Column(String, ForeignKey("partner.contacts.id"), primary_key=True)
    id_relationtype = Column(Integer, ForeignKey("partner.relationtype.id"))
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    partner = relationship("Partner", back_populates="contacts")
    contact = relationship("Contact", back_populates="contacts")
    
    relationtype = relationship("RelationType")
     
    def dict(self):
        return {
            "id_partner": self.id_partner,
            "id_contact": self.id_contact,
            "id_relationtype": self.id_relationtype,
            "partner": self.partner.name,
            "contact": self.contact.name,
            "relationType": self.relationtype.name,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date
            }
        
    