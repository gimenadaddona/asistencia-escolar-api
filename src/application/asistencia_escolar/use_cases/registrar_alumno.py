from src.application.asistencia_escolar.dtos.alumno_dto import (
    AlumnoResponse,
    RegistrarAlumnoRequest,
)
from src.application.asistencia_escolar.mappers.alumno_mapper import AlumnoMapper
from src.domain.asistencia_escolar.repositories import AlumnoRepository


class RegistrarAlumnoUseCase:
    """Caso de uso: dar de alta un nuevo alumno en la nómina."""

    def __init__(self, alumno_repository: AlumnoRepository) -> None:
        self._alumno_repository = alumno_repository

    def execute(self, request: RegistrarAlumnoRequest) -> AlumnoResponse:
        alumno = AlumnoMapper.a_entidad(request)
        alumno_guardado = self._alumno_repository.guardar(alumno)
        return AlumnoMapper.a_response(alumno_guardado)
    