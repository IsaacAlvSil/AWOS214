from pydantic import BaseModel, Field
#modelo de validacion pydantic

class usuario_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, examples=["Isaac"])
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 - 123")
