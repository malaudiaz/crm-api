# Routes contact.py

from fastapi import APIRouter, Depends, HTTPException
from ...schemas.partner.contact import ContactBase, ContactShema, PartnerContactBase, PartnerContactRelation
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List, Dict
from ...services.partner.contact import get_all, new, get_one, delete, update, \
    asociate_partner_contact, desasociate_partner_contact
from starlette import status
from ...auth_bearer import JWTBearer
import uuid

  
contact_route = APIRouter(
    tags=["Contactos"],
    # dependencies=[Depends(JWTBearer())]   
)

@contact_route.get("/contacts", response_model=Dict, summary="Obtener lista de Contactos")
def get_contacts(
    page: int = 1, 
    per_page: int = 6, 
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(page=page, per_page=per_page, criteria_key=criteria_key, criteria_value=criteria_value, db=db)

@contact_route.get("/contacts/{id}", response_model=ContactShema, summary="Obtener un Contacto por su ID")
def get_contact_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(contact_id=id, db=db)

@contact_route.post("/contacts", response_model=ContactShema, summary="Crear un Contacto")
def create_contact(contact: ContactBase, db: Session = Depends(get_db)):
    return new(contact=contact, db=db)

@contact_route.delete("/contacts/{id}", status_code=status.HTTP_200_OK, summary="Desactivar un Contacto por su ID")
def delete_contact(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(contact_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Contacto Desactivado")
    else:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")

@contact_route.put("/contacts/{id}", response_model=ContactShema, summary="Actualizar un Contacto por su ID")
def update_contact(id: uuid.UUID, contact: ContactBase, db: Session = Depends(get_db)):
    return update(db=db, contact_id=str(id), contact=contact)

@contact_route.post("/contacts/asociate", summary="Asociar un Contacto a un Cliente")
def asociate_at_partner(partnercontact: PartnerContactBase, db: Session = Depends(get_db)):
    return asociate_partner_contact(partnercontact=partnercontact, db=db)

@contact_route.post("/contacts/desasociate", summary="Desasociar un Contacto a un Cliente")
def desasociate_at_partner(partnercontactdelete: PartnerContactRelation, db: Session = Depends(get_db)):
    return desasociate_partner_contact(partnercontactdelete, db=db)
