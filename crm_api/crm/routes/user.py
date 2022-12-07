# Routes user.py

from fastapi import APIRouter, Depends, HTTPException, Request
from crm.schemas.user import UserShema, UserCreate, UserBase
from sqlalchemy.orm import Session
from crm.app import get_db
from typing import List, Dict
from crm.services.users import get_all, new, get_one, delete, update
from starlette import status
from crm.auth_bearer import JWTBearer
import uuid
  
user_route = APIRouter(
    tags=["Usuarios"],
    # dependencies=[Depends(JWTBearer())]   
)

@user_route.get("/users", response_model=Dict, summary="Obtener lista de Usuarios")
def get_users(
    page: int = 1, 
    per_page: int = 6, 
    username: str = "",
    fullname: str = "",
    dni: str = "",
    db: Session = Depends(get_db)
):
    return get_all(page=page, per_page=per_page, username=username, fullname=fullname, dni=dni, db=db)

@user_route.post("/users", response_model=UserShema, summary="Crear un Usuario")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return new(user=user, db=db)

@user_route.get("/users/{id}", response_model=UserShema, summary="Obtener un Usuario por su ID")
def get_user_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(user_id=id, db=db)

@user_route.delete("/users/{id}", status_code=status.HTTP_200_OK, summary="Eliminar un Usuario por su ID")
def delete_user(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(user_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Usuario Eliminado")
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@user_route.put("/users/{id}", response_model=UserShema, summary="Actualizar un Usuario por su ID")
def update_user(id: uuid.UUID, user: UserBase, db: Session = Depends(get_db)):
    return update(db=db, user_id=str(id), user=user)
