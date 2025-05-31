from fastapi import APIRouter, Path
from schemas.categories import BaseModel, CategoriaBase, CategoriaCreate, CategoriaOut, CategoriaUpdate, Optional
from services.categories_services import (
    get_categorias,
    get_categorias_by_id,
    create_categorie
)

router = APIRouter()

@router.get("/usuario/{usuario_id}", response_model= list[CategoriaOut])
async def get_categorias_router(usuario_id: int = Path(...)):
    return await get_categorias(usuario_id)
# async def get_categorias_router(user_id: int):
#     return await 

@router.get('/{id}', response_model=CategoriaOut)
async def get_categorias_by_id_router(id: int = Path(...)):
    return await get_categorias_by_id(id)

@router.post('/', response_model=CategoriaBase)
async def create_categorie_router(categorie:CategoriaBase):
    return await create_categorie(categorie)