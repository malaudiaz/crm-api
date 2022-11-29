from unicodedata import name
from fastapi import HTTPException
from ...models.partner.relationtype import RelationType
from ...schemas.partner.relationtype import RelationTypeBase, RelationTypeShema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from ...auth_bearer import decodeJWT
from typing import List
            
def get_all(request: List[RelationTypeShema], skip: int, limit: int, db: Session):  
    data = db.query(RelationType).offset(skip).limit(limit).all()                  
    return data
        
def new(db: Session, relationtype: RelationType):
    
    db_relation = RelationType(name=relationtype.name, description=relationtype.description)
    
    try:
        db.add(db_relation)
        db.commit()
        db.refresh(db_relation)
        return db_relation
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear el tipo de estado'               
        raise HTTPException(status_code=403, detail=msg)
    
def get_one(relationtype_id: int, db: Session):  
    return db.query(RelationType).filter(RelationType.id == relationtype_id).first()

def get_one_by_name(name: str, db: Session):  
    return db.query(RelationType).filter(RelationType.name == name).first()

def delete(relationtype_id: int, db: Session):
    try:
        db_relation = db.query(RelationType).filter(RelationType.id == relationtype_id).first()
        db.delete(db_relation)
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(relationtype_id: str, relationtype: RelationTypeBase, db: Session):
       
    db_relation = db.query(RelationType).filter(RelationType.id == relationtype_id).first()
    
    db_relation.name = relationtype.name
    db_relation.updated_by = 'foo'
    db_relation.description=relationtype.description
        
    try:
        db.add(db_relation)
        db.commit()
        db.refresh(db_relation)
        return db_relation
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un estado con este Nombre")
        