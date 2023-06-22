# Routes user.py

from fastapi import APIRouter, Depends, HTTPException, Request
from crm.schemas.users.user import UserShema, UserCreate, UserBase, ChagePasswordSchema
from crm.schemas.resources.result_object import ResultObject, ResultData
from sqlalchemy.orm import Session
from crm.app import get_db
from typing import List, Dict
from crm.services.users.users import get_all, new, get_one, delete, update, \
    get_all_user_sign_contracts, change_password
from starlette import status
from crm.auth_bearer import JWTBearer
# from crm.functions_action import action
import uuid
  
user_route = APIRouter(
    tags=["Usuarios"],
    dependencies=[Depends(JWTBearer())]   
)

@user_route.get("/users", response_model=ResultData, summary="Obtener lista de Usuarios")
def get_users(
    page: int = 1, 
    per_page: int = 6, 
    total: int = 0,
    total_pages: int = 0,
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(page=page, per_page=per_page, total=total, total_pages=total_pages, criteria_key=criteria_key, criteria_value=criteria_value, db=db)

@user_route.post("/users", response_model=ResultObject, summary="Crear un Usuario")
def create_user(request:Request, user: UserCreate, db: Session = Depends(get_db)):    
    return new(request=request, user=user, db=db)

@user_route.get("/users/{id}", response_model=ResultObject, summary="Obtener un Usuario por su ID")
def get_user_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(user_id=id, db=db)

@user_route.get("/users/contracts/", response_model=ResultObject, summary="Obtener Usuarios que firman contratos")
def get_users_sign_contracts(db: Session = Depends(get_db)):
    return get_all_user_sign_contracts(db=db)

@user_route.delete("/users/{id}", response_model=ResultObject, summary="Eliminar un Usuario por su ID")
def delete_user(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(user_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Usuario Eliminado")
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@user_route.put("/users/{id}", response_model=ResultObject, summary="Actualizar un Usuario por su ID")
def update_user(id: uuid.UUID, user: UserBase, db: Session = Depends(get_db)):
    return update(db=db, user_id=str(id), user=user)

@user_route.post("/users/password", response_model=ResultObject, summary="Cambiar passwoord a un Usuario")
def reset_password(
    request:Request,
    password: ChagePasswordSchema,
    db: Session = Depends(get_db)
):
    return change_password(
        request=request, db=db, password=password)
