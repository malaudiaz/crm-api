from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.partner.relationtype import RelationTypeBase, RelationTypeShema
from sqlalchemy.orm import Session
from crm.app import get_db
from typing import List
from ...services.partner.relationtype import get_all, get_one_by_name, new, get_one, delete, update
from starlette import status
from crm.auth_bearer import JWTBearer
  
relationtype_route = APIRouter(
    tags=["Tipo Relacion Cliente Contacto"],
    # dependencies=[Depends(JWTBearer())]   
)

# @relationtype_route.get("/relationtype/relation", response_model=List[RelationTypeShema], summary="Obtener Tipo de Realcion Cliente Contacto")
# def get_relationtype(
#     request: Request,
#     skip: int = 0, 
#     limit: int = 100, 
#     db: Session = Depends(get_db)
# ):
#     return get_all(request=request, skip=skip, limit=limit, db=db)

# @relationtype_route.post("/relationtype/relationtype", response_model=RelationTypeShema, summary="Crear una tipo de Relación Cliente Contacto")
# def create_relationtype(relationtype: RelationTypeBase, db: Session = Depends(get_db)):
#     return new(relationtype=relationtype, db=db)

# @relationtype_route.get("/relationtype/relationtype{id}", response_model=RelationTypeShema, summary="Obtener un Tipo de Relación por su ID")
# def get_relationtype_by_id(id: str, db: Session = Depends(get_db)):
#     return get_one(relationtype_id=id, db=db)

# @relationtype_route.get("/relationtype/relation/relationtype{name}", response_model=RelationTypeShema, summary="Obtener un Tipo de Relacion por su nombre")
# def get_relationtype_by_name(name: str, db: Session = Depends(get_db)):
#     return get_one_by_name(name=name, db=db)

# @relationtype_route.delete("/relationtype/relationtype{id}", status_code=status.HTTP_200_OK, summary="Eliminar un Tipo de Relacion por su ID")
# def delete_relationtype(id: int, db: Session = Depends(get_db)):
#     is_delete = delete(relationtype_id=int(id), db=db)
#     if is_delete:
#         raise HTTPException(status_code=200, detail="Tipo de Relacion Eliminado")
#     else:
#         raise HTTPException(status_code=404, detail="Tipo de Relacion no encontrado")

# @relationtype_route.put("/relationtype/relationtype{id}", response_model=RelationTypeShema, summary="Actualizar un tipo de relacion por su ID")
# def update_relationtype(id: int, relationtype: RelationTypeBase, db: Session = Depends(get_db)):
#     return update(db=db, srelationtype_id=int(id), relationtype=relationtype)
