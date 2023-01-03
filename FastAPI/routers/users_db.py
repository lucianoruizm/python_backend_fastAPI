# USERS DB API

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema
from db.client import db_client

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

users_list = []

@router.get("/")
async def users():
    return users_list

#Path
@router.get("/{id}") #parametro ingresado id
async def user(id: int):
    return search_user(id)

#Query
@router.get("/") #query ingresado id
async def user(id: int):
    return search_user(id)

#POST crear user
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user_by_email(user.email)) == User:
       raise HTTPException(status_code=404, detail="El usuario ya existe") #Debe responder con error 204 y detail

    user_dict = dict(user)
    del user_dict["id"] # Se elimina porque Mongodb por defecto genera un id, creado como _id

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id":id})) # Pasandolo a la operacion user_schema retorna un objeto que coincide exactamente con lo que se desea retornar que es un objeto de tipo user 

    return User(**new_user)

#PUT update user
@router.put("/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"error":"No se ha actualizado el usuario"}
    
    return user

#DELETE
@router.delete("/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error":"No se ha eliminado el usuario"}


#Función encargada de buscar id del usuario
def search_user_by_email(email: str):
    try:
        user = (db_client.local.user.find_one({"email": email}))
        return User(user_schema(**user))
    except:
        return {"error":"No se ha encontrado el usuario"}
