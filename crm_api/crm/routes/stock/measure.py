# Routes localtion.py

from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.stock.measure import MeasureBase, MeasureSchema
from crm.schemas.resources.result_object import ResultObject, ResultData
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List
from ...services.stock.measure import get_all, new, get_one, delete, update
from starlette import status
from ...auth_bearer import JWTBearer
import uuid
  
measure_route = APIRouter(
    tags=["Inventario"],
    # dependencies=[Depends(JWTBearer())]   
)

@measure_route.get("/measures", response_model=ResultObject, summary="Obtener lista de Unidades de Medidas")
def get_measure(
    request: Request,
    db: Session = Depends(get_db)
):
    return get_all(request=request, db=db)

@measure_route.post("/measure", response_model=MeasureSchema, summary="Crear una Unidad de Medida")
def create_measure(measure: MeasureBase, db: Session = Depends(get_db)):
    return new(measure=measure, db=db)

@measure_route.get("/measure/{id}", response_model=MeasureSchema, summary="Obtener una unidad de medida por su ID")
def get_measure_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(measure_id=id, db=db)

@measure_route.delete("/measure/{id}", status_code=status.HTTP_200_OK, summary="Desactivar una unidad de medida por su ID")
def delete_measure(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(measure_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Unidad de Medida Desactivada")
    else:
        raise HTTPException(status_code=404, detail="Unidad de Medida no encontrada")

@measure_route.put("/measure/{id}", response_model=MeasureSchema, summary="Actualizar una unidad de medida por su ID")
def update_measure(id: uuid.UUID, measure: MeasureBase, db: Session = Depends(get_db)):
    return update(db=db, measure_id=str(id), measure=measure)
