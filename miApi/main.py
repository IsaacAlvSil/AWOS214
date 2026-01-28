#Importaciones
from fastapi import FastAPI
import asyncio

#instancia del servidor 
app = FastAPI()

#endpoints

@app.get("/")
async def bienvenida():
    return {"mensaje" : "¡Bienvenido a mi API!"}

@app.get("/HolaMundo")
async def hola():
    await asyncio.sleep(4)
    return {"mensaje" : "¡Hola mundo FastAPI!",
            "estatus":"200"
            }