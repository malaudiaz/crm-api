from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.contracts.contracts import ContractBase, ContractShema
from ...schemas.resources.result_object import ResultObject, ResultData
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List, Dict
from ...services.contrats.contract import get_all, new, get_one_contract, delete, update
from starlette import status
from ...auth_bearer import JWTBearer
import uuid
  
contract_route = APIRouter(
    tags=["Contratos"],
    dependencies=[Depends(JWTBearer())]   
)

@contract_route.get("/contracts", response_model=ResultData, summary="Obtener lista de Contratos")
def get_contracts(
    page: int = 1, 
    per_page: int = 6, 
    total: int = 0,
    total_pages: int = 0,
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(page=page, per_page=per_page, total=total, total_pages=total_pages, criteria_key=criteria_key, criteria_value=criteria_value, db=db)

@contract_route.get("/contracts/{id}", response_model=ResultData, summary="Obtener un Contrato por su ID")
def get_contract_by_id(id: str, db: Session = Depends(get_db)):
    return get_one_contract(contract_id=id, db=db)

@contract_route.post("/contracts", response_model=ResultData, summary="Crear un Contrato")
def create_contract(request:Request, contract: ContractBase, db: Session = Depends(get_db)):
    return new(request=request, contract=contract, db=db)

@contract_route.delete("/contracts/{id}", response_model=ResultData, summary="Desactivar un Contrato por su ID")
def delete_contract(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(contract_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Contrato Desactivado")
    else:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")

@contract_route.put("/contracts/{id}", response_model=ResultData, summary="Actualizar un Contrato por su ID")
def update_contract(id: uuid.UUID, contract: ContractBase, db: Session = Depends(get_db)):
    return update(db=db, contract_id=str(id), contract=contract)
