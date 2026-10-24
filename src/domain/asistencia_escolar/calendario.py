from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List, Optional, Tuple

from src.domain.asistencia_escolar.exceptions import DatosInvalidosError


class Trimestre(int, Enum):
    """Trimestre del ciclo lectivo. Enero y febrero no pertenecen a ninguno."""

    PRIMERO = 1
    SEGUNDO = 2
    TERCERO = 3

    def meses(self) -> Tuple[int, ...]:
        if self is Trimestre.PRIMERO:
            return (3, 4, 5)
        if self is Trimestre.SEGUNDO:
            return (6, 7, 8)
        return (9, 10, 11, 12)

    @staticmethod
    def de_mes(mes: int) -> Optional["Trimestre"]:
        for trimestre in Trimestre:
            if mes in trimestre.meses():
                return trimestre
        return None


class TipoDiaNoLectivo(str, Enum):
    FERIADO = "feriado"
    SUSPENSION_CLASES = "suspension_clases"
    OTRO = "otro"


@dataclass
class DiaNoLectivo:
    """Fecha sin clases: feriado, suspension u otro motivo."""

    fecha: date
    tipo: TipoDiaNoLectivo
    descripcion: str
    id: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.descripcion.strip():
            raise DatosInvalidosError("La descripcion del dia no lectivo no puede estar vacia")


class DiaNoLectivoRepository(ABC):
    @abstractmethod
    def guardar(self, dia: DiaNoLectivo) -> DiaNoLectivo:
        ...

    @abstractmethod
    def obtener_por_id(self, dia_id: int) -> Optional[DiaNoLectivo]:
        ...

    @abstractmethod
    def obtener_por_fecha(self, fecha: date) -> Optional[DiaNoLectivo]:
        ...

    @abstractmethod
    def listar_por_ciclo_lectivo(self, ciclo_lectivo: int) -> List[DiaNoLectivo]:
        ...

    @abstractmethod
    def eliminar(self, dia_id: int) -> None:
        ...
