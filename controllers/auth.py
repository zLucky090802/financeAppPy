from fastapi import Request, Response, HTTPException

# controllers/auth.py
from main import db  # Usa el db global conectado







from jose import jwt
import bcrypt
from datetime import datetime, timedelta
import os


# JWT
SECRET_KEY = os.getenv("SECRET_JWT_SEED", "Esto-Es-Una-Palabr@_SecretA1215615")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

def generar_jwt(user_id: int, nombre: str):
    payload = {
        "sub": str(user_id),
        "nombre": nombre,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# Función equivalente a `crearUsuario`
async def crear_usuario(req: Request):
    body = await req.json()
    nombre = body.get("nombre")
    email = body.get("email")
    password = body.get("password")

    if not nombre or not email or not password:
        raise HTTPException(status_code=400, detail="Faltan datos")

    usuario_existente = await db.usuarios.find_unique(where={"email": email})
    if usuario_existente:
        raise HTTPException(status_code=409, detail="El usuario ya existe con ese email")

    salt = bcrypt.gensalt()
    password_cifrada = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    nuevo_usuario = await db.usuarios.create(
        data={"nombre": nombre, "email": email, "password": password_cifrada}
    )

    return {
        "message": "Usuario creado",
        "usuario": {
            "id": nuevo_usuario.id,
            "email": nuevo_usuario.email,
        },
    }

# auth.py
async def login_usuario(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email:
        raise HTTPException(status_code=400, detail="El email es obligatorio.")

    usuario = await db.usuarios.find_unique(where={"email": email})
    if not usuario:
        raise HTTPException(status_code=404, detail=f"No se encontró ningún usuario con el email: {email}")

    valid_password = bcrypt.checkpw(password.encode("utf-8"), usuario.password.encode("utf-8"))
    if not valid_password:
        raise HTTPException(status_code=400, detail="Password incorrecto")

    token = generar_jwt(usuario.id, usuario.nombre)
    refresh_token = generar_jwt(usuario.id, usuario.nombre)

    return {
        "message": "Usuario encontrado correctamente.",
        "usuario": {
            "ok": True,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "id": usuario.id,
            "token": token,
            "refreshToken": refresh_token,
        },
    }
