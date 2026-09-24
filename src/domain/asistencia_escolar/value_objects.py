from dataclasses import dataclass
from enum import Enum

from src.domain.asistencia_escolar.exceptions import DatosInvalidosError


class Ciclo(str, Enum):
    CICLO_1 = "1"
    CICLO_2 = "2"


ANIOS_VALIDOS: set[str] = {"1°", "2°", "3°", "4°", "5°", "6°"}
DIVISIONES_VALIDAS: set[str] = {"A", "B", "C", "D"}

TURNO_POR_DIVISION: dict[str, str] = {
    "A": "mañana",
    "B": "mañana",
    "C": "tarde",
    "D": "tarde",
}


@dataclass(frozen=True)
class AnioEscolar:
    valor: str

    def __post_init__(self) -> None:
        if self.valor not in ANIOS_VALIDOS:
            raise DatosInvalidosError(f"Grado invalido: {self.valor}")

    def pertenece_a_ciclo(self, ciclo: Ciclo) -> bool:
        anios_ciclo_1 = {"1°", "2°", "3°"}
        if ciclo == Ciclo.CICLO_1:
            return self.valor in anios_ciclo_1
        return self.valor not in anios_ciclo_1


@dataclass(frozen=True)
class Division:
    valor: str

    def __post_init__(self) -> None:
        if self.valor not in DIVISIONES_VALIDAS:
            raise DatosInvalidosError(f"Division invalida: {self.valor}")

    def obtener_turno(self) -> str:
        return TURNO_POR_DIVISION[self.valor]


class EstadoAsistencia(str, Enum):
    PRESENTE = "presente"
    AUSENTE = "ausente"


class MotivoInasistencia(str, Enum):
    CLIMATICO = "climatico"
    JUSTIFICADO = "justificado"
    INJUSTIFICADO = "injustificado"


TIPOS_ACCION_VALIDOS: set[str] = {
    "llamado_familia",
    "nota_cuaderno",
    "reunion_familia",
    "derivacion_orientacion",
    "otro",
}


@dataclass(frozen=True)
class TipoAccion:
    valor: str

    def __post_init__(self) -> None:
        if self.valor not in TIPOS_ACCION_VALIDOS:
            raise DatosInvalidosError(f"Tipo de accion invalido: {self.valor}")


class RolUsuario(str, Enum):
    DOCENTE = "docente"
    DIRECTIVO = "directivo"
    ORIENTACION = "orientacion"
