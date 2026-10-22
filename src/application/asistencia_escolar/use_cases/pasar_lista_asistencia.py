from typing import Set

from src.application.asistencia_escolar.dtos.asistencia_dto import (
    PasarListaRequest,
    PasarListaResponse,
)
from src.application.asistencia_escolar.mappers.asistencia_mapper import AsistenciaMapper
from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.domain.asistencia_escolar.repositories import AlumnoRepository, AsistenciaRepository
from src.domain.asistencia_escolar.value_objects import AnioEscolar, Division


class PasarListaAsistenciaUseCase:
    """Registra la asistencia de una division completa en una fecha."""

    def __init__(
        self,
        asistencia_repository: AsistenciaRepository,
        alumno_repository: AlumnoRepository,
    ) -> None:
        self._asistencia_repository = asistencia_repository
        self._alumno_repository = alumno_repository

    def execute(self, request: PasarListaRequest) -> PasarListaResponse:
        anio = AnioEscolar(request.anio)
        division = Division(request.division)

        alumnos_vistos: Set[int] = set()
        for item in request.registros:
            if item.alumno_id in alumnos_vistos:
                raise DatosInvalidosError(
                    f"El alumno {item.alumno_id} aparece repetido en la planilla"
                )
            alumnos_vistos.add(item.alumno_id)

            alumno = self._alumno_repository.obtener_por_id(item.alumno_id)
            if alumno is None:
                raise DatosInvalidosError(f"No existe un alumno con id {item.alumno_id}")
            if alumno.anio.valor != anio.valor or alumno.division.valor != division.valor:
                raise DatosInvalidosError(
                    f"El alumno {alumno.nombre_completo()} no pertenece a "
                    f"{anio.valor} {division.valor}"
                )
            if self._asistencia_repository.existe_registro(item.alumno_id, request.fecha):
                raise DatosInvalidosError(
                    f"Ya existe un registro de asistencia para el alumno {item.alumno_id} "
                    f"en la fecha {request.fecha}"
                )

        registros = [
            AsistenciaMapper.item_a_entidad(item, request.fecha)
            for item in request.registros
        ]

        for registro in registros:
            self._asistencia_repository.guardar(registro)

        return PasarListaResponse(
            fecha=request.fecha,
            anio=request.anio,
            division=request.division,
            cantidad_registrados=len(registros),
        )
