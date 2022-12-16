from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
#Base model tiene la capacidad de crear una entidad

router = APIRouter(tags=["users"])

# inciar: uvicorn users:app --reload 

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    age: int

users_list = [
         User(id=1, name="Brais", surname="Moure", email="bm@gmail.com", age=35),
         User(id=2, name="Brais", surname="Moure", email="bm@gmail.com", age=35),
         User(id=3, name="Brais", surname="Moure", email="bm@gmail.com", age=35)
        ]


@router.get("/usersjson")
async def usersjson():
    return [{"name":"Brais", "surname":"Moure", "email":"bm@gmail.com", "age":35 },
            {"name":"Chris", "surname":"Redfield", "email":"bm@gmail.com", "age":48 },
            {"name":"Jill", "surname":"Valentine", "email":"bm@gmail.com", "age":46 }
           ]

@router.get("/users")
async def users():
    return users_list

#Path
@router.get("/user/{id}") #parametro ingresado id
async def user(id: int):
    return search_user(id)

#Query
@router.get("/user/") #query ingresado id
async def user(id: int):
    return search_user(id)

#POST crear user
@router.post("/user/", status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
       raise HTTPException(status_code=404, detail="El usuario ya existe") #Debe responder con error 204 y detail
    
    users_list.append(user)
    return user

#PUT update user
@router.put("/user/")
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
@router.delete("/user/{id}")
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
