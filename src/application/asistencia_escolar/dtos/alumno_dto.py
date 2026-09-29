from typing import List, Optional

from pydantic import BaseModel, Field


class RegistrarAlumnoRequest(BaseModel):
    """Datos necesarios para dar de alta un alumno."""
    nombre: str = Field(min_length=1)
    apellido: str = Field(min_length=1)
    ciclo: str
    anio: str
    division: str


class AlumnoResponse(BaseModel):
    """Datos de un alumno para devolver por API."""
    id: int
    nombre: str
    apellido: str
    nombre_completo: str
    ciclo: str
    anio: str
    division: str
    turno: str


class ListarNominaRequest(BaseModel):
    """Filtros opcionales para listar la nómina."""
    anio: Optional[str] = None
    division: Optional[str] = None


class ListarNominaResponse(BaseModel):
    """Lista de alumnos que cumplen el filtro."""
    alumnos: List[AlumnoResponse]
    total: int
    