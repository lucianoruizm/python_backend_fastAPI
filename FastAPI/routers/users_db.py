# USERS DB API

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())

#Path
@router.get("/{id}") #parametro ingresado id
async def user(id: str):
    return search_user("_id", ObjectId(id))

#Query
@router.get("/") #query ingresado id
async def user(id: str):
    return search_user("_id", ObjectId(id))

#POST crear user
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
       raise HTTPException(status_code=404, detail="El usuario ya existe") #Debe responder con error 204 y detail

    user_dict = dict(user)
    del user_dict["id"] # Se elimina porque Mongodb por defecto genera un id, creado como _id

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id":id})) # Pasandolo a la operacion user_schema retorna un objeto que coincide exactamente con lo que se desea retornar que es un objeto de tipo user 

    return User(**new_user)

#PUT update user
@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.local.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error":"No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id))

#DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error":"No se ha eliminado el usuario"}


def search_user(field: str, key):
    try:
        user = (db_client.local.users.find_one({field: key}))
        return User(**user_schema(user))
    except:
        return {"error":"No se ha encontrado el usuario"}