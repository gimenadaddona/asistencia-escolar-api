from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.domain.asistencia_escolar.value_objects import (
    AnioEscolar,
    Ciclo,
    Division,
    EstadoAsistencia,
    MotivoInasistencia,
    RolUsuario,
    TipoAccion,
)


@dataclass
class Alumno:
    nombre: str
    apellido: str
    ciclo: Ciclo
    anio: AnioEscolar
    division: Division
    id: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.nombre.strip():
            raise DatosInvalidosError("El nombre del alumno no puede estar vacio")
        if not self.apellido.strip():
            raise DatosInvalidosError("El apellido del alumno no puede estar vacio")
        if not self.anio.pertenece_a_ciclo(self.ciclo):
            raise DatosInvalidosError(f"El grado {self.anio.valor} no corresponde al ciclo")

    def nombre_completo(self) -> str:
        return f"{self.apellido}, {self.nombre}"


@dataclass
class RegistroAsistencia:
    alumno_id: int
    fecha: date
    estado: EstadoAsistencia
    motivo_inasistencia: Optional[MotivoInasistencia] = None
    id: Optional[int] = None

    def __post_init__(self) -> None:
        if self.estado == EstadoAsistencia.PRESENTE and self.motivo_inasistencia is not None:
            raise DatosInvalidosError("Un alumno presente no puede tener motivo de inasistencia")
        if self.estado == EstadoAsistencia.AUSENTE and self.motivo_inasistencia is None:
            raise DatosInvalidosError("Toda ausencia debe indicar un motivo")

    def es_falta_injustificada(self) -> bool:
        return self.motivo_inasistencia == MotivoInasistencia.INJUSTIFICADO


@dataclass
class AccionSeguimiento:
    alumno_id: int
    fecha: date
    tipo_accion: TipoAccion
    descripcion: str
    realizado_por: str
    rol_autor: RolUsuario
    id: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.descripcion.strip():
            raise DatosInvalidosError("La descripcion de la accion no puede estar vacia")
        if not self.realizado_por.strip():
            raise DatosInvalidosError("Debe indicarse quien realizo la accion")
