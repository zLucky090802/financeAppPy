from pydantic import BaseModel
from typing import Optional

# Base: campos comunes
class CategoriaBase(BaseModel):
    nombre: str
    usuario_id: Optional[int] = None

# POST / -> Crear una categoría
class CategoriaCreate(CategoriaBase):
    pass

# PUT /:id -> Actualizar una categoría
class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    usuario_id: Optional[int] = None

# GET /:id y GET /usuario/:usuario_id -> respuesta
class CategoriaOut(CategoriaBase):
    id: int

    class Config:
        orm_mode = True
