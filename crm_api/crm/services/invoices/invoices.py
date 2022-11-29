from unicodedata import name
from fastapi import HTTPException
from ...models.invoices.invoice import Invoice
from ...schemas.invoices.invoice import InvoiceBase, InvoiceShema, InvoiceImports
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from typing import List
            
def get_all(request: List[InvoiceShema], skip: int, limit: int, db: Session):  
    data = db.query(Invoice).offset(skip).limit(limit).all()                  
    return data
        
def new(db: Session, invoice: InvoiceBase):
    
    db_invoice = Invoice(invoice_number=invoice.invoice_number, currency=invoice.currency, invoice_import=invoice.invoice_import, 
                         real_import=invoice.real_import, expire_date=invoice.expire_date, observation=invoice.observation, status=invoice.status,
                         created_by='foo', updated_by='foo')
    
    try:
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        return db_invoice
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear la Factura'               
        raise HTTPException(status_code=403, detail=msg)
    
def get_one(invoice_id: str, db: Session):  
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

def delete(invoice_id: str, db: Session):
    try:
        db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        db_invoice.status = 'DELETED'
        db_invoice.updated_by = 'foo'
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(invoice_id: str, invoice: InvoiceBase, db: Session):
       
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    
    db_invoice.invoice_number = invoice.invoice_number
    db_invoice.updated_by = 'foo'
    db_invoice.currency=invoice.currency
    db_invoice.invoice_import=invoice.invoice_import
    db_invoice.real_import=invoice.real_import
    db_invoice.expire_date=invoice.expire_date
    db_invoice.observation=invoice.observation
    db_invoice.status=invoice.status
    
    try:
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        return db_invoice
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un factura con este Nombre")
        
def update_real_imports(invoice_number: str, invoice: InvoiceImports, db: Session):
    
    db_invoice = db.query(Invoice).filter(Invoice.invoice_number == invoice_number).first()
    
    db_invoice.invoice_import=invoice.invoice_import
    db_invoice.real_import=invoice.real_import
    
    try:
        
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        return db_invoice
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un factura con este Nombre")