# partner.py

from unicodedata import name
from fastapi import HTTPException
# from crm.models.partner.partner import Partner
from ...models.partner.partner import Partner
# from crm.schemas.partner.partner import PartnerBase, PartnerShema
from ...schemas.partner.partner import PartnerBase, PartnerShema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
# from crm.auth_bearer import decodeJWT
from ...auth_bearer import decodeJWT
from typing import List

def get_all(request: List[PartnerShema], skip: int, limit: int, db: Session):  
    data = db.query(Partner).offset(skip).limit(limit).all()                  
    return data
        
def new(db: Session, partner: PartnerBase):
    
    db_partner = Partner(name=partner.name, address=partner.address, dni=partner.dni, 
                         email=partner.email, phone=partner.phone, mobile=partner.mobile, nit=partner.nit,
                         created_by='foo', updated_by='foo')
    
    try:
        db.add(db_partner)
        db.commit()
        db.refresh(db_partner)
        return db_partner
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear el cliente'               
        raise HTTPException(status_code=403, detail=msg)
    
def get_one(partner_id: str, db: Session):  
    return db.query(Partner).filter(Partner.id == partner_id).first()

def delete(partner_id: str, db: Session):
    try:
        db_partner = db.query(Partner).filter(Partner.id == partner_id).first()
        db_partner.is_active = False
        db_partner.updated_by = 'foo'
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(partner_id: str, partner: PartnerBase, db: Session):
       
    db_partner = db.query(Partner).filter(Partner.id == partner_id).first()
    db_partner.is_active = False
    db_partner.updated_by = 'foo'
    db_partner.name=partner.name
    db_partner.address=partner.address
    db_partner.dni=partner.dni
    db_partner.email=partner.email
    db_partner.phone=partner.phone
    db_partner.mobile=partner.mobile
    db_partner.nit=partner.nit

    try:
        db.add(db_partner)
        db.commit()
        db.refresh(db_partner)
        return db_partner
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un usuario con este Nombre")
