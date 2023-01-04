from fastapi import APIRouter, Depends, HTTPException, Request
from crm.schemas.resources.status_elment import StatusBase, StatusShema
from sqlalchemy.orm import Session
from crm.app import get_db
from typing import List
from crm.services.resources.status_element import get_all, get_one_by_name, new, get_one, delete, update, get_all_for_contracts
from starlette import status
from crm.auth_bearer import JWTBearer
  
status_route = APIRouter(
    tags=["Estado Entidades"],
    # dependencies=[Depends(JWTBearer())]   
)

# @status_route.get("/resources/status", response_model=List[StatusShema], summary="Obtener lista de Estado de Entidades")
# def get_status(
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     return get_all(request=request, db=db)

@status_route.get("/resources/status/contract", response_model=List, summary="Obtener lista de Estado de los Contratos")
def get_status_contracts(
    request: Request,
    db: Session = Depends(get_db)
):
    return get_all_for_contracts(request=request, db=db)

# @status_route.post("/resources/status", response_model=StatusShema, summary="Crear una Estado de Entidad")
# def create_status(status: StatusBase, db: Session = Depends(get_db)):
#     return new(status=status, db=db)

# @status_route.get("/resources/status{id}", response_model=StatusShema, summary="Obtener un Estado por su ID")
# def get_status_by_id(id: str, db: Session = Depends(get_db)):
#     return get_one(status_id=id, db=db)

# @status_route.get("/resources/status/status{name}", response_model=StatusShema, summary="Obtener un Estado por su nombre")
# def get_status_by_name(name: str, db: Session = Depends(get_db)):
#     return get_one_by_name(name=name, db=db)

# @status_route.delete("/resources/status{id}", status_code=status.HTTP_200_OK, summary="Eliminar un estado por su ID")
# def delete_status(id: int, db: Session = Depends(get_db)):
#     is_delete = delete(status_id=int(id), db=db)
#     if is_delete:
#         raise HTTPException(status_code=200, detail="Estado Eliminada")
#     else:
#         raise HTTPException(status_code=404, detail="Estado no encontrada")

# @status_route.put("/resources/status{id}", response_model=StatusShema, summary="Actualizar un estado por su ID")
# def update_status(id: int, status: StatusBase, db: Session = Depends(get_db)):
#     return update(db=db, status_id=int(id), status=status)
