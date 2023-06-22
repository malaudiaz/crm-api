# warehouse.py

from unicodedata import name
from fastapi import HTTPException
from ...models.stock.product import Product
from ...schemas.stock.product import ProductBase, ProductSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from typing import List
import math
from ...schemas.resources.result_object import ResultObject, ResultData

# def get_all(request: List[ProductSchema], skip: int, limit: int, db: Session):  
#     lst = db.query(Product).offset(skip).limit(limit).all()                  
#     data = []
#     for item in lst:
#         data.append(item.dict())
#     return data
        
def new(db: Session, product: ProductBase):
    
    db_product = Product(code=product.code, name=product.name, description=product.description, 
                         measure_id=product.measure_id, unit_price=product.unit_price, 
                         cost_price=product.cost_price, sale_price=product.sale_price, 
                         ledger_account=product.ledger_account,
                         created_by='foo', updated_by='foo')
        
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = u'Ha ocurrido un error al crear el producto'               
        raise HTTPException(status_code=403, detail=msg)
    
def get_one(product_id: str, db: Session):  
    return db.query(Product).filter(Product.id == product_id).first()

def get_all(page: int, per_page: int, total: int, total_pages: int, criteria_key: str, criteria_value: str, db: Session):  
    
    result = ResultData(page=page, per_page=per_page, total=total, total_pages=total_pages)  
    
    str_where = "WHERE p.is_active=True " 
    str_count = "Select count(*) FROM stock.products p "
    str_query = "Select p.id, code, p.name, p.description, unit_price, cost_price, sale_price, ledger_account, p.created_by, p.created_date, " \
        "p.updated_by, p.updated_date, measure_id, m.name measure_name " \
        "FROM stock.products p " \
        "inner join stock.measure m on m.id = p.measure_id "
    
    dict_query = {'name': " AND name ilike '%" + criteria_value + "%'",
                  'code': " AND code = '" + criteria_value + "'",
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
            'code': item['code'], 
            'name' : item['name'], 
            'description': item['description'], 
            'measure': item['measure_name'], 
            'created_date': item['created_date'],
            'created_by': item['created_by'],
            'update_date': item['updated_date'],
            'updated_by': item['updated_by'],
            'movements': []
            })
    
    return result

def delete(product_id: str, db: Session):
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        db_product.is_active = False
        db_product.updated_by = 'foo'         
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(product_id: str, product: ProductBase, db: Session):
       
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db_product.updated_by = 'foo'
    
    if product.code:
        db_product.code=product.code
    if product.name:
        db_product.name=product.name
    if product.description:
        db_product.description=product.description
    if product.measure_id:
        db_product.measure_id = product.measure_id
    if product.unit_price:
        db_product.unit_price = product.unit_price
    if product.cost_price:
        db_product.cost_price = product.cost_price
    if product.sale_price:
        db_product.sale_price = product.sale_price
    if product.ledger_account:
        db_product.ledger_account = product.ledger_account
    
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        # if e.code == "gkpj":
        raise HTTPException(status_code=404, detail=e.message)
