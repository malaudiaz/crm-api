# Routes user.py

from fastapi import APIRouter, Depends, HTTPException, Request
from crm.schemas.stock.warehouse import WarehouseBase, WarehouseSchema, UpdateWarehouse
from sqlalchemy.orm import Session
from crm.app import get_db
from typing import List
from crm.services.stock.warehouse import get_all, new, get_one, delete, update
from starlette import status
from crm.auth_bearer import JWTBearer
import uuid
  
warehouse_route = APIRouter(
    tags=["Inventario"],
    # dependencies=[Depends(JWTBearer())]   
)

@warehouse_route.get("/warehouses", response_model=List[WarehouseSchema], summary="Obtener lista de Almacenes")
def get_warehouses(
    request: Request,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return get_all(request=request, skip=skip, limit=limit, db=db)

@warehouse_route.post("/warehouse", response_model=WarehouseSchema, summary="Crear un Almacen")
def create_warehouse(warehouse: WarehouseBase, db: Session = Depends(get_db)):
    return new(warehouse=warehouse, db=db)

@warehouse_route.get("/warehouse/{id}", response_model=WarehouseSchema, summary="Obtener un Almacén por su ID")
def get_warehouse_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(warehouse_id=id, db=db)

@warehouse_route.delete("/warehouse/{id}", status_code=status.HTTP_200_OK, summary="Desactivar un Almancen por su ID")
def delete_warehouse(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(warehouse_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Almacén Desactivado")
    else:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")

@warehouse_route.put("/warehouse/{id}", response_model=WarehouseSchema, summary="Actualizar un Almacén por su ID")
def update_warehouse(id: uuid.UUID, warehouse: UpdateWarehouse, db: Session = Depends(get_db)):
    return update(db=db, warehouse_id=str(id), warehouse=warehouse)
