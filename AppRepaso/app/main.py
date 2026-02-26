from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional
from datetime import datetime

app = FastAPI(title="Biblioteca Digital API")

# --- 1. MODELOS PYDANTIC --- 
current_year = datetime.now().year

class Book(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    anio: int = Field(..., gt=1450, le=current_year)
    paginas: int = Field(..., gt=1)
    estado: Literal["disponible", "prestado"] = "disponible"

class User(BaseModel):
    # Usuario debe tener nombre y correo válido
    nombre: str
    correo: EmailStr

class Loan(BaseModel):
    nombre_libro: str
    usuario: User

books_db: List[Book] = [
    Book(nombre="El gato negro", anio=1843, paginas=1056, estado="disponible"),
    Book(nombre="El cuervo", anio=1967, paginas=417, estado="disponible"),
    Book(nombre="El durmiente", anio=1831, paginas=328, estado="disponible")
]
loans_db: List[Loan] = []
# --- 2. ENDPOINTS
@app.post("/libros/", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Book):
    for b in books_db:
        if b.nombre.lower() == libro.nombre.lower():
            raise HTTPException(status_code=400, detail="El libro ya existe o nombre no válido.")
    
    books_db.append(libro)
    return {"mensaje": "Libro registrado exitosamente", "libro": libro}

# b. Listar todos los libros disponibles
@app.get("/libros/disponibles", response_model=List[Book])
def libros_disponibles():
    disponibles = [b for b in books_db if b.estado == "disponible"]
    return disponibles

# c. Buscar un libro por su nombre
@app.get("/libros/{nombre}")
def buscar_libro(nombre: str):
    for b in books_db:
        if b.nombre.lower() == nombre.lower():
            return b
    raise HTTPException(status_code=404, detail="Libro no encontrado")

#Registrar el préstamo de un libro a un usuario
@app.post("/prestamos/")
def registrar_prestamo(prestamo: Loan):
    for b in books_db:
        if b.nombre.lower() == prestamo.nombre_libro.lower():
            if b.estado == "prestado":
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya está prestado.")
            
            b.estado = "prestado"
            loans_db.append(prestamo)
            return {"mensaje": "Préstamo registrado exitosamente"}
            
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# e. Marcar un libro como devuelto
@app.put("/prestamos/devolver/{nombre_libro}", status_code=status.HTTP_200_OK)
def devolver_libro(nombre_libro: str):
    for b in books_db:
        if b.nombre.lower() == nombre_libro.lower():
            if b.estado == "disponible":
                raise HTTPException(status_code=400, detail="El libro no estaba prestado.")
            b.estado = "disponible"
            return {"mensaje": "Libro devuelto con éxito"}
            
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# f. Eliminar el registro de un préstamo
@app.delete("/prestamos/{nombre_libro}")
def eliminar_registro_prestamo(nombre_libro: str):
    for i, prestamo in enumerate(loans_db):
        if prestamo.nombre_libro.lower() == nombre_libro.lower():
            del loans_db[i]
            return {"mensaje": "Registro de préstamo eliminado"}
            
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El registro de préstamo ya no existe.")