from src.application.asistencia_escolar.dtos.asistencia_dto import (
    ReporteAlertasRequest,
    ReporteAlertasResponse,
)
from src.application.asistencia_escolar.mappers.asistencia_mapper import AsistenciaMapper
from src.domain.asistencia_escolar.repositories import AlumnoRepository, AsistenciaRepository
from src.domain.asistencia_escolar.services import ServicioDeteccionAlertaInasistencia


class GenerarReporteAlertasUseCase:
    def __init__(
        self,
        alumno_repository: AlumnoRepository,
        asistencia_repository: AsistenciaRepository,
        servicio_alertas: ServicioDeteccionAlertaInasistencia,
    ) -> None:
        self._alumno_repository = alumno_repository
        self._asistencia_repository = asistencia_repository
        self._servicio_alertas = servicio_alertas

    def execute(self, request: ReporteAlertasRequest) -> ReporteAlertasResponse:
        alumnos = self._alumno_repository.listar_todos()

        alumnos_con_faltas = [
            (alumno, self._asistencia_repository.contar_faltas_injustificadas(alumno.id))
            for alumno in alumnos
            if alumno.id is not None
        ]

        alertas = self._servicio_alertas.evaluar_lote(
            alumnos_con_faltas, limite=request.limite_faltas_injustificadas
        )

        alertas_response = [AsistenciaMapper.alerta_a_response(a) for a in alertas]

        return ReporteAlertasResponse(
            limite_configurado=request.limite_faltas_injustificadas,
            alertas=alertas_response,
            total_alumnos_en_alerta=len(alertas_response),
        )
