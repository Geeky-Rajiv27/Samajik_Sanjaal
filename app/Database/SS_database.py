from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Replace USERNAME, PASSWORD, HOST, PORT, DATABASE with your MySQL info
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:rajiv123@localhost:3306/Samajik_Sanjaal"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
