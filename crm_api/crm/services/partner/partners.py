# partner.py

import math
import datetime
from unicodedata import name
from fastapi import HTTPException
from ...models.partner.partner import Partner
from ...models.partner.contacto import PartnerContact
from ...schemas.partner.partner import PartnerBase, PartnerShema
from ...services.partner.contact import asociate_partner_contact_with_object, update_partner_contact_with_object
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from crm.functions_jwt import get_current_user
from ...auth_bearer import decodeJWT
from typing import List

def get_all(page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    
    str_where = "WHERE is_active=True " 
    str_count = "Select count(*) FROM partner.partners "
    str_query = "Select id, name, address, dni, email, phone, mobile, nit, is_provider, created_by, created_date, " \
        "updated_by, updated_date, registration_number, registration_user, registration_date, type FROM partner.partners "
    
    dict_query = {'name': " AND name ilike '%" + criteria_value + "%'",
                  'nit': " AND nit = '" + criteria_value + "'",
                  'type': " AND type = '" + criteria_value + "'",
                  'registration_number': " AND registration_number = '" + criteria_value + "'",
                  'dni': " AND dni ilike '%" + criteria_value + "%'"}
    
    if criteria_key and criteria_key not in dict_query:
        raise HTTPException(status_code=404, detail="Parametro no válido") 
    
    str_where = str_where + dict_query[criteria_key] if criteria_value else str_where  
    str_count += str_where 
    str_query += str_where
    
    total = db.execute(str_count).scalar()
    total_pages=total/per_page if (total % per_page == 0) else math.trunc(total / per_page) + 1
    
    str_query += " ORDER BY name LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
     
    lst_data = db.execute(str_query)
    data = []
    for item in lst_data:
        data.append({'id': item['id'], 'name' : item['name'], 'address': item['address'], 
                     'dni': item['dni'], 'email': item['email'], 'phone': item['phone'], 
                     'mobile': item['mobile'], 'nit': item['nit'], 'is_provider': item['is_provider'], 
                     'created_by': item['created_by'], 'nit': item['nit'], 'registration_number': item['registration_number'], 
                     'type': item['type'], 'registration_user': item['registration_user'], 
                     'registration_date': item['registration_date'],  'selected': False})
    
    return {"page": page, "per_page": per_page, "total": total, "total_pages": total_pages, "data": data}

def get_one(partner_id: str, db: Session):  
    return db.query(Partner).filter(Partner.id == partner_id).first()

def get_one_by_registration_number(registration_number: str, db: Session):  
    return db.query(Partner).filter(Partner.registration_number == registration_number).first()

def new(request, db: Session, partner: PartnerBase):
    
    currentUser = get_current_user(request) 
    
    db_partner = Partner(type=partner.type, name=partner.name, address=partner.address, dni=partner.dni, 
                         email=partner.email, phone=partner.phone, mobile=partner.mobile, nit=partner.nit,
                         registration_number=partner.registration_number, registration_user=partner.registration_user,
                         registration_date=partner.registration_date, created_by=currentUser['username'], updated_by=currentUser['username'])
  
    try:
        
        db.add(db_partner)
        db.commit()
        db.refresh(db_partner)
        
        if partner.contacts:
            for item_co in partner.contacts:
                # puede existir o no el contacto...
                asociate_partner_contact_with_object(
                    partner_id=db_partner.id, contact=item_co, user_name=currentUser['username'], db=db)
                
        return True
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear el cliente'               
        raise HTTPException(status_code=403, detail=msg)
    
def delete(request, partner_id: str, db: Session):
    
    currentUser = get_current_user(request) 
    
    try:
        db_partner = db.query(Partner).filter(Partner.id == partner_id).first()
        db_partner.is_active = False
        db_partner.updated_by = currentUser['username']
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(request, partner_id: str, partner: PartnerBase, db: Session):
    
    currentUser = get_current_user(request) 
       
    db_partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not db_partner:
        raise HTTPException(status_code=400, detail="No existe cliente con ese ID")
    
    db_partner.updated_by = currentUser['username']
    db_partner.updated_date = datetime.datetime.now()

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
        
        if partner.contacts:
            update_partner_contact_with_object(
                    partner_id=db_partner.id, contacts=partner.contacts, user_name=currentUser['username'], db=db)
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un cliente Registrado")
