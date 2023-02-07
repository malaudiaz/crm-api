# auth_bearer.py

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from crm.config.config import settings
from jwt import decode
import time


def decodeJWT(token: str) -> dict:
    try:       
        decoded_token = decode(jwt=token, key=settings.secret, algorithms=[settings.algorithm])
        return decoded_token if decoded_token["exp"] >= time.time() else None    
    except Exception as e: 
        return {}
       
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):  
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)        
                                
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=401, detail="Esquema de Autentificación erróneo")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=402, detail="Token erróneo ó caducado")
                         
            return credentials.credentials
        else:
            raise HTTPException(status_code=404, detail="Código de autorización erróneo")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
            
        if payload:
            isTokenValid = True

        return isTokenValid
