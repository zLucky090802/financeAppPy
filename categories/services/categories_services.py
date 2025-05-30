from schemas.categories import BaseModel, CategoriaBase, CategoriaCreate, CategoriaOut, CategoriaUpdate,Optional
from fastapi import HTTPException, status
from prisma_client import db


async def get_categorias(user_id:int):
    user_id = user_id
    if not user_id:
        raise HTTPException(status_code=400, detail='usuario_id es requerido')
    
    categorias = await db.categorias.find_many(
        where={
            'usuario_id': int(user_id)
        }
    )

    return categorias

