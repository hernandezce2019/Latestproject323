
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from db.model.user import User
from db.schemas.user import get_user, get_users, UserResponse, UserCreate
from db.client import SessionLocal  # Assuming you set this up in client.py

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={status.HTTP_404_NOT_FOUND:{"message": "No Encontrado"}})

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{id}", response_model=UserResponse)
async def read_user(id: int, db: Session = Depends(get_db)):
    user = get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip, limit)
    return users

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user with this email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Create new user
    db_user = User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        address=user.address,
        date=user.date if user.date else None,  # Let DB use default if None
        password=user.password,
        role=user.role if user.role else "customer"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{id}", response_model=UserResponse)
async def update_user(id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields
    db_user.name = user.name
    db_user.surname = user.surname
    db_user.email = user.email
    db_user.address = user.address
    db_user.date = user.date
    db_user.password = user.password

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}




