# Routes partner.py

from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.partner.partner import PartnerBase, PartnerShema
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List, Dict, Any
from ...services.partner.partners import get_all, new, get_one, delete, update, get_one_by_registration_number
from starlette import status
from ...auth_bearer import JWTBearer
import uuid
  
partner_route = APIRouter(
    tags=["Clientes"],
    dependencies=[Depends(JWTBearer())]
)

@partner_route.get("/partners", response_model=Dict, summary="Obtener lista de Clientes")
def get_partners(
    page: int = 1, 
    per_page: int = 6, 
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(page=page, per_page=per_page, criteria_key=criteria_key, criteria_value=criteria_value, db=db)
    
@partner_route.get("/partners/{id}", response_model=PartnerShema, summary="Obtener un Cliente por su ID")
def get_partner_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(partner_id=id, db=db)

@partner_route.get("/partners/registration_number/{registration_number}", response_model=PartnerShema, 
                   summary="Obtener un Cliente por su numero de registro")
def get_partner_by_registration_number(registration_number: str, db: Session = Depends(get_db)):
    return get_one_by_registration_number(registration_number=registration_number, db=db)

# @partner_route.post("/partners", response_model=PartnerShema, summary="Crear un Cliente")
@partner_route.post("/partners", summary="Crear un Cliente")
def create_partner(request:Request, partner: PartnerBase, db: Session = Depends(get_db)):
    return new(request=request, partner=partner, db=db)

# @partner_route.post("/partners", summary="Crear un Cliente")
# def create_partner(partner: Dict[Any, Any], db: Session = Depends(get_db)):
#     print(partner)
#     return True
#     return new(partner=partner, db=db)

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
