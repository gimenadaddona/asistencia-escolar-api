from src.application.asistencia_escolar.dtos.accion_dto import (
    AccionResponse,
    RegistrarAccionRequest,
)
from src.domain.asistencia_escolar.entities import AccionSeguimiento
from src.domain.asistencia_escolar.value_objects import RolUsuario, TipoAccion


class AccionMapper:
    """Traduce entre AccionSeguimiento (Domain) y sus DTOs (Application)."""

    @staticmethod
    def a_entidad(request: RegistrarAccionRequest, fecha) -> AccionSeguimiento:
        return AccionSeguimiento(
            alumno_id=request.alumno_id,
            fecha=fecha,
            tipo_accion=TipoAccion(request.tipo_accion),
            descripcion=request.descripcion,
            realizado_por=request.realizado_por,
            rol_autor=RolUsuario(request.rol_autor),
        )

    @staticmethod
    def a_response(accion: AccionSeguimiento) -> AccionResponse:
        return AccionResponse(
            id=accion.id if accion.id is not None else 0,
            alumno_id=accion.alumno_id,
            fecha=accion.fecha,
            tipo_accion=accion.tipo_accion.valor,
            descripcion=accion.descripcion,
            realizado_por=accion.realizado_por,
            rol_autor=accion.rol_autor.value,
        )
        