# location.py

from unicodedata import name
from fastapi import HTTPException
from ...models.stock.measure import Measure
from ...schemas.stock.measure import MeasureBase, MeasureSchema
from crm.schemas.resources.result_object import ResultObject, ResultData
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from typing import List

def get_all(request: List[MeasureSchema], db: Session):  
    result = ResultObject() 
    result.data = []
    lst = db.query(Measure).all()                  
    for item in lst:
        result.data.append({'id': item.id, 'name' : item.name, 'description': item.description})
    # data = []
    # for item in lst:
    #     data.append(item.dict())
    return result
        
def new(db: Session, measure: MeasureBase):
    
    db_measure = Measure(name=measure.name, description=measure.description, created_by='foo', updated_by='foo')
        
    try:
        db.add(db_measure)
        db.commit()
        db.refresh(db_measure)
        return db_measure
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe una unidad de medida con ese nombre")
        else:
            msg = u'Ha ocurrido un error al crear la unidad de medida'               
            raise HTTPException(status_code=403, detail=msg)
    
def get_one(measure_id: str, db: Session):  
    measure = db.query(Measure).filter(Measure.id == measure_id).first()

    # data = {}
    # if location:
    #     data = location.dict()    
    return measure

def delete(measure_id: str, db: Session):
    try:
        db_measure = db.query(Measure).filter(Measure.id == measure_id).first()
        db_measure.is_active = False
        db_measure.updated_by = 'foo'
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(measure_id: str, measure: MeasureBase, db: Session):
       
    db_measure = db.query(Measure).filter(Measure.id == measure_id).first()
    db_measure.updated_by = 'foo'
    
    if measure.name:
        db_measure.name=measure.name
    if measure.description:
        db_measure.description=measure.description
    
    try:
        db.add(db_measure)
        db.commit()
        db.refresh(db_measure)
        return db_measure
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe una unidad de medida con ese nombre")
