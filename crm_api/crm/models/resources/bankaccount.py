
"""coding=utf-8."""

from email.policy import default
from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, DateTime, Integer, Boolean, Text
from ...config.db import Base

class Bank(Base):
    """Bank Class contains standard information for Banks."""
 
    __tablename__ = "banks"
    __table_args__ = {'schema' : 'resources'}
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), nullable=True)
    name = Column(String(200), nullable=False, unique=True)
    addres = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(50), nullable=False, default='foo')
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False, default='foo')
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    def dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "addres": self.addres,
            "is_active": self.is_active
        }

class BankAccount(Base):
    """BankAccount Class contains standard information for Bank Accounts."""
 
    __tablename__ = "bank_accounts"
    __table_args__ = {'schema' : 'resources'}
    
    id = Column(Integer, primary_key=True)
    number = Column(String(50), nullable=True, unique=True)
    title = Column(String(300), nullable=False)
    currency_code = Column(String(3), ForeignKey("resources.currencies.code"), nullable=False)
    bank_id = Column(Integer, ForeignKey("resources.banks.id"), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(50), nullable=False, default='foo')
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False, default='foo')
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    def dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "title": self.title,
            "currency_code": self.currency_code,
            "bank": self.bank_id,
            "is_active": self.is_active
        }
