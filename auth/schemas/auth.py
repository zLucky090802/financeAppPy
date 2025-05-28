from pydantic import BaseModel, EmailStr

class UsuarioNuevo(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
