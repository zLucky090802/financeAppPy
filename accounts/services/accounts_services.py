
from schema.accounts import Cuenta, CuentaCreate, CuentaUpdate, BalanceCuenta
from fastapi import HTTPException, status
from prisma_client import db




async def get_cuentas_predeterminadas() -> list[Cuenta]:
    return await db.cuentas.find_many(where={"es_personalizada": False})

async def get_cuentas_personalizadas(usuario_id: int) -> list[Cuenta]:
    return await db.cuentas.find_many(where={"usuario_id": usuario_id, "es_personalizada": True})

async def get_cuenta_by_id(id: int) -> Cuenta:
    cuenta = await db.cuentas.find_unique(where={"id": id})
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return cuenta

async def create_cuenta(cuenta: CuentaCreate) -> Cuenta:
    try:
        return await db.cuentas.create(data={**cuenta.dict(), "es_personalizada": True})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la cuenta: {str(e)}")

async def update_cuenta(id: int, cuenta: CuentaUpdate) -> Cuenta:
    cuenta_existente = await db.cuentas.find_unique(where={"id": id})
    if not cuenta_existente:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    data_to_update = cuenta.dict(exclude_unset=True)
    try:
        return await db.cuentas.update(where={"id": id}, data=data_to_update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la cuenta: {str(e)}")

async def delete_cuenta(id: int, usuario_id: int) -> dict:
    cuenta_existente = await db.cuentas.find_first(where={"id": id, "usuario_id": usuario_id})
    if not cuenta_existente:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    try:
        await db.transacciones.delete_many(where={"cuenta_id": id})
        await db.cuentas.delete(where={"id": id})
        return {"ok": True, "msg": "Cuenta eliminada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la cuenta: {str(e)}")

async def get_balance_cuenta_by_id(usuario_id: int, cuenta_id: int) -> BalanceCuenta:
    cuenta = await db.cuentas.find_first(where={"id": cuenta_id, "usuario_id": usuario_id})
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada para este usuario")

    movimientos = await db.transacciones.find_many(
        where={"cuenta_id": cuenta_id, "usuario_id": usuario_id},
        select={"tipo": True, "monto": True}
    )

    total_ingresos = 0
    total_gastos = 0

    for mov in movimientos:
        monto = float(mov.monto)
        if mov.tipo == "ingreso":
            total_ingresos += monto
        elif mov.tipo == "gasto":
            total_gastos += monto

    saldo_inicial = float(cuenta.saldo_inicial or 0)
    balance_transacciones = total_ingresos - total_gastos
    balance_total = saldo_inicial + balance_transacciones
    capital_total = saldo_inicial + total_ingresos

    return BalanceCuenta(
        usuarioId=usuario_id,
        cuentaId=cuenta_id,
        saldoInicial=saldo_inicial,
        totalIngresos=total_ingresos,
        totalGastos=total_gastos,
        capitalTotal=capital_total,
        balanceTransacciones=balance_transacciones,
        balanceTotal=balance_total,
    )
