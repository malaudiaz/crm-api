# location.py

from unicodedata import name
from fastapi import HTTPException
from ...models.stock.location import Location
from ...schemas.stock.location import LocationBase, LocationSchema, UpdateLocation
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from typing import List

def get_all(request: List[LocationSchema], skip: int, limit: int, db: Session):  
    lst = db.query(Location).offset(skip).limit(limit).all()                  
    
    data = []
    for item in lst:
        data.append(item.dict())
    return data
        
def new(db: Session, location: LocationBase):
    
    db_location = Location(name=location.name, corridor=location.corridor, floor=location.floor, observation=location.observation,
                           warehouse_id=location.warehouse_id, created_by='foo', updated_by='foo')
    # db_warehouse.locations = []
    
    try:
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        return db_location
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe una localidad con ese nombre")
        else:
            msg = u'Ha ocurrido un error al crear la localidación'               
            raise HTTPException(status_code=403, detail=msg)
    
def get_one(location_id: str, db: Session):  
    location = db.query(Location).filter(Location.id == location_id).first()

    data = {}
    if location:
        data = location.dict()    
    return data

def delete(location_id: str, db: Session):
    try:
        db_location = db.query(Location).filter(Location.id == location_id).first()
        db_location.is_active = False
        db_location.updated_by = 'foo'
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(location_id: str, location: UpdateLocation, db: Session):
       
    db_location = db.query(Location).filter(Location.id == location_id).first()
    db_location.updated_by = 'foo'
    
    if location.name:
        db_location.name=location.name
    if location.corridor != 0:
        db_location.corridor=location.corridor
    if location.floor != 0:
        db_location.floor = location.floor
    
    if location.warehouse_id:
        db_location.warehouse_id = location.warehouse_id
    
    db_location.is_active = location.is_active
    
    try:
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        return db_location
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe una localidad con ese nombre")
