# auth.py
from fastapi import Request, HTTPException
from crm.models.business import Business
from crm.models.user import Users
from crm.models.skeleton import Skeleton
from jwt import encode
from crm.auth_bearer import decodeJWT
from datetime import datetime, timedelta
from passlib.context import CryptContext
# from fast_captcha import img_captcha
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from crm.schemas.user import UserLogin
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from crm.config.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def expire_date(minutes: int):
    expire = datetime.utcnow() + timedelta(minutes=minutes)
    return expire

def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(minutes=30)},
                   key="SECRET_KEY", algorithm="HS256")
    return token

def get_login_user(request: Request):
    token = request.headers['authorization'].split(' ')[1]
    user = decodeJWT(token)
    return user

# def get_captcha(request: Request):
#     img, text = img_captcha()    
#     request.session["captcha"] = text
#     return StreamingResponse(content=img, media_type='image/jpeg')

# def verify_captcha(request: Request, text: str):
#     captcha = str(request.session.get("captcha"))
#     return captcha.upper() == text.upper()

def auth(db: Session, user: UserLogin): 
    data = db.query(Users).filter(Users.username == user.username).first()
    if data is None:
        if user.username == settings.usr and user.password == settings.pasw:
            token_data = {"username": user.username}
            return JSONResponse(content={"token": write_token(data=token_data), "token_type": "Bearer"}, status_code=200)
        else:    
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if pwd_context.verify(user.password, data.password):
        db_user = db.query(
            Business.id, 
            Users
        ).filter(
            Business.id == Skeleton.business_id
        ).filter(
            Skeleton.id == Users.skeleton_id
        ).where(Users.username == user.username).first()  
        
        token_data = {"business_id": db_user.id, "username": db_user.Users.username, "user_id": db_user.Users.id, "skeleton_id": db_user.Users.skeleton_id}

        return JSONResponse(content={"token": write_token(data=token_data), "token_type": "Bearer"}, status_code=200)

        # raise HTTPException(status_code=200, detail={"token": write_token(data=token_data), "token_type": "Bearer"})
    else:
        raise HTTPException(status_code=404, detail="Contraseña incorrecta")
