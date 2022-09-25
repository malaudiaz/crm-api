# Routes options.py

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from crm.app import get_db
from crm.schemas.options import OptionSchema, OptionSchemaCreate
from crm.services.options import get_main, get_child, new, get_one, delete, update
from typing import List
from starlette import status
import uuid
# from crm.auth_bearer import JWTBearer
  
options_route = APIRouter(
    tags=["Opciones del Menu"],
    # dependencies=[Depends(JWTBearer())]   
)

@options_route.get("/menu", response_model=List[OptionSchema], summary="Obtener lista de opciones principales del menu")
def get_main_options(
    db: Session = Depends(get_db)
):
    return get_main(db=db)

@options_route.get("/submenu/{id}", response_model=List[OptionSchema], summary="Obtener lista de Opciones de un Menu")
def get_child_options(id: uuid.UUID, db: Session = Depends(get_db)):
    return get_child(id=str(id), db=db)

@options_route.post("/menu", response_model=OptionSchema, summary="Crear una Opción de Menu")
def create_option(option: OptionSchemaCreate, db: Session = Depends(get_db)):
    return new(option=option, db=db)

@options_route.get("/menu/{id}", response_model=OptionSchema, summary="Obtener una opción del menú por su ID")
def get_option_by_id(id: uuid.UUID, db: Session = Depends(get_db)):
    return get_one(id=str(id), db=db)

@options_route.delete("/menu/{id}", status_code=status.HTTP_200_OK, summary="Eliminar a opción de menú por su ID")
def delete_option(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Opción Eliminada")
    else:
        raise HTTPException(status_code=404, detail="Opción no encontrado")

@options_route.put("/menu/{id}", response_model=OptionSchema, summary="Actualizar una Opción del Menu por su ID")
def update_option(id: uuid.UUID, option: OptionSchemaCreate, db: Session = Depends(get_db)):
    return update(db=db, id=str(id), option=option)
