# business.py

from fastapi import HTTPException, Request
from crm.models.business import Business
from crm.schemas.business import BusineSchemaCreate
from crm.config.config import settings
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from crm.auth_bearer import decodeJWT

def get_all_business(request: Request, skip: int, limit: int, db: Session):
    user = decodeJWT(request.headers['authorization'].split(' ')[1]) 
    if user["username"] == settings.usr:
        return db.query(Business).offset(skip).limit(limit).all()
    else:
        raise HTTPException(status_code=404, detail="No tienes permiso para esta opción") 

def create_new_business(request: Request, db: Session, business: BusineSchemaCreate):
    user = decodeJWT(request.headers['authorization'].split(' ')[1]) 
    if user["username"] == settings.usr:
        try:
            db_business = db.query(Business).filter(Business.id == user['business_id']).first()
        except NoResultFound:
            db_business = Business(name=business.name, description=business.description)
            try:
                db.add(db_business)
                db.commit()
                db.refresh(db_business)
                return db_business
            except (Exception, SQLAlchemyError) as e:
                if e.code == "gkpj":
                    raise HTTPException(status_code=400, detail="Ya existe un negocio con este Nombre")
        else:
            raise HTTPException(status_code=404, detail="El usuario ya tiene un Negocio")
    else:
        raise HTTPException(status_code=404, detail="No tienes permiso para esta opción") 

def get_by_id(db: Session, business_id: str):
    return db.query(Business).filter(Business.id == business_id).first()
    
def delete_by_id(db: Session, business_id: str):
    try:
        db_business = db.query(Business).filter(Business.id == business_id).first()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    else:
        try:
            db.delete(db_business)
            db.commit()
            return True
        except (Exception, SQLAlchemyError) as e:
            print(e)
            raise HTTPException(status_code=404, detail="No es posible eliminar")

def update_business_by_id(db: Session, business_id: str, business: BusineSchemaCreate):
    try:
        db_business = db.query(Business).filter(Business.id == business_id).first()
    
        if db_business is None:
            raise HTTPException(status_code=404, detail="Negocio no encontrado")
        
        db_business.name = business.name
        db_business.description = business.description
        db.add(db_business)
        db.commit()
        db.refresh(db_business)
        return db_business
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un negocio con este Nombre")
    