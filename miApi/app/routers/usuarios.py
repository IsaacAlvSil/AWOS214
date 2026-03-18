from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import usuario_create
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

router = APIRouter(
    prefix="/v1/usuarios", tags=["CRUD HTTP"]
    )

#enpoints de usuarios 
@router.get("/")
async def leer_usuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "usuarios":usuarios
    }

@router.post("/",status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:usuario_create):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario.model_dump())

    return{
        "mensaje":"Usuario agregado",
        "Usuario":usuario
    }

@router.put("/{id_buscado}", status_code=status.HTTP_202_ACCEPTED)
async def actualizar_usuario(id_buscado: int, datos_nuevos: dict):
    for usr in usuarios:
        if usr["id"] == id_buscado:
            usr.update(datos_nuevos)
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usr
            }
        
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )  

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, userAuth: str = Depends(verificar_Peticion)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return{
                "message": f"usuario eliminado correctamente por: {userAuth}" 
            }
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )