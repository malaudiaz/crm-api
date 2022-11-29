# contract.py

from unicodedata import name
from fastapi import HTTPException
from ...models.contracts.contract import Contract
from ...schemas.contracts.contracts import ContractBase, ContractShema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from typing import List

from ...services.partner.partners import get_one as partner_get_one
from ...services.partner.contact import get_one as contact_get_one
    
def get_all(totalCount: int, skip: int, limit: int, db: Session):  
    
    str_query = "Select count(*) FROM contract.contracts where is_active=True "
        
    totalCount = db.execute(str_query).scalar() if totalCount == 0 else totalCount
    data = db.query(Contract).offset(skip).limit(limit).all()  
    return {'totalCount': int(totalCount), 'lst_data': data}

def get_one(contract_id: str, db: Session):  
    return db.query(Contract).filter(Contract.id == contract_id).first()

def get_by_number(number: str, db: Session):  
    return db.query(Contract).filter(Contract.number == number).first()

def new(db: Session, contract: ContractBase):
    
    db_contract = Contract(number=contract.number, id_partner=contract.id_partner, id_contact=contract.id_contact, sign_by=contract.sign_by,
                           sign_date=contract.sign_date, initial_aproved_import=contract.initial_aproved_import, 
                           real_aproved_import=contract.initial_aproved_import, real_import=contract.initial_aproved_import,
                           is_supplement=contract.is_supplement, created_by='foo', updated_by='foo')
  
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
   
