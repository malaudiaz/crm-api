# skeleton.py

from fastapi import HTTPException, Request
from crm.models.business import Business
from crm.models.skeleton import Skeleton
from crm.schemas.skeleton import SkeletonSchemaCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, IntegrityError
from crm.auth_bearer import decodeJWT

def get_all_skeleton(request: Request, skip: int, limit: int, db: Session):
    user = decodeJWT(request.headers['authorization'].split(' ')[1]) 
    return db.query(Skeleton).where(Skeleton.business_id == user['business_id']).offset(skip).limit(limit).all()

def create_new_skeleton(request: Request, db: Session, skeleton: SkeletonSchemaCreate):
    user = decodeJWT(request.headers['authorization'].split(' ')[1]) 
    
    if skeleton.business_id != user["business_id"]:
        skeleton.business_id = user["business_id"]

    business = db.query(Business).filter(Business.id == user['business_id']).first()
    
    if business is None:
        raise HTTPException(status_code=404, detail="Error en los datos, el Negocio no existe")             
    
    if skeleton.parent != "":   
        db_skeleton = db.query(Skeleton).filter(Skeleton.id == str(skeleton.parent)).first()
        if db_skeleton is None:
            raise HTTPException(status_code=404, detail="Error en los datos, el Departamento Padre no existe")             
    
    db_skeleton = Skeleton(name=skeleton.name, description=skeleton.description, parent=str(skeleton.parent), business_id=user['business_id'])
    try:
        db.add(db_skeleton)
        db.commit()
        db.refresh(db_skeleton)
        return db_skeleton
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        raise HTTPException(status_code=400, detail="Existen errores en sus datos")

def get_by_id(request: Request, db: Session, skeleton_id: str):
    user = decodeJWT(request.headers['authorization'].split(' ')[1]) 
    return db.query(Skeleton).filter(Skeleton.business_id == user['business_id'] and Skeleton.id == skeleton_id).first()

def delete_by_id(request: Request, db: Session, skeleton_id: str):   
    user = decodeJWT(request.headers['authorization'].split(' ')[1]) 
    db_skeleton = db.query(Skeleton).filter(Skeleton.business_id == user['business_id'] and Skeleton.id == skeleton_id).first()
    
    if db_skeleton is not None:
        raise HTTPException(status_code=403, detail="Imposible Eliminar, Existen departamentos hijos asociados a éste departamento.")      

    try:
        db_skeleton = db.query(Skeleton).filter(Skeleton.id == skeleton_id).first()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    else:
        try:
            db.delete(db_skeleton)
            db.commit()
            return True
        except (Exception, SQLAlchemyError) as e:
            print(e)
            raise HTTPException(status_code=404, detail="No es posible eliminar")

def update_by_id(request: Request, db: Session, skeleton_id: str, skeleton: SkeletonSchemaCreate):
    user = decodeJWT(request.headers['authorization'].split(' ')[1]) 
    skeleton.business_id = user["business_id"]

    business = db.query(Business).filter(Business.id == user["business_id"]).first()
    
    if business is None:
        raise HTTPException(status_code=404, detail="Error en los datos, el Negocio no existe")             
    
    db_skeleton = db.query(Skeleton).filter(Skeleton.id == str(skeleton.parent)).first()
    
    if db_skeleton is None:
        raise HTTPException(status_code=404, detail="Error en los datos, el Departamento Padre no existe")             

    try:
        db_skeleton = db.query(Skeleton).filter(Skeleton.id == skeleton_id).first()
    
        if db_skeleton is None:
            raise HTTPException(status_code=404, detail="Departamento no encontrado")
        
        db_skeleton.name = skeleton.name
        db_skeleton.description = skeleton.description
        db_skeleton.parent = skeleton.parent
        db_skeleton.business_id = skeleton.business_id
        
        db.add(db_skeleton)
        db.commit()
        db.refresh(db_skeleton)
        return db_skeleton
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un negocio con este Nombre")
    