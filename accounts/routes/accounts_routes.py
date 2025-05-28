from fastapi import APIRouter, Path, status
from typing import List
from schema.accounts import Cuenta, CuentaCreate, CuentaUpdate, BalanceCuenta
from services.accounts_services import (
    get_cuentas_predeterminadas,
    get_cuentas_personalizadas,
    get_cuenta_by_id,
    create_cuenta,
    update_cuenta,
    delete_cuenta,
    get_balance_cuenta_by_id,
)

router = APIRouter()

@router.get("/predeterminadas", response_model=List[Cuenta])
async def route_get_cuentas_predeterminadas():
    return await get_cuentas_predeterminadas()

@router.get("/personalizadas/{usuario_id}", response_model=List[Cuenta])
async def route_get_cuentas_personalizadas(usuario_id: int = Path(...)):
    return await get_cuentas_personalizadas(usuario_id)

@router.get("/{id}", response_model=Cuenta)
async def route_get_cuenta_by_id(id: int = Path(...)):
    return await get_cuenta_by_id(id)

@router.post("/", response_model=Cuenta, status_code=status.HTTP_201_CREATED)
async def route_create_cuenta(cuenta: CuentaCreate):
    return await create_cuenta(cuenta)

@router.put("/{id}", response_model=Cuenta)
async def route_update_cuenta(id: int, cuenta: CuentaUpdate):
    return await update_cuenta(id, cuenta)

@router.delete("/{id}/{usuario_id}", status_code=status.HTTP_200_OK)
async def route_delete_cuenta(id: int, usuario_id: int):
    return await delete_cuenta(id, usuario_id)

@router.get("/balance/{usuario_id}/{cuenta_id}", response_model=BalanceCuenta)
async def route_get_balance_cuenta_by_id(usuario_id: int, cuenta_id: int):
    return await get_balance_cuenta_by_id(usuario_id, cuenta_id)
