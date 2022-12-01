from fastapi import FastAPI #importar FastAPI

app = FastAPI() #se llama a la clase FastAPI y se guarda en variable app

@app.get("/") # "/": raiz del localhost
async def root():
    return "Hello FastAPI!"
#siempre que se llama al servidor la función debe ser asíncrona

@app.get("/url")
async def url():
    return { "url_curso":"https://mouredev.com/python" } #Retorna en formato JSON

# Si se ingresa una dirección invalida, se retorna un JSON not found y un error 404.