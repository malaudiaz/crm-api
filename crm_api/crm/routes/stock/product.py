# Routes product.py

from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.stock.product import ProductBase, ProductSchema
from sqlalchemy.orm import Session
from ...app import get_db
from typing import List
from ...services.stock.product import get_all, new, get_one, delete, update
from starlette import status
from ...auth_bearer import JWTBearer
import uuid
  
product_route = APIRouter(
    tags=["Inventario"],
    # dependencies=[Depends(JWTBearer())]   
)

@product_route.get("/product", response_model=List[ProductSchema], summary="Obtener lista de Productos")
def get_products(
    request: Request,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return get_all(request=request, skip=skip, limit=limit, db=db)

@product_route.post("/product", response_model=ProductSchema, summary="Crear un Producto")
def create_product(product: ProductBase, db: Session = Depends(get_db)):
    return new(product=product, db=db)

@product_route.get("/product/{id}", response_model=ProductSchema, summary="Obtener un Producto por su ID")
def get_product_by_id(id: str, db: Session = Depends(get_db)):
    return get_one(product_id=id, db=db)

@product_route.delete("/product/{id}", status_code=status.HTTP_200_OK, summary="Desactivar un Producto por su ID")
def delete_product(id: uuid.UUID, db: Session = Depends(get_db)):
    is_delete = delete(product_id=str(id), db=db)
    if is_delete:
        raise HTTPException(status_code=200, detail="Producto Desactivado")
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

@product_route.put("/product/{id}", response_model=ProductSchema, summary="Actualizar un Producto por su ID")
def update_product(id: uuid.UUID, product: ProductSchema, db: Session = Depends(get_db)):
    return update(db=db, product_id=str(id), product=product)