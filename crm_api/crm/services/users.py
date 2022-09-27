# users.py

from fastapi import HTTPException, Request
from crm.models.user import Users
from crm.models.business import Business
from crm.models.skeleton import Skeleton
from crm.schemas.user import UserCreate, UserShema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from crm.auth_bearer import decodeJWT

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def password_check(passwd, min_len, max_len):
      
    RejectSym =['$', '@', '#', '%', '^']
    AcceptSym = ['!', '*', '.', '+', '-', '_', '?', ';', ':', '&', '=']
    
    RespObj = {"success": True, "message": "Contraseña correcta"}
      
    if len(passwd) < min_len:
        RespObj["success"] = False
        RespObj["message"] = "La contraseña no debe tener menos de " + str(min_len) + " carácteres"
          
    if len(passwd) > max_len:
        RespObj["success"] = False
        RespObj["message"] = "La contraseña no debe exceder los " + str(max_len) + " carácteres"
          
    if not any(char.isdigit() for char in passwd):
        RespObj["success"] = False
        RespObj["message"] = "La contraseña debe contar con al menos un Número"
          
    if not any(char.isupper() for char in passwd):
        RespObj["success"] = False
        RespObj["message"] = "La contraseña debe contar con al menos una Mayúscula"
          
    if not any(char.islower() for char in passwd):
        RespObj["success"] = False
        RespObj["message"] = "La contraseña debe contar con al menos una Minúscula"

    if not any(char in AcceptSym for char in passwd):
        RespObj["success"] = False
        RespObj["message"] = "La contraseña debe contener al menos un carácter especial"
        
    if any(char in RejectSym for char in passwd):
        RespObj["success"] = False
        RespObj["message"] = "La contraseña contiene carácteres no permitidos"

    return RespObj

def get_all(request: Request, skip: int, limit: int, db: Session):  
    user = decodeJWT(request.headers['authorization'].split(' ')[1]) 
    
    data = db.query(Users).offset(skip).limit(limit).all()    
  
    lst_users = []
    for row in data:
        user =row.Users
        lst_users.append(UserShema(id=user.id, username=user.username, fullname=user.fullname, dni=user.dni, email=user.email, phone=user.phone, skeleton_id=user.skeleton_id, password=user.password, is_active=user.is_active))    
              
    return lst_users
        
def new(db: Session, user: UserCreate):
    pass_check = password_check(user.password, 8, 15)   
    if not pass_check['success']:
        raise HTTPException(status_code=404, detail="Error en los datos, " + pass_check['message'])             
    
    user.password = pwd_context.hash(user.password)  
    db_user = Users(username=user.username, fullname=user.fullname, dni=user.dni, email=user.email, phone=user.phone, password=user.password)
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = 'Ha ocurrido un error al crear el usuario'
        if e.code == 'gkpj':
            field_name = str(e.__dict__['orig']).split('"')[1].split('_')[1]
            if field_name == 'username':
                msg = msg + ', el nombre de usuario ya existe'
            if field_name == 'dni':
                msg = msg + ', el dni ya existe'
        
        raise HTTPException(status_code=403, detail=msg)
    
def get_one(user_id: str, db: Session):  
    return db.query(Users).filter(Users.id == user_id).first()

def delete(user_id: str, db: Session):
    try:
        db_user = db.query(Users).filter(Users.id == user_id).first()
        db.delete(db_user)
        db.commit()
        return True
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    
def update(user_id: str, user: UserCreate, db: Session):
       
    db_user = db.query(Users).filter(Users.id == user_id).first()
    db_user.username = user.username
    db_user.fullname = user.fullname
    db_user.dni = user.dni
    db_user.email = user.email
    db_user.phone = user.phone

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail="Ya existe un usuario con este Nombre")
