from fastapi import APIRouter, HTTPException
from db.models.user import User
from db.client import db_client

router = APIRouter(tags=["users"])

users_list = []

@router.get("/usersdb")
async def users():
    return users_list

#Path
@router.get("/userdb/{id}") #parametro ingresado id
async def user(id: int):
    return search_user(id)

#Query
@router.get("/userdb/") #query ingresado id
async def user(id: int):
    return search_user(id)

#POST crear user
@router.post("/userdb/", status_code=201)
async def user(user: User):
    # if type(search_user(user.id)) == User:
    #    raise HTTPException(status_code=404, detail="El usuario ya existe") #Debe responder con error 204 y detail

    db_client.local.users.insert_one(user)

    return user

#PUT update user
@router.put("/userdb/")
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
@router.delete("/userdb/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error":"No se ha eliminado el usuario"}


#Función encargada de buscar id del usuario
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
