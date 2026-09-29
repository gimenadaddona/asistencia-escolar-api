from datetime import date
from typing import List

from pydantic import BaseModel, Field


class RegistrarAccionRequest(BaseModel):
    """Datos para registrar una acción de seguimiento sobre un alumno."""
    alumno_id: int
    tipo_accion: str
    descripcion: str = Field(min_length=1)
    realizado_por: str = Field(min_length=1)
    rol_autor: str


class AccionResponse(BaseModel):
    """Una acción de seguimiento, para mostrar en el historial."""
    id: int
    alumno_id: int
    fecha: date
    tipo_accion: str
    descripcion: str
    realizado_por: str
    rol_autor: str


class HistorialAccionesResponse(BaseModel):
    """Historial completo de acciones de un alumno."""
    alumno_id: int
    nombre_completo_alumno: str
    acciones: List[AccionResponse]
    