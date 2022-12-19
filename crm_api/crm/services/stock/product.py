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

def get_all(request: List[ProductSchema], skip: int, limit: int, db: Session):  
    lst = db.query(Product).offset(skip).limit(limit).all()                  
    data = []
    for item in lst:
        data.append(item.dict())
    return data
        
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
