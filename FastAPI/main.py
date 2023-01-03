from fastapi import FastAPI #importar FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI() #se llama a la clase FastAPI y se guarda en variable app

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static") #example: http://127.0.0.1:8000/static/images/AlexisOnAHorseInSpace.jpg

@app.get("/") # "/": raiz del localhost
async def root():
    return "Hello FastAPI!"
#siempre que se llama al servidor la función debe ser asíncrona

@app.get("/url")
async def url():
    return { "url_curso":"https://mouredev.com/python" } #Retorna en formato JSON

# Si se ingresa una dirección invalida, se retorna un JSON not found y un error 404.