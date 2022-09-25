# Routes business.py

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from sqlalchemy.orm import Session
from crm.app import get_db
from crm.schemas.skeleton import SkeletonSchema, SkeletonSchemaCreate
from crm.services.skeleton import get_all_skeleton, create_new_skeleton, get_by_id, delete_by_id, update_by_id
from crm.auth_bearer import JWTBearer
from typing import List
import uuid

skeleton_route = APIRouter(
    tags=["Estructura del Negocio"],
    dependencies=[Depends(JWTBearer())]   
)

@skeleton_route.get("/skeleton", response_model=List[SkeletonSchema], summary="Obtener lista de Estructura del Negocio")
def get_all(
    request: Request,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    skeleton = get_all_skeleton(request=request, skip=skip, limit=limit, db=db)
    return skeleton

@skeleton_route.post("/skeleton", response_model=SkeletonSchema, summary="Crear un departamento en la estructura del Negocio")
def create_skeleton(request: Request, skeleton: SkeletonSchemaCreate, db: Session = Depends(get_db)):
    return create_new_skeleton(request=request, db=db, skeleton=skeleton)

@skeleton_route.get("/skeleton/{skeleton_id}", response_model=SkeletonSchema, summary="Obtener un Departamento")
def get_one(request: Request, skeleton_id: uuid.UUID, db: Session = Depends(get_db)):
    skeleton = get_by_id(request=request, db=db, skeleton_id=str(skeleton_id))
    if skeleton is None:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    return skeleton

@skeleton_route.delete("/skeleton/{skeleton_id}", status_code=status.HTTP_200_OK, summary="Eliminar un Departamento")
def delete_business(request: Request, skeleton_id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete_by_id(request=request, skeleton_id=str(skeleton_id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Departamento Eliminado")
    else:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")

@skeleton_route.put("/skeleton/{skeleton_id}", response_model=SkeletonSchema, summary="Modificar un departamento por su ID")
def update_business(request: Request, skeleton_id: uuid.UUID, skeleton: SkeletonSchemaCreate, db: Session = Depends(get_db)):
    return update_by_id(request=request, db=db, skeleton_id=str(skeleton_id), skeleton=skeleton)
