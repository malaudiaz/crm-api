# Routes contact.py

from fastapi import APIRouter, Depends, HTTPException
from ...schemas.partner.contact import ContactBase, ContactShema, PartnerContactBase, PartnerContactRelation
from ...schemas.resources.result_object import ResultObject, ResultData
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List, Dict
from ...services.partner.contact import get_all, new, get_one_contact, delete, update, \
    asociate_partner_contact, desasociate_partner_contact, get_contacts_by_partner
from starlette import status
from ...auth_bearer import JWTBearer
import uuid

  
contact_route = APIRouter(
    tags=["Contactos"],
    dependencies=[Depends(JWTBearer())]   
)

@contact_route.get("/contacts", response_model=ResultData, summary="Obtener lista de Contactos")
def get_contacts(
    page: int = 1, 
    per_page: int = 6, 
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(page=page, per_page=per_page, criteria_key=criteria_key, criteria_value=criteria_value, db=db)

@contact_route.get("/contacts/{id}", response_model=ResultData, summary="Obtener un Contacto por su ID")
def get_contact_by_id(id: str, db: Session = Depends(get_db)):
    return get_one_contact(contact_id=id, db=db)

@contact_route.get("/contacts/partner/{partner_id}", response_model=ResultData, summary="Obtener listado de Contactos de un Cliente")
def get_contacts(
    page: int = 1, 
    per_page: int = 6, 
    partner_id: str = "", 
    db: Session = Depends(get_db)
):
    return get_contacts_by_partner(page=page, per_page=per_page, partner_id=partner_id, db=db)

@contact_route.post("/contacts", response_model=ResultData, summary="Crear un Contacto")
def create_contact(contact: ContactBase, db: Session = Depends(get_db)):
    return new(contact=contact, db=db)

@contact_route.delete("/contacts/{id}", response_model=ResultData, summary="Desactivar un Contacto por su ID")
def delete_contact(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(contact_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Contacto Desactivado")
    else:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")

@contact_route.put("/contacts/{id}", response_model=ResultData, summary="Actualizar un Contacto por su ID")
def update_contact(id: uuid.UUID, contact: ContactBase, db: Session = Depends(get_db)):
    return update(db=db, contact_id=str(id), contact=contact)
