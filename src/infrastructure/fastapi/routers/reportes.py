from fastapi import APIRouter, Depends, Query

from src.application.asistencia_escolar.dtos.asistencia_dto import (
    ReporteAlertasRequest,
    ReporteAlertasResponse,
    ReporteSeguimientoResponse,
)
from src.application.asistencia_escolar.use_cases.generar_reporte_alertas import (
    GenerarReporteAlertasUseCase,
)
from src.application.asistencia_escolar.use_cases.generar_reporte_seguimiento import (
    GenerarReporteSeguimientoUseCase,
)
from src.infrastructure.fastapi.dependencies import (
    get_reporte_alertas_uc,
    get_reporte_seguimiento_uc,
)

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/alertas", response_model=ReporteAlertasResponse)
def reporte_alertas(
    limite: int = Query(default=5, gt=0, description="Faltas injustificadas para alertar"),
    use_case: GenerarReporteAlertasUseCase = Depends(get_reporte_alertas_uc),
) -> ReporteAlertasResponse:
    return use_case.execute(ReporteAlertasRequest(limite_faltas_injustificadas=limite))


@router.get("/seguimiento", response_model=ReporteSeguimientoResponse)
def reporte_seguimiento(
    limite: int = Query(default=5, gt=0, description="Faltas injustificadas para alertar"),
    use_case: GenerarReporteSeguimientoUseCase = Depends(get_reporte_seguimiento_uc),
) -> ReporteSeguimientoResponse:
    return use_case.execute(ReporteAlertasRequest(limite_faltas_injustificadas=limite))
