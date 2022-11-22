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
    
    db_movement = Movement(quantity=movement.quantity, measurement=movement.measurement, 
                           document_number=movement.document_number, status_id=movement.status_id,
                           source=movement.source, destiny=movement.destiny, product_id=movement.product_id,
                           created_by='foo', updated_by='foo', )
    # buscar el producto para asociarlo al movimiento

    # product = db.query(Product).filter(Product.id == movement.product_id).first() 

    # if not product:
    #     raise Exception("Error en el movimiento, no existe producto")
    
    # db_movement.product = product
    
    # buscar el status para asociarlo al movimiento
    status = db.query(StatusElement).filter(StatusElement.id == int(movement.status_id)).first()
    
    # raise Exception(status_element)
    if not status:
        raise Exception("No existe estado para el movimiento")

    # db_movement.status = status
    # buscando localidades de origen y destino
    # location_source = db.query(Location).filter(Location.id == movement.source).first()
    # location_destiny = db.query(Location).filter(Location.id == movement.destiny).first()

    # if not location_source:
    #     raise Exception("No existe localización de origen")

    # if not location_destiny:
    #     raise Exception("No existe localización destino")

    # db_movement.location_source = location_source    
    # db_movement.location_destiny = location_destiny       
    
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
    if movement.measurement:
        db_movement.measurement = movement.measurement
    
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
