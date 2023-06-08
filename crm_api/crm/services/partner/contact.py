# contact.py

import math
from unicodedata import name
from fastapi import HTTPException
from ...models.partner.contacto import Contact, PartnerContact
from ...schemas.partner.contact import ContactBase, ContactShema, PartnerContactBase, PartnerContactRelation, ContactCreate
from ...schemas.resources.result_object import ResultObject, ResultData
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from typing import List

def get_all(page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    
    result = ResultData(page=page, per_page=per_page)  
        
    str_where = "WHERE is_active=True " 
    str_count = "Select count(*) FROM partner.contacts "
    str_query = "Select id, name, job, address, dni, email, phone, mobile, created_by, created_date, " \
        "updated_by, updated_date FROM partner.contacts "
    
    dict_query = {'name': " AND name ilike '%" + criteria_value + "%'",
                  'phone': " AND phone = '" + criteria_value + "'",
                  'mobile': " AND mobile = '" + criteria_value + "'",
                  'dni': " AND dni ilike '%" + criteria_value + "%'"}
    
    if criteria_key and criteria_key not in dict_query:
        raise HTTPException(status_code=404, detail="Parametro no válido")
    
    str_where = str_where + dict_query[criteria_key] if criteria_value else str_where 
    str_count += str_where 
    str_query += str_where
    
    result.total = db.execute(str_count).scalar()
    result.total_pages=result.total/result.per_page if (result.total % result.per_page == 0) else math.trunc(result.total / result.per_page) + 1
    
    str_query += " ORDER BY name LIMIT " + str(result.per_page) + " OFFSET " + str(result.page*result.per_page-result.per_page)
     
    lst_data = db.execute(str_query)
    result.data = []
    for item in lst_data:
        result.data.append(
            {'id': item['id'], 'name' : item['name'], 'address': item['address'], 
             'dni': item['dni'], 'email': item['email'], 'phone': item['phone'], 
             'mobile': item['mobile'], 'job': item['job'], 'selected': False})
    
    return result

def get_one_contact(contact_id: str, db: Session): 
    result = ResultData()
    result.data = {}
    result.data = get_one(contact_id=contact_id, db=db)
    return result

def get_one(contact_id: str, db: Session): 
    return db.query(Contact).filter(Contact.id == contact_id).first()
    
def get_contacts_by_partner(page: int, per_page: int, partner_id: str, db: Session): 
    
    result = ResultData(page=page, per_page=per_page)  
    
    str_where = "WHERE con.is_active=True AND id_partner = '" + partner_id + "' "
    str_count = "SELECT count(id_partner) FROM partner.partners_contacts pac " \
        "JOIN partner.contacts con ON con.id = pac.id_contact " 
        
    str_query = "SELECT id_contact, name, address, dni, email, phone, mobile, job " \
        "FROM partner.partners_contacts pac " \
        "JOIN partner.contacts con ON con.id = pac.id_contact " 
    
    str_count += str_where 
    str_query += str_where
    
    result.total = db.execute(str_count).scalar()
    result.total_pages=result.total/result.per_page if (result.total % result.per_page == 0) else math.trunc(result.total / result.per_page) + 1
    
    str_query += " ORDER BY name LIMIT " + str(result.per_page) + " OFFSET " + str(result.page*result.per_page-result.per_page)
     
    lst_data = db.execute(str_query)
    result.data = []
    for item in lst_data:
        result.data.append(
            {'id': item['id_contact'], 'name' : item['name'], 'address': item['address'], 
             'dni': item['dni'], 'email': item['email'], 'phone': item['phone'], 
             'mobile': item['mobile'], 'job': item['job'], 'selected': False})
    
    return result
    
def get_lst_contacts_by_partner_id(partner_id: str, db: Session): 
    
    result = ResultData()
    
    str_query = "SELECT id_contact, name, address, dni, email, phone, mobile, job " \
        "FROM partner.partners_contacts pac " \
        "JOIN partner.contacts con ON con.id = pac.id_contact " \
        "WHERE con.is_active=True AND id_partner = '" + partner_id + "' " \
        "ORDER BY name"
    
    lst_data = db.execute(str_query)
    result.data = []
    for item in lst_data:
        result.data.append({
            'id': item['id_contact'], 'name' : item['name'], 'address': item['address'], 
            'dni': item['dni'], 'email': item['email'], 'phone': item['phone'], 
            'mobile': item['mobile'], 'job': item['job'], 'selected': False})
    
    return result

def get_lst_contact_id_by_partner_id(partner_id: str, db: Session): 
    
    str_query = "SELECT id_contact FROM partner.partners_contacts pac " \
        "JOIN partner.contacts con ON con.id = pac.id_contact " \
        "WHERE con.is_active=True AND id_partner = '" + partner_id + "' "
    
    lst_data = db.execute(str_query)
    
    data = []
    for item in lst_data:
        data.append(item['id_contact'])
    
    return data

def new(db: Session, contact: ContactBase):
    
    result = ResultData()
    
    db_contact = Contact(name=contact.name, job=contact.job, address=contact.address, dni=contact.dni, 
                         email=contact.email, phone=contact.phone, mobile=contact.mobile, 
                         created_by='foo', updated_by='foo')
  
    try:
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear el contacto'               
        raise HTTPException(status_code=403, detail=msg)
    
def create_contact(db: Session, contact: ContactCreate, user_name: str):
    
    db_contact = Contact(name=contact.name, job=contact.job, address=contact.address, dni=contact.dni, 
                         email=contact.email, phone=contact.phone, mobile=contact.mobile, 
                         created_by=user_name, updated_by=user_name)
  
    try:
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact.id
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear el contacto'               
        raise HTTPException(status_code=403, detail=msg)
    
def delete(contact_id: str, db: Session):
    result = ResultData()
    
    try:
        db_contact = get_one(contact_id=contact_id, db=db)
        db_contact.is_active = False
        db_contact.updated_by = 'foo'
        db.commit()
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(contact_id: str, contact: ContactBase, db: Session):
    
    result = ResultData()
       
    db_contact = get_one(contact_id=contact_id, db=db)
    db_contact.updated_by = 'foo'
    db_contact.name=contact.name
    db_contact.job= contact.job
    db_contact.address=contact.address
    db_contact.dni=contact.dni
    db_contact.email=contact.email
    db_contact.phone=contact.phone
    db_contact.mobile=contact.mobile
    
    try:
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un contacto Registrado")
   
def asociate_partner_contact(partnercontact: PartnerContactBase, db: Session):
    
    result = ResultData()
    
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
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al asociar el cliente y su contacto'               
        raise HTTPException(status_code=403, detail=msg)
    
def desasociate_partner_contact(partnercontactdelete: PartnerContactRelation, db: Session):
    
    result = ResultData()
    
    # partner = partner_get_one(partnercontactdelete.id_partner, db=db)
    # if not partner:
    #     raise HTTPException(status_code=400, detail="No Existe Cliente con ese ID")
    
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
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")

def desasociate_partner_one_contact(partner_id: str, contact_id:str, db: Session):
    
    result = ResultData()
    
    db_partnercontact = db.query(PartnerContact).filter_by(id_partner = partner_id, id_contact = contact_id).first()
    if not db_partnercontact:
        return result
    
    try:
        db.delete(db_partnercontact)
        db.commit()
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def asociate_partner_contact_with_object(partner_id: str, contact: ContactCreate, user_name: str, db: Session):
    
    one_contact = get_one(contact.id, db=db)
    if not one_contact:
        contact_id = create_contact(db=db, contact=contact, user_name=user_name)
    else:
        contact_id =  one_contact.id
        db_partnercontact = db.query(PartnerContact).filter_by(id_partner=partner_id, id_contact=contact_id).first()
        if db_partnercontact:
            return True
    
    db_partnercontact = PartnerContact(id_partner=partner_id, id_contact=contact_id, 
                                       id_relationtype=None, created_by=user_name, updated_by=user_name)
    
    try:
        db.add(db_partnercontact)
        db.commit()
        return True
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al asociar el cliente y su contacto'               
        raise HTTPException(status_code=403, detail=msg)
    
def update_partner_contact_with_object(partner_id: str, contacts: List[ContactCreate], user_name: str, db: Session):
    
    lst_contacts_initial = get_lst_contact_id_by_partner_id(partner_id, db=db)
    
    lst_contacts_currrent = []
    
    for item_co in contacts:
        # puede existir o no el contacto..., también puede eliminarse
        if item_co.id:
            lst_contacts_currrent.append(item_co.id)
            
        asociate_partner_contact_with_object(
            partner_id=partner_id, contact=item_co, user_name=user_name, db=db)
    
    # borrar los que ya no vienen
    for item in lst_contacts_initial:
        if item in lst_contacts_currrent:
            continue
        desasociate_partner_one_contact(partner_id=partner_id, contact_id=item, db=db)
        
    return True
