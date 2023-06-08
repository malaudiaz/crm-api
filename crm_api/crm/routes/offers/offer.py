# Routes offer.py

from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.offers.offer import OfferBase, OfferSchema
from ...schemas.resources.result_object import ResultObject
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List, Dict, Any
from ...services.offers.offer import get_all, new, get_one, delete, update
from starlette import status
from ...auth_bearer import JWTBearer
import uuid
  
offer_route = APIRouter(
    tags=["Ofertas"],
    dependencies=[Depends(JWTBearer())]
)

@offer_route.get("/offers", response_model=ResultObject, summary="Obtener lista de Ofertas")
def get_offers(
    page: int = 1, 
    per_page: int = 6, 
    total: int = 0,
    total_pages: int = 25,
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(page=page, per_page=per_page, total=total, total_pages=total_pages, 
    criteria_key=criteria_key, criteria_value=criteria_value, db=db)
    
@offer_route.get("/offers/{id}", response_model=ResultObject, summary="Obtener una oferta por su ID")
def get_offer_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(offer_id=id, db=db)

@offer_route.post("/offer", response_model=ResultObject, summary="Crear una Oferta")
def create_offer(request:Request, offer: OfferBase, db: Session = Depends(get_db)):
    return new(request=request, offer=offer, db=db)

@offer_route.delete("/offer/{id}", response_model=ResultObject, summary="Desactivar una oferta por su ID")
def delete_offer(request:Request, id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(request=request, offer_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Oferta Desactivada")
    else:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")

@offer_route.put("/offer/{id}", response_model=ResultObject, summary="Actualizar una Oferta por su ID")
def update_offer(request:Request, id: str, offer: OfferBase, db: Session = Depends(get_db)):
    return update(request=request, offer_id=id, offer=offer, db=db)
