from sqlalchemy.orm import Session
from db.model.user import User as UserModel
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    surname: str
    email: str
    address: str
    date: Optional[datetime] = None
    password: str
    role: Optional[str] = "customer"  # Default role is customer

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    address: str
    date: datetime
    password: Optional [str] = None
    role: Optional [str] = "customer"

    class Config:
        from_attributes = True

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).order_by(UserModel.id).offset(skip).limit(limit).all()