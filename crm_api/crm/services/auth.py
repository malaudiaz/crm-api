# auth.py
from fastapi import HTTPException, Header, Request
# from crm_api.crm.models.users.user import Users
# from ..models.users.user import  Users
from ..models.users.user import Users
from passlib.context import CryptContext
# from fast_captcha import img_captcha
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
# from crm_api.crm.schemas.users.user import UserLogin
from ..schemas.users.user import UserLogin
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from crm.functions_jwt import write_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def get_captcha(request: Request):
#     img, text = img_captcha()    
#     request.session["captcha"] = text
#     return StreamingResponse(content=img, media_type='image/jpeg')

# def verify_captcha(request: Request, text: str):
#     captcha = str(request.session.get("captcha"))
#     return captcha.upper() == text.upper()

def auth(request: Request, db: Session, user: UserLogin): 
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    data = db.query(Users).filter(Users.username == user.username).first()
    if data is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if pwd_context.verify(user.password, data.password):
        db_user = db.query(Users).where(Users.username == user.username).first()  
                
        token_data = {"username": data.username, "user_id": data.id}

        return JSONResponse(content={"token": write_token(data=token_data), "token_type": "Bearer", "fullname": db_user.fullname, "job": db_user.job, "user_id": db_user.id}, status_code=200)

    else:
        raise HTTPException(status_code=405, detail="Contraseña incorrecta")
