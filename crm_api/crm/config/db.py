# db.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings
# from crm.config.config import settings

 
SQLALCHEMY_DATABASE_URL = settings.database_uri
# SQLALCHEMY_DATABASE_URL = "postgresql://admin:pgsql09@localhost:5432/crm" 


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()
