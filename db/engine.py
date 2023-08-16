import os
from sqlalchemy import create_engine,text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from env.sql import SQLSettings

settings = SQLSettings()

username = settings.SQL_USER
password = settings.SQL_PASS
host = settings.SQL_HOST
port = settings.SQL_PORT
database = settings.SQL_DB


# create an engine that connects to the MySQL database
DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL)

# create a session factory to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=True)

# create a base class for SQLAlchemy models
Base = declarative_base()

def test_connection():
    try:
        session = SessionLocal()
        session.execute(text('SELECT 1'))
        print('Successfully connected to Database !')
    except Exception as e:
        print(f'Failed to connect to the database: {e}')
        os._exit(0)

test_connection()