"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 60

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])  # kept for future hashed passwords


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "chernandez": {
        "username": "chernandez",
        "full_name": "Cesar Hernandez",
        "email": "chernandez@gmail.com",
        "disabled": False,
        "password": "123456",
    },
    "chernandez1": {
        "username": "chernandez1",
        "full_name": "Cesar Hernandez 1",
        "email": "chernandez1@gmail.com",
        "disabled": False,
        "password": "654321",
    },
}


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_dict = users_db.get(form.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto"
        )

    user = search_user(form.username)

    # NOTE: passwords in `users_db` are plain for now; replace with hashed verification later
    if form.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contrasena no es correcta"
        )

    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }

    return {"access_token": user.username, "token_type": "bearer"}


def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
        """