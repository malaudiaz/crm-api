from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.invoices.invoice import InvoiceBase, InvoiceImports, InvoiceShema
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List
from ...services.invoices.invoices import get_all, new, get_one, update_real_imports, update, delete
from starlette import status
from ...auth_bearer import JWTBearer
import uuid
  
invoice_route = APIRouter(
    tags=["Facturas"],
    dependencies=[Depends(JWTBearer())]   
)

@invoice_route.get("/invoices", response_model=List[InvoiceShema], summary="Obtener lista de Facturas")
def get_invoices(
    request: Request,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return get_all(request=request, skip=skip, limit=limit, db=db)

@invoice_route.post("/invoices", response_model=InvoiceShema, summary="Crear una Factura")
def create_invoice(invoice: InvoiceBase, db: Session = Depends(get_db)):
    return new(invoice=invoice, db=db)

@invoice_route.get("/invoices/{id}", response_model=InvoiceShema, summary="Obtener una Factura por su ID")
def get_invoice_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(invoice_id=id, db=db)

@invoice_route.delete("/invoices/{id}", status_code=status.HTTP_200_OK, summary="Eliminar una Factura por su ID")
def delete_invoice(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(invoice_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Factura Eliminada")
    else:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

@invoice_route.put("/invoices/{id}", response_model=InvoiceShema, summary="Actualizar una Factura por su ID")
def update_invoice(id: uuid.UUID, invoice: InvoiceBase, db: Session = Depends(get_db)):
    return update(db=db, invoice_id=str(id), invoice=invoice)

@invoice_route.put("/invoices/importes/{invoice_number}", response_model=InvoiceShema, summary="Actualizar importes de una Factura por su invoice_number")
def update_imports(invoice_number: str, invoice: InvoiceImports, db: Session = Depends(get_db)):
    return update_real_imports(db=db, invoice_number=str(invoice_number), invoice=invoice)