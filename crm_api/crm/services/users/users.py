# users.py

from fastapi import HTTPException
from crm.models.users.user import Users
from crm.schemas.users.user import UserCreate, UserBase, ChagePasswordSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from crm.functions_jwt import get_current_user
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
    str_query = "Select id, username, fullname, dni, email, job, phone, password FROM enterprise.users "
    
    dict_query = {'username': " AND username ilike '%" + criteria_value + "%'",
                  'fullname': " AND fullname ilike '%" + criteria_value + "%'",
                  'id': " AND id = '" + criteria_value + "' ",
                  'dni': " AND dni ilike '%" + criteria_value + "%'"}
    
    if criteria_key and criteria_key not in dict_query:
        raise HTTPException(status_code=404, detail="Parametro no válido")
    
    str_where = str_where + dict_query[criteria_key] if criteria_value else ""  
    str_count += str_where 
    str_query += str_where
    
    total = db.execute(str_count).scalar()
    total_pages=total/per_page if (total % per_page == 0) else math.trunc(total / per_page) + 1
    
    str_query += " ORDER BY username LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
     
    lst_data = db.execute(str_query)
    data = []
    for item in lst_data:
        data.append({'id': item['id'], 'username' : item['username'], 'fullname': item['fullname'], 'dni': item['dni'], 
            'email': item['email'], 'job': item['job'], 'phone': item['phone'], 'password': item['password'], 'selected': False})
    
    return {"page": page, "per_page": per_page, "total": total, "total_pages": total_pages, "data": data}

def new(request, db: Session, user: UserCreate):  
    # Para obtener el usuario logueado descomentar estas dos líneas. 
    # currentUser = get_current_user(request)      
    # print(currentUser)

    pass_check = password_check(user.password, 8, 15)   
    if not pass_check['success']:
        raise HTTPException(status_code=404, detail="Error en los datos, " + pass_check['message'])             
    
    user.password = pwd_context.hash(user.password)  
    db_user = Users(username=user.username, fullname=user.fullname, dni=user.dni, job=user.job, 
                    email=user.email, phone=user.phone, password=user.password, selected=False)
        
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

def get_one_by_username(username: str, db: Session):  
    return db.query(Users).filter(Users.username == username, Users.is_active == True).first()

def get_all_user_sign_contracts(db: Session):  
    data = []
    lst_data = db.query(Users).filter(Users.sign_contracts == True).all()
    for item in lst_data:
        data.append({'id': item.id, 'username' : item.username, 'fullname': item.fullname})
    return data

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

def change_password(request, db: Session, password: ChagePasswordSchema):  
    
    # if el user_name viene vacio cojo el usario logueado
    if not password.username:
        currentUser = get_current_user(request)
        username = currentUser['username'] 
    else:
        username = password.username
    
    # verificar que existe ese usuario con ese password
    one_user = get_one_by_username(username=username, db=db)
    if not one_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if pwd_context.verify(password.current_password, one_user.password):
        
        # verificar que las contrasenas nuevas son iguales
        if str(password.new_password) != str(password.renew_password):
            raise HTTPException(status_code=404, detail="La contraseña nueva y la confirmación no coinciden")
        
        #verificando que tenga la estructura correcta
        pass_check = password_check(password.new_password, 8, 15)   
        if not pass_check['success']:
            raise HTTPException(status_code=404, detail="Error en el nuevo password, " + pass_check['message']) 
        
        #cambiando el paswword al usuario
        one_user.password = pwd_context.hash(password.new_password)
        
        try:
            db.add(one_user)
            db.commit()
            db.refresh(one_user)
            return True
        except (Exception, SQLAlchemyError) as e:
            print(e.code)
            if e.code == "gkpj":
                raise HTTPException(status_code=400, detail="Error cambiando password en BD")
        
    else:
        raise HTTPException(status_code=405, detail="Contraseña incorrecta")

