from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQL Server connection string using pyodbc
DATABASE_URL = (
    "mssql+pyodbc://sa:Welcome2024!@DESKTOP-KCE16AP\\MSSQLSERVER1/GruasCR"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()