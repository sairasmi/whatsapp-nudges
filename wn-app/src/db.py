import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.pool import QueuePool
from config import settings
import urllib.parse
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


from databases import Database

# DATABASE_URL = "mysql+pymysql://root:@localhost/whatsapp_nudge?charset=utf8mb4"
db_password = urllib.parse.quote(settings.DB_Pass)
DATABASE_URL = f'{settings.DB_Dialect}+pymysql://{settings.DB_User}:{db_password}@{settings.DB_Host}:{settings.DB_Port}/{settings.DB_Name}'
os.environ['DATABASE_URL'] = DATABASE_URL          # This env is needed for alembic to run migrations

engine = create_engine(DATABASE_URL, echo_pool=True)
logging.info(engine)

metadata = MetaData()

# databases query builder
database = Database(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

metadata.create_all(engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
