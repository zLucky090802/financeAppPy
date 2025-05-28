# auth_service/main.py

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_path)  # Añadir al inicio para prioridad

print("sys.path:", sys.path)  # Debug para ver si está incluida la raíz

from prisma_client import db  # Importar después de modificar sys.path
from routes import auth  # Asegúrate que "routes/auth.py" contiene el router llamado "router"

# Crear instancia de FastAPI
app = FastAPI(title="Auth Service")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8100"],  # Cambia según tu frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de ciclo de vida
@app.on_event("startup")
async def startup():
    await db.connect()
    print("✅ Prisma conectado")

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    print("❌ Prisma desconectado")

# Registrar rutas
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Punto de entrada si se ejecuta directamente
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
