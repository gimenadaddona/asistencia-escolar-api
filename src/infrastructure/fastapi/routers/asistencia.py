from fastapi import APIRouter, Depends, status

from src.application.asistencia_escolar.dtos.asistencia_dto import (
    PasarListaRequest,
    PasarListaResponse,
)
from src.application.asistencia_escolar.use_cases.pasar_lista_asistencia import (
    PasarListaAsistenciaUseCase,
)
from src.infrastructure.fastapi.dependencies import get_pasar_lista_uc

router = APIRouter(prefix="/asistencia", tags=["Asistencia"])


@router.post("", response_model=PasarListaResponse, status_code=status.HTTP_201_CREATED)
def pasar_lista(
    request: PasarListaRequest,
    use_case: PasarListaAsistenciaUseCase = Depends(get_pasar_lista_uc),
) -> PasarListaResponse:
    return use_case.execute(request)
