from unicodedata import name
from fastapi import HTTPException
from ...models.resources.status import StatusElement
from ...schemas.resources.status_elment import StatusBase, StatusShema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
# from crm.auth_bearer import decodeJWT
from ...auth_bearer import decodeJWT
from typing import List
from sqlalchemy import or_
            
def get_all(request: List[StatusShema], db: Session):  
    data = db.query(StatusElement).all() 
    return data
        
def get_all_for_contracts(request: List[StatusBase], db: Session): 
    data = db.query(StatusElement.name, StatusElement.description).filter(or_(StatusElement.name == v for v in ('DELIVERED', 'RECEIVED', 'APPROVED', 'CANCELLED'))).all()
    return data

def new(db: Session, status: StatusElement):
    
    db_status = StatusElement(name=status.name, description=status.description)
    
    try:
        db.add(db_status)
        db.commit()
        db.refresh(db_status)
        return db_status
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear el tipo de estado'               
        raise HTTPException(status_code=403, detail=msg)

def get_one(status_id: int, db: Session):  
    return db.query(StatusElement).filter(StatusElement.id == status_id).first()

def get_one_by_name(name: str, db: Session):  
    return db.query(StatusElement).filter(StatusElement.name == name).first()

def delete(status_id: int, db: Session):
    try:
        db_status = db.query(StatusElement).filter(StatusElement.id == status_id).first()
        db.delete(db_status)
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(status_id: str, status: StatusBase, db: Session):
       
    db_status = db.query(StatusElement).filter(StatusElement.id == status_id).first()
    
    db_status.name = status.name
    db_status.updated_by = 'foo'
    db_status.description=status.description
        
    try:
        db.add(db_status)
        db.commit()
        db.refresh(db_status)
        return db_status
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un estado con este Nombre")
        