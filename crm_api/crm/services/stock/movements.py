# movements.py

from unicodedata import name
from fastapi import HTTPException
from ...models.stock.movement import Movement
from ...models.stock.location import Location
from ...models.resources.status import StatusElement
from ...models.stock.product import Product
from ...schemas.stock.movement import MovementBase, MovementShema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from typing import List

def get_all(request: List[MovementShema], skip: int, limit: int, db: Session):  
    lst = db.query(Movement).offset(skip).limit(limit).all()                  
    
    data = []
    for item in lst:
        data.append(item.dict())
    return data
        
def new(db: Session, movement: MovementBase):
    
    db_movement = Movement(quantity=movement.quantity, measure_id=movement.measure_id, 
                           document_number=movement.document_number, status_id=movement.status_id,
                           source=movement.source, destiny=movement.destiny, product_id=movement.product_id,
                           created_by='foo', updated_by='foo', )
    
    # try:
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement.dict()
    # except (Exception, SQLAlchemyError, IntegrityError) as e:
    #     print(e)
    #     msg = u'Ha ocurrido un error al crear el movimiento'               
    #     raise HTTPException(status_code=403, detail=msg)
    
def get_one(movement_id: str, db: Session):  
    movement = db.query(Movement).filter(Movement.id == movement_id).first()

    data = {}
    if movement:
        data = movement.dict()    
    return data

def delete(movement_id: str, db: Session):
    try:
        db_movement = db.query(Movement).filter(Movement.id == movement_id).first()
        db_movement.updated_by = 'foo'
        
        if db_movement:
            status = db.query(StatusElement).filter(StatusElement.name == "CANCELED").first()

            if not status:
                raise Exception("No existe el estado Cancelado")

            db_movement.status = status
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(movement_id: str, movement: MovementBase, db: Session):
       
    db_movement = db.query(Movement).filter(Movement.id == movement_id).first()
    db_movement.updated_by = 'foo'
    
    if movement.quantity:
        db_movement.quantity=movement.quantity
    if movement.document_number:
        db_movement.document_number=movement.document_number
    if movement.measure_id:
        db_movement.measure_id = movement.measure_id
    
    if movement.source:
        db_movement.source = movement.source
    
    if movement.destiny:
        db_movement.destiny = movement.destiny

    if movement.product_id:
        db_movement.product_id = movement.product_id

    if movement.status_id:
        db_movement.status_id = movement.status_id
    
    try:
        db.add(db_movement)
        db.commit()
        db.refresh(db_movement)
        return db_movement
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible actualizar el movimiento")
