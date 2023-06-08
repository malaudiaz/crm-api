# warehouse.py

from unicodedata import name
from fastapi import HTTPException
from ...models.offers.offer import Offer
from ...schemas.offers.offer import OfferBase, OfferSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from crm.functions_jwt import get_current_user
from typing import List
import math
from ...schemas.resources.result_object import ResultObject, ResultData

       
def new(request, db: Session, offer: OfferBase):
    
    result = ResultData() 
    currentUser = get_current_user(request) 
    db_offer = Offer(code=offer.code, name=offer.name, description=offer.description, 
                     cost_price=offer.cost_price, sale_price=offer.sale_price, 
                     ledger_account=offer.ledger_account,
                     created_by=currentUser['username'], updated_by=currentUser['username'])
        
    try:
        db.add(db_offer)
        db.commit()
        db.refresh(db_offer)
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = u'Ha ocurrido un error al crear la oferta'               
        raise HTTPException(status_code=403, detail=msg)
    
def get_one(offer_id: str, db: Session):  
    return db.query(Offer).filter(Offer.id == offer_id).first()

def get_all(page: int, per_page: int, total: int, total_pages: int, criteria_key: str, criteria_value: str, db: Session):  
    
    result = ResultData(page=page, per_page=per_page, total=total, total_pages=total_pages)  
    
    str_where = "WHERE t.is_active=True " 
    str_count = "Select count(*) FROM offer.offers t "
    str_query = "Select t.id, code, t.name, t.description, cost_price, sale_price, ledger_account, t.created_by, t.created_date, " \
        "t.updated_by, t.updated_date " \
        "FROM offer.offers t "         
    
    dict_query = {'name': " AND name ilike '%" + criteria_value + "%'",
                  'code': " AND code ilike '%" + criteria_value + "%'",
                  'sale_price': " AND sale_price ilike '%" + criteria_value + "%'",
                  }
    
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
            {'id': item['id'], 
            'created_date': item['created_date'],
            'created_by': item['created_by'],
            'updated_date': item['updated_date'],
            'updated_by': item['updated_by'],
            'code': item['code'], 
            'name': item['name'], 
            'description': item['description'], 
            'cost_price': item['cost_price'], 
            'sale_price' : item['sale_price'], 
            })
    
    return result

def delete(request, offer_id: str, db: Session):
    try:
        currentUser = get_current_user(request) 
        db_offer = db.query(Offer).filter(Offer.id == offer_id).first()
        db_offer.is_active = False
        db_offer.updated_by = currentUser['username']       
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(request, offer_id: str, offer: OfferBase, db: Session):
       
    result = ResultData() 
    currentUser = get_current_user(request)
    db_offer = db.query(Offer).filter(Offer.id == offer_id).first()
    db_offer.updated_by = currentUser['username']
    
    if offer.code:
        db_offer.code=offer.code
    if offer.name:
        db_offer.name=offer.name
    if offer.description:
        db_offer.description=offer.description
    if offer.cost_price:
        db_offer.cost_price = offer.cost_price
    if offer.sale_price:
        db_offer.sale_price = offer.sale_price
    if offer.ledger_account:
        db_offer.ledger_account = offer.ledger_account
    
    try:
        db.add(db_offer)
        db.commit()
        db.refresh(db_offer)
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        # if e.code == "gkpj":
        raise HTTPException(status_code=404, detail=e.message)
