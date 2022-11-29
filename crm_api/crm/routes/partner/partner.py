# Routes partner.py

from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.partner.partner import PartnerBase, PartnerShema
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List, Dict
from ...services.partner.partners import get_all, new, get_one, delete, update, get_one_by_registration_number, get_by_name, \
    get_by_dni, get_by_nit
from starlette import status
from ...auth_bearer import JWTBearer
import uuid
  
partner_route = APIRouter(
    tags=["Clientes"],
    #dependencies=[Depends(JWTBearer())]   
)

@partner_route.get("/partners", response_model=Dict, summary="Obtener lista de Clientes")
def get_partners(
    totalCount: int = 0,
    skip: int = 0, 
    limit: int = 100, 
    name: str = '',
    db: Session = Depends(get_db)
):
    return get_all(totalCount=totalCount, skip=skip, limit=limit, db=db, name=name)

@partner_route.get("/partners/{id}", response_model=PartnerShema, summary="Obtener un Cliente por su ID")
def get_partner_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(partner_id=id, db=db)

@partner_route.get("/partners/registration_number/{registration_number}", response_model=PartnerShema, 
                   summary="Obtener un Cliente por su numero de registro")
def get_partner_by_registration_number(registration_number: str, db: Session = Depends(get_db)):
    return get_one_by_registration_number(registration_number=registration_number, db=db)

@partner_route.get("/partners/name/{name}", response_model=List[PartnerShema], summary="Obtener lista de Clientes por similitud de nombre")
def get_partners_by_name(
    request: Request,
    name: str = '',
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return get_by_name(name=name, request=request, skip=skip, limit=limit, db=db)

@partner_route.get("/partners/dni/{dni}", response_model=List[PartnerShema], summary="Obtener lista de Clientes por similitud de dni")
def get_partners_by_dni(
    request: Request,
    dni: str = '',
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return get_by_dni(dni=dni, request=request, skip=skip, limit=limit, db=db)

@partner_route.get("/partners/nit/{nit}", response_model=List[PartnerShema], summary="Obtener lista de Clientes por similitud de nit")
def get_partners_by_nit(
    request: Request,
    nit: str = '',
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return get_by_nit(nit=nit, request=request, skip=skip, limit=limit, db=db)

@partner_route.post("/partners", response_model=PartnerShema, summary="Crear un Cliente")
def create_partner(partner: PartnerBase, db: Session = Depends(get_db)):
    return new(partner=partner, db=db)

@partner_route.delete("/partners/{id}", status_code=status.HTTP_200_OK, summary="Desactivar un Cliente por su ID")
def delete_partner(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(partner_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Cliente Desactivado")
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

@partner_route.put("/partners/{id}", response_model=PartnerShema, summary="Actualizar un Cliente por su ID")
def update_partner(id: uuid.UUID, partner: PartnerBase, db: Session = Depends(get_db)):
    return update(db=db, partner_id=str(id), partner=partner)
