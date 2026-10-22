from fastapi import APIRouter, Depends, status

from src.application.asistencia_escolar.dtos.accion_dto import (
    AccionResponse,
    HistorialAccionesResponse,
    RegistrarAccionRequest,
)
from src.application.asistencia_escolar.use_cases.consultar_historial_acciones import (
    ConsultarHistorialAccionesUseCase,
)
from src.application.asistencia_escolar.use_cases.registrar_accion_seguimiento import (
    RegistrarAccionSeguimientoUseCase,
)
from src.infrastructure.fastapi.dependencies import get_historial_uc, get_registrar_accion_uc

router = APIRouter(tags=["Acciones de seguimiento"])


@router.post("/acciones", response_model=AccionResponse, status_code=status.HTTP_201_CREATED)
def registrar_accion(
    request: RegistrarAccionRequest,
    use_case: RegistrarAccionSeguimientoUseCase = Depends(get_registrar_accion_uc),
) -> AccionResponse:
    return use_case.execute(request)


@router.get("/alumnos/{alumno_id}/acciones", response_model=HistorialAccionesResponse)
def historial_de_acciones(
    alumno_id: int,
    use_case: ConsultarHistorialAccionesUseCase = Depends(get_historial_uc),
) -> HistorialAccionesResponse:
    return use_case.execute(alumno_id)
