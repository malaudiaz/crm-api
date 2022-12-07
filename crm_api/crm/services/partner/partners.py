# partner.py

import math
from unicodedata import name
from fastapi import HTTPException
from ...models.partner.partner import Partner
from ...schemas.partner.partner import PartnerBase, PartnerShema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from typing import List

def get_all(page: int, per_page: int, db: Session, name=''):  
    
    str_query = "Select count(*) FROM partner.partners where is_active=True "
    if name:
        str_query += " AND name ilike '%" + name + "%'"
        
    total = db.execute(str_query).scalar()
    total_pages=total/per_page if (total % per_page == 0) else math.trunc(total / per_page) + 1
    
    if name:
        data = db.query(Partner).filter(Partner.name.ilike(f'%{name}%')).offset(page*per_page-per_page).limit(per_page).all() 
    else:
        data = db.query(Partner).offset(page*per_page-per_page).limit(per_page).all()  
         
    return {"page": page, "per_page": per_page, "total": total, "total_pages": total_pages, "data": data}

def get_all_old(totalCount: int, skip: int, limit: int, db: Session, name=''):  
    
    str_query = "Select count(*) FROM partner.partners where is_active=True "
    if name:
        str_query += " AND name ilike '%" + name + "%'"
        
    totalCount = db.execute(str_query).scalar() if totalCount == 0 else totalCount
    if name:
        data = db.query(Partner).filter(Partner.name.ilike(f'%{name}%')).offset(skip).limit(limit).all() 
    else:
        data = db.query(Partner).filter(Partner.is_active == True).order_by(Partner.dni.asc()).offset(skip).limit(limit).all()  
         
    return {'totalCount': int(totalCount), 'lst_data': data}

def get_one(partner_id: str, db: Session):  
    return db.query(Partner).filter(Partner.id == partner_id).first()

def get_one_by_registration_number(registration_number: str, db: Session):  
    return db.query(Partner).filter(Partner.registration_number == registration_number).first()

def get_by_name(request: List[PartnerShema], name: str, skip: int, limit: int, db: Session):  
    return db.query(Partner).filter(Partner.name.ilike(f'%{name}%')).offset(skip).limit(limit).all() 

def get_by_dni(equest: List[PartnerShema], dni: str, skip: int, limit: int, db: Session):  
    return db.query(Partner).filter(Partner.dni.ilike(f'%{dni}%')).offset(skip).limit(limit).all()

def get_by_nit(equest: List[PartnerShema], nit: str, skip: int, limit: int, db: Session):  
    return db.query(Partner).filter(Partner.nit.ilike(f'%{nit}%')).offset(skip).limit(limit).all()

def new(db: Session, partner: PartnerBase):
    
    db_partner = Partner(type=partner.type, name=partner.name, address=partner.address, dni=partner.dni, 
                         email=partner.email, phone=partner.phone, mobile=partner.mobile, nit=partner.nit,
                         registration_number=partner.registration_number, registration_user=partner.registration_user,
                         registration_date=partner.registration_date, created_by='foo', updated_by='foo')
  
    try:
        db.add(db_partner)
        db.commit()
        db.refresh(db_partner)
        return db_partner
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear el cliente'               
        raise HTTPException(status_code=403, detail=msg)
    
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
    db_partner.type=partner.type
    db_partner.name=partner.name
    db_partner.address=partner.address
    db_partner.dni=partner.dni
    db_partner.email=partner.email
    db_partner.phone=partner.phone
    db_partner.mobile=partner.mobile
    db_partner.nit=partner.nit
    db_partner.registration_number=partner.registration_number
    db_partner.registration_user=partner.registration_user
    db_partner.registration_date=partner.registration_date

    try:
        db.add(db_partner)
        db.commit()
        db.refresh(db_partner)
        return db_partner
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un cliente Registrado")
