"""coding=utf-8."""

from datetime import datetime
from email.policy import default
import uuid
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.sql.sqltypes import String, Boolean, DateTime, Integer, Date
from ...config.db import Base
from sqlalchemy.orm import relationship

def generate_uuid():
    return str(uuid.uuid4())

class Representer(Base):
    """Representer Class contains standard information for a Representer."""
 
    __tablename__ = "representers"
    __table_args__ = {'schema' : 'partner'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(400), nullable=False)
    address = Column(String(400), nullable=True)
    dni = Column(String(30), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(60), nullable=True)
    mobile = Column(String(60), nullable=True)
    nit = Column(String(11), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    contacts = relationship("RepresenterContact", back_populates="representer")
    bank_accounts = relationship("RepresenterBankAccount", back_populates="representer")
    
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
            }

class RepresenterBankAccount(Base):
    """Asociación entre Representantes y Cuentas Bancarias"""
 
    __tablename__ = "representers_bank_accounts"
    __table_args__ = {'schema' : 'partner'}
    
    id_representer = Column(String, ForeignKey("partner.representers.id"), primary_key=True)
    id_bank_account = Column(Integer, ForeignKey("resources.bank_accounts.id"), primary_key=True)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    Representer = relationship("Representer")
    bank_account = relationship("BankAccount")
    
    relationtype = relationship("RelationType")
     
    def dict(self):
        return {
            "id_representer": self.id_representer,
            "id_bank_account": self.id_bank_account,
            "representer": self.representer.name,
            "bank_account": self.bank_account.number
            }
        
class RepresenterContact(Base):
    """Asociación entre Empresas Representantes y Contactos"""
 
    __tablename__ = "representers_contacts"
    __table_args__ = {'schema' : 'partner'}
    
    id_representer = Column(String, ForeignKey("partner.representers.id"), primary_key=True)
    id_contact = Column(String, ForeignKey("partner.contacts.id"), primary_key=True)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    representer = relationship("Representer", back_populates="contacts")
    contact = relationship("Contact", back_populates="contacts")
    
    def dict(self):
        return {
            "id_representer": self.id_representer,
            "id_contact": self.id_contact,
            "representer": self.representer.name,
            "contact": self.contact.name,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date
            }
        