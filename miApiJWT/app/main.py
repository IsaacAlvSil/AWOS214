#Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError  
from datetime import datetime, timedelta, timezone

#instancia del servidor 
app = FastAPI(
    title="Mi API",
    description="Isaac Silva",
    version="1.0.0"
)

#BD ficticia
usuarios = [
    {"id": 1, "nombre":"Juan", "edad" :21 },
    {"id": 2, "nombre":"Isra", "edad" :23 },
    {"id": 3, "nombre":"Abdiel", "edad" :21 },
    {"id": 4, "nombre":"Jafet", "edad" :24 },
    {"id": 5, "nombre":"Roger", "edad" :19 },
]

#modelo de validacion pydantic
class usuario_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, examples=["Isaac"])
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 - 123")


#Seguridad JWT y OAuth2 
SECRET_KEY = "Mi_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales no válidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    return username


#Endpoint login
@app.post("/login", tags=["Seguridad"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "isaac" or form_data.password != "123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


#Endpoints
@app.get("/", tags=["Inicio"])
async def bienvenida():
    return {"mensaje" : "¡Bienvenido a mi API!"}

@app.get("/HolaMundo" ,tags=["Bienvenida Asincrona"])
async def hola():
    await asyncio.sleep(4)
    return {
        "mensaje" : "¡Hola FastAPI! ",
        "estatus": "200"
    }

@app.get("/v1/parametroOp/{id}", tags=["Parametro obligatorio"])
async def consultaUno(id:int):
    return {"Se encontro usuario" : id}

@app.get("/v1/parametroOp/", tags=["Parametro opcional"])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje:":"usuario encontrado", "usuario":usuario}
        return{"mensaje:":"usuario no encontrado", "usuario":id}
    else:
        return{"mensaje:":"No se proporciono id"}

@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def leer_usuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "usuarios":usuarios
    }

@app.post("/v1/usuarios/",tags=["CRUD HTTP"],status_code=status.HTTP_201_CREATED)
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

@app.put("/v1/usuarios/{id_buscado}", tags=["CRUD HTTP"])
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

#Usamos el get_current_user
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, current_user: str = Depends(get_current_user)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return{
                "message": f"usuario eliminado correctamente por: {current_user}" 
            }
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )