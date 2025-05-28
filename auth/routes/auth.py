from fastapi import APIRouter
from schemas.auth import UsuarioNuevo, LoginRequest
from services.auth_services import crear_usuario, login_usuario

router = APIRouter()

@router.post("/new")
async def crear_usuario_route(user: UsuarioNuevo):
    return await crear_usuario(user.dict())

@router.post("/")
async def login_usuario_route(credentials: LoginRequest):
    return await login_usuario(credentials.dict())
