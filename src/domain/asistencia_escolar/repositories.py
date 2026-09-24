from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from src.domain.asistencia_escolar.entities import (
    AccionSeguimiento,
    Alumno,
    RegistroAsistencia,
)
from src.domain.asistencia_escolar.value_objects import AnioEscolar, Division


class AlumnoRepository(ABC):
    @abstractmethod
    def guardar(self, alumno: Alumno) -> Alumno:
        ...

    @abstractmethod
    def obtener_por_id(self, alumno_id: int) -> Optional[Alumno]:
        ...

    @abstractmethod
    def listar_por_anio_division(self, anio: AnioEscolar, division: Division) -> List[Alumno]:
        ...

    @abstractmethod
    def eliminar(self, alumno_id: int) -> None:
        ...


class AsistenciaRepository(ABC):
    @abstractmethod
    def guardar(self, registro: RegistroAsistencia) -> RegistroAsistencia:
        ...

    @abstractmethod
    def listar_por_alumno(self, alumno_id: int) -> List[RegistroAsistencia]:
        ...

    @abstractmethod
    def contar_faltas_injustificadas(self, alumno_id: int) -> int:
        ...

    @abstractmethod
    def existe_registro(self, alumno_id: int, fecha: date) -> bool:
        ...


class AccionSeguimientoRepository(ABC):
    @abstractmethod
    def guardar(self, accion: AccionSeguimiento) -> AccionSeguimiento:
        ...

    @abstractmethod
    def listar_por_alumno(self, alumno_id: int) -> List[AccionSeguimiento]:
        ...
