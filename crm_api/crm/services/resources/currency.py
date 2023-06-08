from unicodedata import name
from fastapi import HTTPException
from ...models.resources.currency import Currency
from ...schemas.resources.currency import CurrencyBase, CurrencyShema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
# from crm.auth_bearer import decodeJWT
from ...auth_bearer import decodeJWT
from typing import List
from sqlalchemy import or_
            
def get_all(request: List[CurrencyBase], db: Session):  
    data = db.query(Currency).all() 
    return data
        
def new(db: Session, currency: CurrencyBase):
    
    db_currency = Currency(code=currency.code, name=currency.name, description=currency.description)
    
    try:
        db.add(db_currency)
        db.commit()
        db.refresh(db_currency)
        return db_currency
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear la moneda'               
        raise HTTPException(status_code=403, detail=msg)

def get_one(currency_code: str, db: Session):  
    return db.query(Currency).filter(Currency.code == currency_code).first()

def get_one_by_name(name: str, db: Session):  
    return db.query(Currency).filter(Currency.name == name).first()

def delete(currency_code: str, db: Session):
    try:
        db_currency = db.query(Currency).filter(Currency.code == currency_code).first()
        db.delete(db_currency)
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(currency_code: str, currency: CurrencyBase, db: Session):
       
    db_currency = db.query(Currency).filter(Currency.code == currency_code).first()
    
    db_currency.name = currency.name
    db_currency.updated_by = 'foo'
    db_currency.description=currency.description
        
    try:
        db.add(db_currency)
        db.commit()
        db.refresh(db_currency)
        return db_currency
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe una moneda con este Codigo")
        