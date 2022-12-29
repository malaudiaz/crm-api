# contract.py

import math
from unicodedata import name
from fastapi import HTTPException
from ...models.contracts.contract import Contract
from ...schemas.contracts.contracts import ContractBase, ContractShema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from crm.functions_jwt import get_current_user
from ...auth_bearer import decodeJWT
from typing import List

from ...services.partner.partners import get_one as partner_get_one
from ...services.partner.contact import get_one as contact_get_one

def get_all(page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    
    str_where = " WHERE cont.is_active=True "
    str_inner = " INNER JOIN partner.partners pa ON pa.id = cont.id_partner INNER JOIN partner.contacts co ON co.id = cont.id_contact " \
        "JOIN resources.status_element st ON st.name = cont.status_name " \
        "LEFT JOIN enterprise.users us ON us.id = cont.sign_by "
    str_count = "Select count(*) FROM contract.contracts cont"
    str_query = "Select cont.id, number, pa.name as partner_name, co.name as contact_name, sign_by,  us.fullname as sign_full_name, " \
        "sign_date, initial_aproved_import, real_aproved_import, real_import, " \
        "is_supplement, contract_id, cont.created_date, status_name, st.description as status_description " \
        "FROM contract.contracts cont "
    
    dict_query = {'number': " AND number ilike '%" + criteria_value + "%'",
                  'nit': " AND nit = '" + criteria_value + "'",
                  'registration_number': " AND registration_number = '" + criteria_value + "'",
                  'dni': " AND dni ilike '%" + criteria_value + "%'"}
    
    str_count += str_inner
    str_query += str_inner
    
    str_where = str_where + dict_query[criteria_key] if criteria_value else str_where 
     
    str_count += str_where 
    str_query += str_where
    
    total = db.execute(str_count).scalar()
    total_pages=total/per_page if (total % per_page == 0) else math.trunc(total / per_page) + 1
    
    str_query += " ORDER BY number LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
    
    lst_data = db.execute(str_query)
    data = []
    for item in lst_data:
        data.append({'id': item['id'], 'number' : item['number'], 'partner': item['partner_name'], 
                     'contact': item['contact_name'], 'sign_by': item['sign_by'], 'sign_full_name': item['sign_full_name'], 
                     'sign_date': item['sign_date'], 
                     'initial_aproved_import': item['initial_aproved_import'], 'real_aproved_import': item['real_aproved_import'],  
                     'real_import': item['real_import'], 'selected': False, 'status_name': item['status_name'], 
                    "status_description": item['status_description']})
    
    return {"page": page, "per_page": per_page, "total": total, "total_pages": total_pages, "data": data}
    
def get_one(contract_id: str, db: Session):  
    return db.query(Contract).filter(Contract.id == contract_id).first()

def new(request, db: Session, contract: ContractBase):
    
    currentUser = get_current_user(request) 
    
    db_contract = Contract(number=contract.number, id_partner=contract.id_partner, id_contact=contract.id_contact, sign_by=contract.sign_by,
                           sign_date=contract.sign_date, initial_aproved_import=contract.initial_aproved_import, 
                           real_aproved_import=contract.initial_aproved_import, real_import=contract.initial_aproved_import,
                           is_supplement=False, created_by=currentUser['username'], updated_by=currentUser['username'],
                           status_name='DELIVERED')
  
    try:
        db.add(db_contract)
        db.commit()
        db.refresh(db_contract)
        return db_contract
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear el contrato'               
        raise HTTPException(status_code=403, detail=msg)
    
def delete(contract_id: str, db: Session):
    try:
        db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
        db_contract.is_active = False
        db_contract.updated_by = 'foo'
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(contract_id: str, contract: ContractBase, db: Session):
       
    db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
    db_contract.updated_by = 'foo'
    db_contract.number=contract.number
    db_contract.id_partner=contract.id_partner
    db_contract.id_contact=contract.id_contact
    db_contract.sign_by=contract.sign_by
    db_contract.sign_date=contract.sign_date
    db_contract.initial_aproved_import=contract.initial_aproved_import
    db_contract.real_aproved_import=contract.real_aproved_import
    db_contract.real_import=contract.real_import
    db_contract.is_supplement=contract.is_supplement
                           
    try:
        db.add(db_contract)
        db.commit()
        db.refresh(db_contract)
        return db_contract
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un contacto Registrado")
   
