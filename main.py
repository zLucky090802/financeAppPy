from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from database import Base, engine
from prisma_client import db
from routes import auth

load_dotenv()
from sqlalchemy import text


try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("✅ Conexión a la base de datos establecida")
except Exception as e:
    print("❌ Error al conectar a la base de datos:", e)

app = FastAPI()



@app.on_event("startup")
async def startup():
    await db.connect()
    print("✅ Prisma conectado")

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    print("❌ Prisma desconectado")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8100"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Rutas
app.include_router(auth.router, prefix="/financeApp/auth", tags=["Auth"])
# app.include_router(accounts.router, prefix="/financeApp/accounts", tags=["Accounts"])
# app.include_router(movements.router, prefix="/financeApp/movements", tags=["Movements"])
# app.include_router(categorias.router, prefix="/financeApp/categorias", tags=["Categorias"])
Base.metadata.create_all(bind=engine)
# Iniciar servidor
if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv("PORT", 3000))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
