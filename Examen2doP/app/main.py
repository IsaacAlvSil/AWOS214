from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional
from datetime import datetime

app = FastAPI(title="Sistema de tickets de soporte tecnico")

current_year = datetime.now().year

class ticket(BaseModel):
    newticket: str = Field(..., min_length=5, max_length=100)
    descripcion: str = Field(..., min_length=20, max_length=200)
    estado: Literal ["pendiente", "revisado"] = "pendiente"

class User(BaseModel):
    nombre_usuario: str
    correo: EmailStr

ticket_db: List[ticket] = [
    ticket(nombre="El gato negro", descripcion="falla de sistema", estado="pendiente"),
    ticket(nombre="El gato negro", descripcion="falla de sistema", estado="pendiente"),
    ticket(nombre="El gato negro", descripcion="falla de sistema", estado="pendiente"),
]


class Loan(BaseModel):
    ticket_name: str
    usuario: User


loans_db: List[Loan] = []

@app.post("/tickets/", status_code=status.HTTP_201_CREATED)
def registrar_ticket(ticket: ticket):
    for b in ticket_db:
        if b.nombre.lower() == ticket.nombre.lower():
            raise HTTPException(status_code=400, detail="El ticket ya existe o nombre no válido.")
    
    ticket_db.append(ticket)
    return {"mensaje": "Ticket registrado exitosamente", "ticket": ticket}

