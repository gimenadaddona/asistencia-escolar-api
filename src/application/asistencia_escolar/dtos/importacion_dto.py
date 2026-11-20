from typing import List

from pydantic import BaseModel, Field

from src.application.asistencia_escolar.dtos.alumno_dto import AlumnoResponse


class VistaPreviaNominaRequest(BaseModel):
    texto: str = Field(min_length=1, max_length=20000)


class CandidatoAlumno(BaseModel):
    apellido: str
    nombre: str
    revisar: bool
    linea_original: str


class VistaPreviaNominaResponse(BaseModel):
    candidatos: List[CandidatoAlumno]
    lineas_ignoradas: int


class AlumnoAImportar(BaseModel):
    apellido: str = Field(min_length=1, max_length=100)
    nombre: str = Field(min_length=1, max_length=100)


class ImportarNominaRequest(BaseModel):
    anio: str
    division: str
    alumnos: List[AlumnoAImportar] = Field(min_length=1, max_length=100)


class ImportarNominaResponse(BaseModel):
    registrados: List[AlumnoResponse]
    omitidos_por_duplicado: List[str]
