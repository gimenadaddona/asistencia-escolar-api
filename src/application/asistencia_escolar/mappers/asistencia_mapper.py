from typing import List

from src.application.asistencia_escolar.dtos.asistencia_dto import (
    AlertaAlumnoResponse,
    RegistroAsistenciaItem,
)
from src.domain.asistencia_escolar.entities import RegistroAsistencia
from src.domain.asistencia_escolar.events import AlertaInasistenciaGenerada
from src.domain.asistencia_escolar.value_objects import EstadoAsistencia, MotivoInasistencia


class AsistenciaMapper:
    """Traduce entre RegistroAsistencia (Domain) y sus DTOs (Application)."""

    @staticmethod
    def item_a_entidad(item: RegistroAsistenciaItem, fecha) -> RegistroAsistencia:
        """Un item de la planilla -> Entidad de dominio."""
        estado = EstadoAsistencia.PRESENTE if item.presente else EstadoAsistencia.AUSENTE
        motivo = (
            MotivoInasistencia(item.motivo_inasistencia)
            if item.motivo_inasistencia is not None
            else None
        )
        return RegistroAsistencia(
            alumno_id=item.alumno_id,
            fecha=fecha,
            estado=estado,
            motivo_inasistencia=motivo,
        )

    @staticmethod
    def alerta_a_response(alerta: AlertaInasistenciaGenerada) -> AlertaAlumnoResponse:
        """Evento de dominio -> DTO de salida."""
        return AlertaAlumnoResponse(
            alumno_id=alerta.alumno_id,
            nombre_completo=alerta.nombre_completo,
            cantidad_faltas_injustificadas=alerta.cantidad_faltas_injustificadas,
        )
        