from fastapi import APIRouter
from pydantic import BaseModel
from controllers.auth import crear_usuario, login_usuario

class UsuarioNuevo(BaseModel):
    nombre: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post("/new")
async def crear_usuario_route(user: UsuarioNuevo):
    return await crear_usuario(user.model_dump())


@router.post("/")
async def login_usuario_route(credentials: LoginRequest):
    return await login_usuario(credentials.model_dump())

