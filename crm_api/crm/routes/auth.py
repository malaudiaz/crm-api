# auth.py

from fastapi import APIRouter, Depends, Request, Header
# from crm_api.crm.schemas.users.user import UserLogin
from ..schemas.users.user import UserLogin
# from services.auth import auth
from ..services.auth import auth
#, get_captcha, verify_captcha

from sqlalchemy.orm import Session
from crm.app import get_db
from starlette import status
from crm.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
from crm.functions_jwt import get_current_user

from crm.config.config import settings

auth_routes = APIRouter()

# @auth_routes.get('/captcha/show', tags=["Captcha"], summary='Mostrar un captcha al usuario')
# def captcha(request: Request):
#     return get_captcha(request)   

# @auth_routes.post('/captcha/verify', status_code=status.HTTP_200_OK, tags=["Captcha"], summary='Verificar el captcha del usuario')
# def captcha(request: Request, text: str):
#     is_captcha = verify_captcha(request=request, text=text)
#     if is_captcha:
#         raise HTTPException(status_code=200, detail="Captcha Correcto")
#     else:
#         raise HTTPException(status_code=403, detail="Captcha Incorrecto")    

@auth_routes.post("/login", status_code=status.HTTP_200_OK, tags=["Autentificación"], summary="Autentificación en la API")
def login(request:Request, user: UserLogin, db: Session = Depends(get_db)):
    return auth(request=request, db=db, user=user)

@auth_routes.get('/me', summary='Obtiene información del usuario autentificado', tags=["Autentificación"], dependencies=[Depends(JWTBearer())])
async def get_me(request:Request):
    user = get_current_user(request)       
    return JSONResponse(content=user, status_code=200)
