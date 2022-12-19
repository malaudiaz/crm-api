from jwt import encode, decode
from jwt import exceptions
from datetime import datetime, timedelta
from os import getenv
from fastapi.responses import JSONResponse

def expire_date(minutes: int):
    expire = datetime.utcnow() + timedelta(minutes=minutes)
    return expire

def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(minutes=30)}, key="SECRET_KEY", algorithm="HS256")
    return token
  
def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key="SECRET_KEY", algorithms=["HS256"])
        decode(token, key="SECRET_KEY", algorithms=["HS256"])
    except exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid Token"}, status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expired"}, status_code=401)
    
def get_current_user(request):
    token = request.headers["authorization"].split(" ")[1]
    return decode(token, key="SECRET_KEY", algorithms=["HS256"])