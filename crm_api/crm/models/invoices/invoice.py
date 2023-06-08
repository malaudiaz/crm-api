"""coding=utf-8."""

from email.policy import default
import uuid
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Boolean, DateTime, Float
from ...config.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class Invoice(Base):
    """Invoice Class contains standard information for a Invoice."""
 
    __tablename__ = "invoices"
    __table_args__ = {'schema' : 'invoice'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    invoice_number = Column(String(50), nullable=False, unique=False)
    currency = Column(String(3), nullable=False)
    invoice_import = Column(Float, default=float(0.00))
    real_import = Column(Float, default=float(0.00))
    expire_date = Column(DateTime, nullable=False, default=datetime.now())
    observation = Column(String(350), nullable=False)
    status = Column(String(35), nullable=False)
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    def dict(self):
        return {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "currency": self.currency,
            "invoice_import": self.invoice_import,
            "real_import": self.real_import,
            "expire_date": self.expire_date,
            "observation": self.observation,
            "status": self.status,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date
        }
    
# Base.metadata.create_all(bind=engine)
