from schemas.categories import BaseModel, CategoriaBase, CategoriaCreate, CategoriaOut, CategoriaUpdate,Optional
from fastapi import HTTPException, status
from prisma_client import db
from fastapi.responses import JSONResponse
from prisma.errors import PrismaError

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

async def get_categorias_by_id(id: int):
    
    categoria = await db.categorias.find_unique(
        where={
            'id': int(id)
        }
    )

    if categoria:
        return categoria
    else:
        raise HTTPException(status_code=400, detail='Categoria no encontrada')


async def create_categorie(categorie: CategoriaBase) -> CategoriaBase:

    if not categorie.nombre:
        raise HTTPException(status_code=400, detail='El nombre es requerido')

    if not categorie.usuario_id:
        raise HTTPException(status_code=400, detail='El id del usuario es requerido')

    try:
        existing = await db.categorias.find_first(
            where={
                "usuario_id": categorie.usuario_id,
                "nombre": categorie.nombre
            }
        )
        if existing:
            print('Entrando al if de categoría existente')
            raise HTTPException(
                status_code=400,
                detail='La categoría ya existe para este usuario'
            )
        
        nueva_categoria = await db.categorias.create(
            data=categorie.model_dump()
        )

        return nueva_categoria

    except PrismaError as e:
        print("⛔ Error al crear categoría:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error al acceder a la base de datos'
        )

   



    
