from typing import List

from src.application.asistencia_escolar.dtos.alumno_dto import (
    AlumnoResponse,
    ListarNominaRequest,
    ListarNominaResponse,
)
from src.application.asistencia_escolar.mappers.alumno_mapper import AlumnoMapper
from src.domain.asistencia_escolar.entities import Alumno
from src.domain.asistencia_escolar.repositories import AlumnoRepository
from src.domain.asistencia_escolar.value_objects import AnioEscolar, Division


class ListarNominaUseCase:
    """Caso de uso: listar alumnos, opcionalmente filtrados por año y división."""

    def __init__(self, alumno_repository: AlumnoRepository) -> None:
        self._alumno_repository = alumno_repository

    def execute(self, request: ListarNominaRequest) -> ListarNominaResponse:
        alumnos: List[Alumno]

        if request.anio is not None and request.division is not None:
            alumnos = self._alumno_repository.listar_por_anio_division(
                AnioEscolar(request.anio), Division(request.division)
            )
        else:
            alumnos = self._alumno_repository.listar_todos()

        responses = [AlumnoMapper.a_response(a) for a in alumnos]
        return ListarNominaResponse(alumnos=responses, total=len(responses))
    