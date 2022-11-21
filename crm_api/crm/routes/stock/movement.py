# Routes movement.py

from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.stock.movement import MovementBase, MovementShema
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List
from ...services.stock.movements import get_all, new, get_one, delete, update
from starlette import status
from ...auth_bearer import JWTBearer
import uuid
  
movement_route = APIRouter(
    tags=["Inventario"],
    # dependencies=[Depends(JWTBearer())]   
)

@movement_route.get("/movement", response_model=List[MovementShema], summary="Obtener lista de movimientos")
def get_movements(
    request: Request,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return get_all(request=request, skip=skip, limit=limit, db=db)

@movement_route.post("/movement", response_model=MovementShema, summary="Crear un movimiento")
def create_movement(movement: MovementBase, db: Session = Depends(get_db)):
    return new(movement=movement, db=db)

@movement_route.get("/movement/{id}", response_model=MovementShema, summary="Obtener un movimiento por su ID")
def get_movement_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(movement_id=id, db=db)

@movement_route.delete("/movement/{id}", status_code=status.HTTP_200_OK, summary="Cancelar un movimiento por su ID")
def delete_movement(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(movement_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Movimiento Cancelado")
    else:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

@movement_route.put("/movement/{id}", response_model=MovementShema, summary="Actualizar un movimiento por su ID")
def update_movement(id: uuid.UUID, movement: MovementBase, db: Session = Depends(get_db)):
    return update(db=db, movement_id=str(id), movement=movement)
