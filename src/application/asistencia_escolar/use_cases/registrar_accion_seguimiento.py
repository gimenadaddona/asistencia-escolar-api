from datetime import date

from src.application.asistencia_escolar.dtos.accion_dto import (
    AccionResponse,
    RegistrarAccionRequest,
)
from src.application.asistencia_escolar.mappers.accion_mapper import AccionMapper
from src.domain.asistencia_escolar.repositories import AccionSeguimientoRepository


class RegistrarAccionSeguimientoUseCase:
    def __init__(self, accion_repository: AccionSeguimientoRepository) -> None:
        self._accion_repository = accion_repository

    def execute(self, request: RegistrarAccionRequest) -> AccionResponse:
        accion = AccionMapper.a_entidad(request, fecha=date.today())
        accion_guardada = self._accion_repository.guardar(accion)
        return AccionMapper.a_response(accion_guardada)
