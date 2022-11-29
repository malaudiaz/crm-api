# app.py

from sys import prefix
from fastapi import FastAPI
from crm.config.config import settings
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from logging.config import dictConfig
from crm.config.db import SessionLocal
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html)
from fastapi.staticfiles import StaticFiles

dictConfig(settings.log_config)

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=None, redoc_url=None
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(SessionMiddleware, secret_key=settings.secret)

from crm.routes.auth import auth_routes
from crm.routes.user import user_route
from crm.routes.options import options_route
from crm.routes.invoices.invoice import invoice_route
from crm.routes.resources.status import status_route
from crm.routes.partner.partner import partner_route
from crm.routes.partner.relationtype import relationtype_route
from crm.routes.partner.contact import contact_route
from crm.routes.stock.warehouse import warehouse_route
from crm.routes.stock.location import location_route
from crm.routes.stock.movement import movement_route
from crm.routes.stock.product import product_route
from crm.routes.contracts.contract import contract_route

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

app.include_router(auth_routes, prefix="/api")
app.include_router(user_route, prefix="/api")
app.include_router(options_route, prefix="/api")
app.include_router(invoice_route, prefix="/api")
app.include_router(status_route, prefix="/api")
app.include_router(partner_route, prefix="/api")
app.include_router(relationtype_route, prefix='/api')
app.include_router(contact_route, prefix="/api")
app.include_router(warehouse_route, prefix="/api/stock/warehouse")
app.include_router(location_route, prefix="/api/stock/location")
app.include_router(movement_route, prefix="/api/stock/movement")
app.include_router(product_route, prefix="/api/stock/product")
app.include_router(contract_route, prefix="/api")
