# users.py

from fastapi import HTTPException
from crm_api.crm.models.users.user import Users
from crm_api.crm.schemas.users.user import UserCreate, UserBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from crm.auth_bearer import decodeJWT
from typing import List
import math


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

def get_all(page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    
    str_where = "WHERE is_active=True " 
    str_count = "Select count(*) FROM enterprise.users "
    str_query = "Select id, username, fullname, dni, email, phone FROM enterprise.users "
    
    dict_query = {'username': " AND username ilike '%" + criteria_value + "%'",
                  'fullname': " AND fullname ilike '%" + criteria_value + "%'",
                  'dni': " AND dni ilike '%" + criteria_value + "%'"}
    
    str_where = str_where + dict_query[criteria_key] if criteria_value else ""  
    str_count += str_where 
    str_query += str_where
    
    total = db.execute(str_count).scalar()
    total_pages=total/per_page if (total % per_page == 0) else math.trunc(total / per_page) + 1
    
    str_query += " ORDER BY username LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
     
    lst_data = db.execute(str_query)
    data = []
    for item in lst_data:
        data.append({'id': item['id'], 'username' : item['username'], 'fullname': item['fullname'], 
                     'dni': item['dni'], 'email': item['email'], 'phone': item['phone'], 'selected': False})
    
    return {"page": page, "per_page": per_page, "total": total, "total_pages": total_pages, "data": data}

def get_all_old(page: int, per_page: int, username: str, fullname: str, dni: str, db: Session):  
    
    str_where = "WHERE is_active=True " 
    str_count = "Select count(*) FROM enterprise.users "
    str_query = "Select id, username, fullname, dni, email, phone FROM enterprise.users "
    
    if username:
        str_where += " AND username ilike '%" + username + "%'"
        
    if fullname:
        str_where += " AND fullname ilike '%" + fullname + "%'"
    
    if dni:
        str_where += " AND dni ilike '%" + dni + "%'"
        
    str_count += str_where
    str_query += str_where
    
    total = db.execute(str_count).scalar()
    total_pages=total/per_page if (total % per_page == 0) else math.trunc(total / per_page) + 1
    
    str_query += " LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
     
    lst_data = db.execute(str_query)
    data = []
    for item in lst_data:
        data.append({'id': item['id'], 'username' : item['username'], 'fullname': item['fullname'], 
                     'dni': item['dni'], 'email': item['email'], 'phone': item['phone'], 'selected': False})
    
    return {"page": page, "per_page": per_page, "total": total, "total_pages": total_pages, "data": data}
        
def new(db: Session, user: UserCreate):   
    pass_check = password_check(user.password, 8, 15)   
    if not pass_check['success']:
        raise HTTPException(status_code=404, detail="Error en los datos, " + pass_check['message'])             
    
    user.password = pwd_context.hash(user.password)  
    db_user = Users(username=user.username, fullname=user.fullname, dni=user.dni, job=user.job, email=user.email, phone=user.phone, password=user.password, selected=False)
        
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
    
def update(user_id: str, user: UserBase, db: Session):
       
    db_user = db.query(Users).filter(Users.id == user_id).first()
    db_user.username = user.username
    db_user.fullname = user.fullname
    db_user.dni = user.dni
    db_user.job = user.job
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
