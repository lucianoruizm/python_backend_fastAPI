Curso de backend con Python

Por: MoureDev
Repositorio de todos los cursos de Python:
https://github.com/mouredev/Hello-Python

Para ver todo el contenido visto en las clases, ingresar al repositorio de backend en Python:
https://github.com/mouredev/Hello-Python/tree/main/Backend

Framework utilizado: FastAPI
https://fastapi.tiangolo.com/

Instalación:
pip install fastapi
pip install "uvicorn[standard]" (local server)

o instalar todo

pip install fastapi[all]

Iniciar servidor:
uvicorn main:app --reload (donde main es el nombre del archivo python que se va a utilizar)
Ingresar URL obtenida, por ejemplo en un explorador para ver los resultados.

url + /docs = Se ingresa a Swagger UI
url + /redoc = Se ingresa a documentación generada de la API

jwt tokens:
https://jwt.io/
instalación: pip install "python-jose[cryptography]"
Librería del algoritmo de encriptación bcrypt: 
  pip install "passlib[bcrypt]"

bcrypt generator: https://bcrypt-generator.com/

mongoDB:
  https://www.mongodb.com/docs/manual/administration/install-community/
  Librería pymongo:
        pip install pymongo