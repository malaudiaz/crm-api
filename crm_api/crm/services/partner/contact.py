# contact.py

import math
from unicodedata import name
from fastapi import HTTPException
from ...models.partner.contacto import Contact, PartnerContact
from ...schemas.partner.contact import ContactBase, ContactShema, PartnerContactBase, PartnerContactRelation
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from typing import List

from ...services.partner.partners import get_one as partner_get_one

def get_all(page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    
    str_where = "WHERE is_active=True " 
    str_count = "Select count(*) FROM partner.contacts "
    str_query = "Select id, name, address, dni, email, phone, mobile, created_by, created_date, " \
        "updated_by, updated_date FROM partner.contacts "
    
    dict_query = {'name': " AND name ilike '%" + criteria_value + "%'",
                  'phone': " AND phone = '" + criteria_value + "'",
                  'mobile': " AND mobile = '" + criteria_value + "'",
                  'dni': " AND dni ilike '%" + criteria_value + "%'"}
    
    str_where = str_where + dict_query[criteria_key] if criteria_value else ""  
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
                     'mobile': item['mobile'], 'selected': False})
    
    return {"page": page, "per_page": per_page, "total": total, "total_pages": total_pages, "data": data}
    
def get_one(contact_id: str, db: Session):  
    return db.query(Contact).filter(Contact.id == contact_id).first()

def new(db: Session, contact: ContactBase):
    
    db_contact = Contact(name=contact.name, address=contact.address, dni=contact.dni, 
                         email=contact.email, phone=contact.phone, mobile=contact.mobile, 
                         created_by='foo', updated_by='foo')
  
    try:
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear el contacto'               
        raise HTTPException(status_code=403, detail=msg)
    
def delete(contact_id: str, db: Session):
    try:
        db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
        db_contact.is_active = False
        db_contact.updated_by = 'foo'
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(contact_id: str, contact: ContactBase, db: Session):
       
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db_contact.updated_by = 'foo'
    db_contact.name=contact.name
    db_contact.address=contact.address
    db_contact.dni=contact.dni
    db_contact.email=contact.email
    db_contact.phone=contact.phone
    db_contact.mobile=contact.mobile
    
    try:
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un contacto Registrado")
   
def asociate_partner_contact(partnercontact: PartnerContactBase, db: Session):
    
    partner = partner_get_one(partnercontact.id_partner, db=db)
    if not partner:
        raise HTTPException(status_code=400, detail="No Existe Cliente con ese ID")
    
    contact = get_one(partnercontact.id_contact, db=db)
    if not contact:
        raise HTTPException(status_code=400, detail="No Existe Contacto con ese ID")
    
    db_partnercontact = db.query(PartnerContact).filter_by(id_partner = partnercontact.id_partner, id_contact = partnercontact.id_contact).first()
    if db_partnercontact:
        raise HTTPException(status_code=400, detail="Existe relacion registrada entre Cliente y este contacto")
    
    db_partnercontact = PartnerContact(id_partner=partnercontact.id_partner, id_contact=partnercontact.id_contact, 
                                       id_relationtype=partnercontact.id_relationtype, created_by='foo', updated_by='foo')
    
    try:
        db.add(db_partnercontact)
        db.commit()
        db.refresh(db_partnercontact)
        return True
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al asociar el cliente y su contacto'               
        raise HTTPException(status_code=403, detail=msg)
    
def desasociate_partner_contact(partnercontactdelete: PartnerContactRelation, db: Session):
    
    partner = partner_get_one(partnercontactdelete.id_partner, db=db)
    if not partner:
        raise HTTPException(status_code=400, detail="No Existe Cliente con ese ID")
    
    contact = get_one(partnercontactdelete.id_contact, db=db)
    if not contact:
        raise HTTPException(status_code=400, detail="No Existe Contacto con ese ID")
       
    db_partnercontact = db.query(PartnerContact).filter_by(id_partner = partnercontactdelete.id_partner, 
                                                           id_contact = partnercontactdelete.id_contact).first()
    if not db_partnercontact:
        raise HTTPException(status_code=400, detail="No existe un contacto Registrado a ese Cliente")
    
    try:
        db.delete(db_partnercontact)
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
