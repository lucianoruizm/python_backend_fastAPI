import os
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 #Esto hará que el token tenga una duración de 1 min

load_dotenv()
SECRET = os.getenv('SECRET')

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

#Representación de db
users_db = {
    "jillvalentine": {
        "username": "jillvalentine",
        "full_name": "Jill Valentine",
        "email": "jillv@stars.com",
        "disabled": False,        #Al estar activo tiene la autorización de acceder a los datos del usuario
        "password": "$2a$12$E3WG7GMS3.QsF9Ja1vmL8e7nLy8v7S6ChahfCF2FuvwVqOh1Jbe8q" #Generado con bcrypt
    },
    "chrisredfield": {
        "username": "chrisredfield",
        "full_name": "Chris Redfield",
        "email": "chrisred@stars.com",
        "disabled": True,            #Al estar inactivo no tiene la autorización de acceder a los datos del usuario
        "password": " $2a$12$7f5ZszJDYfg/EPD0NDYY7eAPg01AOYlbkodOsbIOnZooWXqVLO/pO" #Generado con bcrypt
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if username is None:
           raise exception
        
    except JWTError:
        raise exception
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password): #Verifica que el password sea el mismo que coincide con el token que se genera
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
        # Para volver a generar el token se debe hacer login
    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)): #esta operación depende de que el user este autenticado, según la función pasada
    return user