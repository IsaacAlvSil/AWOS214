from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter

router = APIRouter( tags= ['Varios'])


@router.get("/")
async def bienvenida():
    return {"mensaje" : "¡Bienvenido a mi API!"}


@router.get("/HolaMundo")
async def hola():
    await asyncio.sleep(4)
    return {"mensaje" : "¡Hola mundo FastAPI! ",
            "estatus": "200"
            }