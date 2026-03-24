from fastapi import FastAPI, Depends , HTTPException, APIRouter, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.client import SessionLocal
from db.model.user import User as UserModel
from db.schemas.user import UserResponse

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(prefix="/login",
                   tags=["login"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No Encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
  username: str
  full_name: str
  email: str
  disabled: bool

class UserDB(User):
  password: str


def search_user(db: Session, username: str):
  # For this implementation, we'll use email as username
  user = db.query(UserModel).filter(UserModel.email == username).first()
  if user:
    return UserDB(
      username=user.email,
      full_name=f"{user.name} {user.surname}",
      email=user.email,
      disabled=False,  # You can add a disabled field to your User model if needed
      password=user.password
    ), user  # return both Pydantic and SQL object for role lookup
  return None, None
  
async def current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
  user = search_user(db, token)
  if not user:
    raise HTTPException(status_code=400, detail= "El usuario no es correcto")
  
  if user.disabled:
    raise HTTPException(status_code=400, detail= "El usuario esta inactivo")
  
  return user
  
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  user_info, user_obj = search_user(db, form.username)
  if not user_info:
    raise HTTPException(status_code=400, detail= "El usuario no es correcto")
  
  if not form.password == user_info.password:
    raise HTTPException(status_code=400, detail= "La contrasena no es correcta")
  
  # determine redirect based on role in user_obj
  redirect = "/customer_home.html"
  if user_obj and user_obj.role == "admin":
    redirect = "/admin_home.html"
  
  return {"access_token": user_info.username, "token_type": "bearer", "role": user_obj.role if user_obj else "customer", "redirect": redirect}

"""
En este post muesta como usa el ouath form que envia la informacion y el depends, 
signifca la dependencia de todo el sistema de informacion, una vez autenticado, el usuario va a estar 
autorizado o no
el return roken es la manera en la cual la aplicacion va saber que el usuario esta autenticado, 
"""

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
  return user

