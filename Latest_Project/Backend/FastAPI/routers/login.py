from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.model.user import User
from db.client import SessionLocal
import bcrypt

router = APIRouter(prefix="/auth",
                   tags=["auth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No Encontrado"}})


class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    redirect: str
    message: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/debug/users")
async def debug_all_users(db: Session = Depends(get_db)):
    """DEBUG: Show all users in database"""
    try:
        users = db.query(User).all()
        result = []
        for u in users:
            result.append({
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "password": u.password
            })
        return {"count": len(result), "users": result}
    except Exception as e:
        return {"error": str(e)}

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint using email and password from database
    Returns redirect URL based on user role
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        print(f"DEBUG: User not found with email: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User not found with email: {credentials.email}"
        )
    
    # Verify password (simple comparison for now, use bcrypt for hashing)
    print(f"DEBUG: Checking password. Input: {credentials.password}, DB: {user.password}")
    if user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    # Determine role, ensure it's a string to satisfy response model
    role_value = user.role if user.role is not None else "customer"

    # Determine redirect URL based on role
    if role_value == "admin":
        redirect = "admin_home.html"
    else:
        redirect = "customer_home.html"

    print(f"DEBUG: Login successful for {credentials.email} with role {role_value}")
    return LoginResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=role_value,
        redirect=redirect,
        message="Login successful"
    )