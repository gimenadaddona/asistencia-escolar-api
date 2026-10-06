from src.application.asistencia_escolar.dtos.asistencia_dto import (
    AlumnoEnSeguimientoResponse,
    ReporteAlertasRequest,
    ReporteSeguimientoResponse,
)
from src.application.asistencia_escolar.use_cases.generar_reporte_alertas import (
    GenerarReporteAlertasUseCase,
)
from src.domain.asistencia_escolar.repositories import AccionSeguimientoRepository, AlumnoRepository


class GenerarReporteSeguimientoUseCase:
    """
    Caso de uso para directivo y orientacion: junta las alertas de inasistencia
    con el historial completo de acciones ya tomadas por el docente, alumno por alumno.
    """

    def __init__(
        self,
        reporte_alertas_use_case: GenerarReporteAlertasUseCase,
        accion_repository: AccionSeguimientoRepository,
        alumno_repository: AlumnoRepository,
    ) -> None:
        self._reporte_alertas_use_case = reporte_alertas_use_case
        self._accion_repository = accion_repository
        self._alumno_repository = alumno_repository

    def execute(self, request: ReporteAlertasRequest) -> ReporteSeguimientoResponse:
        reporte_alertas = self._reporte_alertas_use_case.execute(request)

        alumnos_en_seguimiento = []
        for alerta in reporte_alertas.alertas:
            alumno = self._alumno_repository.obtener_por_id(alerta.alumno_id)
            acciones = self._accion_repository.listar_por_alumno(alerta.alumno_id)

            acciones_dict = [
                {
                    "fecha": str(a.fecha),
                    "tipo_accion": a.tipo_accion.valor,
                    "descripcion": a.descripcion,
                    "realizado_por": a.realizado_por,
                    "rol_autor": a.rol_autor.value,
                }
                for a in acciones
            ]

            alumnos_en_seguimiento.append(
                AlumnoEnSeguimientoResponse(
                    alumno_id=alerta.alumno_id,
                    nombre_completo=alerta.nombre_completo,
                    anio=alumno.anio.valor if alumno else "",
                    division=alumno.division.valor if alumno else "",
                    cantidad_faltas_injustificadas=alerta.cantidad_faltas_injustificadas,
                    acciones=acciones_dict,
                )
            )

        return ReporteSeguimientoResponse(
            limite_configurado=reporte_alertas.limite_configurado,
            alumnos_en_seguimiento=alumnos_en_seguimiento,
        )
