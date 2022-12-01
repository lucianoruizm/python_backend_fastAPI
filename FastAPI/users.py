from fastapi import FastAPI
from pydantic import BaseModel
#Base model tiene la capacidad de crear una entidad

app = FastAPI()

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


@app.get("/usersjson")
async def usersjson():
    return [{"name":"Brais", "surname":"Moure", "email":"bm@gmail.com", "age":35 },
            {"name":"Chris", "surname":"Redfield", "email":"bm@gmail.com", "age":48 },
            {"name":"Jill", "surname":"Valentine", "email":"bm@gmail.com", "age":46 }
           ]

@app.get("/users")
async def users():
    return users_list

#Path
@app.get("/user/{id}") #parametro ingresado id
async def user(id: int):
    return search_user(id)

#Query
@app.get("/user/") #query ingresado id
async def user(id: int):
    return search_user(id)

#Función encargada de buscar id del usuario
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}