# Routes business.py

from fastapi import APIRouter, Depends, HTTPException, Request
from crm.schemas.business import BusineSchema, BusineSchemaCreate
from starlette import status
from sqlalchemy.orm import Session
from crm.app import get_db
from typing import List
import uuid
from crm.auth_bearer import JWTBearer
from crm.services.business import get_all_business, create_new_business, \
    get_by_id, delete_by_id, update_business_by_id 

business_route = APIRouter(
    tags=["Negocios"],
    dependencies=[Depends(JWTBearer())]
)

@business_route.get("/business", response_model=List[BusineSchema], summary="Obtener Negocio del Usuario")
def get_all(
    request: Request,
    skip: int = 0, 
    limit: int = 100,     
    db: Session = Depends(get_db)
):
    business = get_all_business(request=request, skip=skip, limit=limit, db=db)
    return business

@business_route.post("/business", response_model=BusineSchema, summary="Crear un Negocio")
def create_business(request: Request, business: BusineSchemaCreate, db: Session = Depends(get_db)):
    return create_new_business(request=request, db=db, business=business)

@business_route.get("/business/{business_id}", response_model=BusineSchema, summary="Obtener un Negocio por su ID")
def get_one(business_id: uuid.UUID, db: Session = Depends(get_db)):
    db_business = get_by_id(db=db, business_id=str(business_id))
    if db_business is None:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    return db_business

@business_route.delete("/business/{business_id}", status_code=status.HTTP_200_OK, summary="Eliminar un Negocio por su ID")
def delete_business(business_id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete_by_id(business_id=str(business_id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Negocio Eliminado")
    else:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")

@business_route.put("/business/{business_id}", response_model=BusineSchema, summary="Actualizar un Negocio por su ID")
def update_business(business_id: uuid.UUID, business: BusineSchemaCreate, db: Session = Depends(get_db)):
    return update_business_by_id(db=db, business_id=str(business_id), business=business)
