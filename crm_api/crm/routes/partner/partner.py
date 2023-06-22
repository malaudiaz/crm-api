# Routes partner.py

from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.partner.partner import PartnerBase, PartnerShema
from ...schemas.resources.result_object import ResultObject, ResultData
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List, Dict, Any
from ...services.partner.partners import get_all, new, get_one_partner, delete, update
from starlette import status
from ...auth_bearer import JWTBearer
import uuid
  
partner_route = APIRouter(
    tags=["Clientes"],
    dependencies=[Depends(JWTBearer())]
)

@partner_route.get("/partners", response_model=ResultData, summary="Obtener lista de Clientes")
def get_partners(
    page: int = 1, 
    per_page: int = 6, 
    total: int = 0,
    total_pages: int = 0,
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(page=page, per_page=per_page, total=total, total_pages=total_pages, criteria_key=criteria_key, criteria_value=criteria_value, db=db)
    
@partner_route.get("/partners/{id}", response_model=ResultData, summary="Obtener un Cliente por su ID")
def get_partner_by_id(id: str, db: Session = Depends(get_db)):
    return get_one_partner(partner_id=id, db=db)

@partner_route.post("/partners", response_model=ResultData, summary="Crear un Cliente")
def create_partner(request:Request, partner: PartnerBase, db: Session = Depends(get_db)):
    return new(request=request, partner=partner, db=db)

@partner_route.delete("/partners/{id}", response_model=ResultData, summary="Desactivar un Cliente por su ID")
def delete_partner(request:Request, id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(request=request, partner_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Cliente Desactivado")
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

@partner_route.put("/partners/{id}", response_model=ResultData, summary="Actualizar un Cliente por su ID")
def update_partner(request:Request, id: str, partner: PartnerBase, db: Session = Depends(get_db)):
    return update(request=request, partner_id=id, partner=partner, db=db)
