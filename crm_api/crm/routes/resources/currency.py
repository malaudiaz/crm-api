from fastapi import APIRouter, Depends, HTTPException, Request
from crm.schemas.resources.currency import CurrencyBase, CurrencyShema
from sqlalchemy.orm import Session
from crm.app import get_db
from typing import List
from crm.services.resources.currency import get_all, new
from starlette import status
from crm.auth_bearer import JWTBearer
  
currency_route = APIRouter(
    tags=["Monedas"],
    # dependencies=[Depends(JWTBearer())]   
)

@currency_route.get("/resources/currency", response_model=List[CurrencyBase], summary="Obtener lista de Monedas")
def get_currency(
    request: Request,
    db: Session = Depends(get_db)
):
    return get_all(request=request, db=db)

@currency_route.post("/resources/currency", response_model=CurrencyShema, summary="Crear una Moneda")
def create_currency(currency: CurrencyBase, db: Session = Depends(get_db)):
    return new(currency=currency, db=db)


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
