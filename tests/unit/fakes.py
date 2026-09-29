from datetime import date
from typing import Dict, List, Optional

from src.domain.asistencia_escolar.entities import (
    AccionSeguimiento,
    Alumno,
    RegistroAsistencia,
)
from src.domain.asistencia_escolar.repositories import (
    AccionSeguimientoRepository,
    AlumnoRepository,
    AsistenciaRepository,
)
from src.domain.asistencia_escolar.value_objects import AnioEscolar, Division


class FakeAlumnoRepository(AlumnoRepository):
    """Implementación en memoria de AlumnoRepository, solo para tests."""

    def __init__(self) -> None:
        self._alumnos: Dict[int, Alumno] = {}
        self._siguiente_id = 1

    def guardar(self, alumno: Alumno) -> Alumno:
        if alumno.id is None:
            alumno.id = self._siguiente_id
            self._siguiente_id += 1
        self._alumnos[alumno.id] = alumno
        return alumno

    def obtener_por_id(self, alumno_id: int) -> Optional[Alumno]:
        return self._alumnos.get(alumno_id)

    def listar_por_anio_division(self, anio: AnioEscolar, division: Division) -> List[Alumno]:
        return [
            a for a in self._alumnos.values()
            if a.anio.valor == anio.valor and a.division.valor == division.valor
        ]

    def listar_todos(self) -> List[Alumno]:
        return list(self._alumnos.values())
    
    def eliminar(self, alumno_id: int) -> None:
        self._alumnos.pop(alumno_id, None)


class FakeAsistenciaRepository(AsistenciaRepository):
    """Implementación en memoria de AsistenciaRepository, solo para tests."""

    def __init__(self) -> None:
        self._registros: List[RegistroAsistencia] = []
        self._siguiente_id = 1

    def guardar(self, registro: RegistroAsistencia) -> RegistroAsistencia:
        if registro.id is None:
            registro.id = self._siguiente_id
            self._siguiente_id += 1
        self._registros.append(registro)
        return registro

    def listar_por_alumno(self, alumno_id: int) -> List[RegistroAsistencia]:
        return [r for r in self._registros if r.alumno_id == alumno_id]

    def contar_faltas_injustificadas(self, alumno_id: int) -> int:
        return sum(
            1 for r in self._registros
            if r.alumno_id == alumno_id and r.es_falta_injustificada()
        )

    def existe_registro(self, alumno_id: int, fecha: date) -> bool:
        return any(
            r.alumno_id == alumno_id and r.fecha == fecha
            for r in self._registros
        )


class FakeAccionSeguimientoRepository(AccionSeguimientoRepository):
    """Implementación en memoria de AccionSeguimientoRepository, solo para tests."""

    def __init__(self) -> None:
        self._acciones: List[AccionSeguimiento] = []
        self._siguiente_id = 1

    def guardar(self, accion: AccionSeguimiento) -> AccionSeguimiento:
        if accion.id is None:
            accion.id = self._siguiente_id
            self._siguiente_id += 1
        self._acciones.append(accion)
        return accion

    def listar_por_alumno(self, alumno_id: int) -> List[AccionSeguimiento]:
        return [a for a in self._acciones if a.alumno_id == alumno_id]
    