from src.application.asistencia_escolar.dtos.asistencia_dto import (
    PasarListaRequest,
    PasarListaResponse,
)
from src.application.asistencia_escolar.mappers.asistencia_mapper import AsistenciaMapper
from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.domain.asistencia_escolar.repositories import AsistenciaRepository


class PasarListaAsistenciaUseCase:
    """Caso de uso: registrar la asistencia de todos los alumnos de una división en una fecha."""

    def __init__(self, asistencia_repository: AsistenciaRepository) -> None:
        self._asistencia_repository = asistencia_repository

    def execute(self, request: PasarListaRequest) -> PasarListaResponse:
        cantidad_guardados = 0

        for item in request.registros:
            if self._asistencia_repository.existe_registro(item.alumno_id, request.fecha):
                raise DatosInvalidosError(
                    f"Ya existe un registro de asistencia para el alumno {item.alumno_id} "
                    f"en la fecha {request.fecha}"
                )

            registro = AsistenciaMapper.item_a_entidad(item, request.fecha)
            self._asistencia_repository.guardar(registro)
            cantidad_guardados += 1

        return PasarListaResponse(
            fecha=request.fecha,
            anio=request.anio,
            division=request.division,
            cantidad_registrados=cantidad_guardados,
        )
        