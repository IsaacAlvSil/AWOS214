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
    title="API sistema de tickets",
    description="Isaac Silva",
    version="1.0.0"
)

#BD ficticia
tickets = [
    {"id": 1, "descripcion":"falla tecnica", "estado" :"pendiente" },
    {"id": 2, "descripcion":"adeudo", "estado" :"pendiente" },
    {"id": 3, "descripcion":"sin señal", "estado" :"pendiente" },
    {"id": 4, "descripcion":"sin actualizaciones", "estado" :"pendiente" },
    {"id": 5, "descripcion":"adeuso", "estado" :"pendiente" },
]

#modelo de validacion pydantic
class ticket_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de ticket")
    descripcion: str = Field(..., min_length=3, max_length=50, examples=["falla"])
    estado: str = Field(..., min_length=3, max_length=50, examples=["pendiente"])


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
    if form_data.username != "soporte" or form_data.password != "4321":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


#Endpoints
@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def leer_tickets():
    return{
        "status":"200",
        "total": len(tickets),
        "tickets":tickets
    }

@app.post("/v1/tickets/",tags=["CRUD HTTP"],status_code=status.HTTP_201_CREATED)
async def crear_ticket(ticket:ticket_create):
    for usr in tickets:
        if usr["id"] == ticket.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    tickets.append(ticket.model_dump())

    return{
        "mensaje":"Ticket agregado",
        "ticket":ticket
    }

@app.put("/v1/tickets/{id_buscado}", tags=["CRUD HTTP"])
async def actualizar_ticket(id_buscado: int, datos_nuevos: dict):
    for usr in tickets:
        if usr["id"] == id_buscado:
            usr.update(datos_nuevos)
            return {
                "mensaje": "Ticket actualizado",
                "ticket": usr
            }
        
    raise HTTPException(
        status_code=404,
        detail="Ticket no encontrado"
    )  

#Usamos el get_current_user
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_ticket(id:int, current_user: str = Depends(get_current_user)):
    for ticket in tickets:
        if ticket["id"] == id:
            tickets.remove(ticket)
            return{
                "message": f"ticket eliminado correctamente por: {current_user}" 
            }
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )