# options.py

from fastapi import HTTPException
from crm.models.options import Options
from sqlalchemy.orm import Session
from crm.schemas.options import OptionSchemaCreate
from sqlalchemy.exc import SQLAlchemyError

def get_main(db: Session):
    return db.query(Options).where(Options.parent == "").all()

def get_child(id: str, db: Session):
    return db.query(Options).where(Options.parent == id).all()

def new(db: Session, option: OptionSchemaCreate):
    db_option = db.query(Options).filter(Options.id == option.parent).first()
    
    if db_option is None:
        raise HTTPException(status_code=404, detail="El padre de esta opción no existe")                 
    
    db_option = Options(name=option.name, description=option.description, parent=option.parent)
    try:
        db.add(db_option)
        db.commit()
        db.refresh(db_option)
        return db_option
    except (Exception, SQLAlchemyError) as e:
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Repetido")

def get_one(id: str, db: Session):
    return db.query(Options).filter(Options.id == id).first()

def delete(id: str, db: Session):
    try:
        db_option = db.query(Options).filter(Options.id == id).first()
        db.delete(db_option)
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")

def update(id: str, option: OptionSchemaCreate, db: Session):
    db_option = db.query(Options).filter(Options.id == option.parent).first()
    
    if db_option is None:
        raise HTTPException(status_code=404, detail="El padre de esta opción no existe")                   
    
    db_option = db.query(Options).filter(Options.id == id).first()
    db_option.name = option.name
    db_option.descriptione = option.description
    db_option.parent = option.parent
    
    try:
        db.add(db_option)
        db.commit()
        db.refresh(db_option)
        return db_option
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Repetido")
