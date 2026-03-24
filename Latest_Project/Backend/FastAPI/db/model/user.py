from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from db.client import Base

class User(Base):
    __tablename__ = 'users'  # Your SQL table name
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    address = Column(String(255), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    password = Column(String(255), nullable=False)  # Store hashed passwords in production
    role = Column(String(50), default="customer", nullable=False)  # admin or customer