# Routes localtion.py

from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.stock.location import LocationBase, LocationSchema, UpdateLocation, LocationWarehouseSchema
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List
from ...services.stock.location import get_all, new, get_one, delete, update
from starlette import status
from ...auth_bearer import JWTBearer
import uuid
  
location_route = APIRouter(
    tags=["Inventario"],
    # dependencies=[Depends(JWTBearer())]   
)

@location_route.get("/locations", response_model=List[LocationSchema], summary="Obtener lista de Localidades")
def get_locations(
    request: Request,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return get_all(request=request, skip=skip, limit=limit, db=db)

@location_route.post("/location", response_model=LocationWarehouseSchema, summary="Crear una localidad")
def create_location(location: LocationBase, db: Session = Depends(get_db)):
    return new(location=location, db=db)

@location_route.get("/location/{id}", response_model=LocationSchema, summary="Obtener una Localidad por su ID")
def get_location_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(location_id=id, db=db)

@location_route.delete("/location/{id}", status_code=status.HTTP_200_OK, summary="Desactivar una localidad por su ID")
def delete_location(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(location_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Localidad Desactivada")
    else:
        raise HTTPException(status_code=404, detail="Localidad no encontrada")

@location_route.put("/location/{id}", response_model=LocationSchema, summary="Actualizar una localidad por su ID")
def update_location(id: uuid.UUID, location: UpdateLocation, db: Session = Depends(get_db)):
    return update(db=db, location_id=str(id), location=location)
