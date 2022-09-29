# Routes user.py

from fastapi import APIRouter, Depends, HTTPException, Request
from crm.schemas.partner.partner import PartnerBase, PartnerShema
from sqlalchemy.orm import Session
from crm.app import get_db
from typing import List
from crm.services.partner.partners import get_all, new, get_one, delete, update
from starlette import status
from crm.auth_bearer import JWTBearer
import uuid
  
partner_route = APIRouter(
    tags=["Clientes"],
    dependencies=[Depends(JWTBearer())]   
)

@partner_route.get("/partners", response_model=List[PartnerShema], summary="Obtener lista de Clientes")
def get_partners(
    request: Request,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return get_all(request=request, skip=skip, limit=limit, db=db)

@partner_route.post("/partners", response_model=PartnerShema, summary="Crear un Cliente")
def create_partner(partner: PartnerBase, db: Session = Depends(get_db)):
    return new(partner=partner, db=db)

@partner_route.get("/partners/{id}", response_model=PartnerShema, summary="Obtener un Cliente por su ID")
def get_partner_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(partner_id=id, db=db)

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
