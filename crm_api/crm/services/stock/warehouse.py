# warehouse.py

from unicodedata import name
from fastapi import HTTPException
from ...models.stock.warehouse import Warehouse
from ...schemas.stock.warehouse import WarehouseSchema, WarehouseBase, UpdateWarehouse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from typing import List

def get_all(request: List[WarehouseSchema], skip: int, limit: int, db: Session):  
    lst = db.query(Warehouse).offset(skip).limit(limit).all()                  
    data = []
    for item in lst:
        data.append(item.dict())
    return data
        
def new(db: Session, warehouse: WarehouseBase):
    
    db_warehouse = Warehouse(name=warehouse.name, code=warehouse.code, address=warehouse.address, 
                             created_by='foo', updated_by='foo')
        
    try:
        db.add(db_warehouse)
        db.commit()
        db.refresh(db_warehouse)
        return db_warehouse
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = u'Ha ocurrido un error al crear el almacén'               
        raise HTTPException(status_code=403, detail=msg)
    
def get_one(warehouse_id: str, db: Session):  
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

def delete(warehouse_id: str, db: Session):
    try:
        db_warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
        db_warehouse.is_active = False
        db_warehouse.updated_by = 'foo' 
        
        if len(db_warehouse.locations) != 0:
            for item in db_warehouse.locations:
                item.is_active = False
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(warehouse_id: str, warehouse: UpdateWarehouse, db: Session):
       
    db_warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    db_warehouse.updated_by = 'foo'
    
    if warehouse.name:
        db_warehouse.name=warehouse.name
    if warehouse.address:
        db_warehouse.address=warehouse.address
    if warehouse.code:
        db_warehouse.code = warehouse.code
    
    db_warehouse.is_active = warehouse.is_active
    
    try:
        db.add(db_warehouse)
        db.commit()
        db.refresh(db_warehouse)
        return db_warehouse
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un almacen con este Nombre")
