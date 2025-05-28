from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime

class CuentaBase(BaseModel):
    usuario_id: Optional[int]
    nombre: str = Field(..., max_length=100)
    tipo: Optional[str] = Field(None, max_length=50)
    cuenta_base_id: Optional[int]
    saldo_inicial: Optional[Decimal] = Decimal("0.00")
    descripcion: Optional[str]

class CuentaCreate(CuentaBase):
    pass  # es_personalizada se fija automáticamente a True

class CuentaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    tipo: Optional[str] = Field(None, max_length=50)
    saldo_inicial: Optional[Decimal]
    cuenta_base_id: Optional[int]
    descripcion: Optional[str]

class Cuenta(CuentaBase):
    id: int
    es_personalizada: Optional[bool] = False
    fecha_creacion: Optional[datetime]

    class Config:
        orm_mode = True

class BalanceCuenta(BaseModel):
    usuarioId: int
    cuentaId: int
    saldoInicial: Decimal
    totalIngresos: Decimal
    totalGastos: Decimal
    capitalTotal: Decimal
    balanceTransacciones: Decimal
    balanceTotal: Decimal
