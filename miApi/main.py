#Importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

#instancia del servidor 
app = FastAPI(
    title="Mi primer API",
    description="Isaac Silva",
    version="1.0.0"
    )
#BD ficticia
usuarios=[
    {"id": 1, "nombre":"Juan", "edad" :21 },
    {"id": 2, "nombre":"Isra", "edad" :23 },
    {"id": 3, "nombre":"Abdiel", "edad" :21 },
    {"id": 4, "nombre":"Jafet", "edad" :24 },
    {"id": 5, "nombre":"Roger", "edad" :19 },
]

#endpoints

@app.get("/", tags=["Inicio"])
async def bienvenida():
    return {"mensaje" : "¡Bienvenido a mi API!"}

@app.get("/HolaMundo" ,tags=["Bienvenida Asincrona"])
async def hola():
    await asyncio.sleep(4)
    return {"mensaje" : "¡Hola mundo FastAPI! ",
            "estatus": "200"
            }

@app.get("/v1/usuario/{id}", tags=["Parametro obligatorio"])
async def consultaUno(id:int):
    return {"Se encontro usuario" : id}


@app.get("/v1/usuarios/", tags=["Parametro opcional"])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje:":"usuario encontrado", "usuario":usuario}
        return{"mensaje:":"usuario no encontrado", "usuario":id}
    else:
        return{"mensaje:":"No se proporciono id"}