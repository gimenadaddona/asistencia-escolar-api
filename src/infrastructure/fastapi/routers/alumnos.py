from typing import Optional

from fastapi import APIRouter, Depends, status

from src.application.asistencia_escolar.dtos.alumno_dto import (
    AlumnoResponse,
    ListarNominaRequest,
    ListarNominaResponse,
    RegistrarAlumnoRequest,
)
from src.application.asistencia_escolar.use_cases.listar_nomina import ListarNominaUseCase
from src.application.asistencia_escolar.use_cases.registrar_alumno import (
    RegistrarAlumnoUseCase,
)
from src.infrastructure.fastapi.dependencies import get_listar_nomina_uc, get_registrar_alumno_uc

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


@router.post("", response_model=AlumnoResponse, status_code=status.HTTP_201_CREATED)
def registrar_alumno(
    request: RegistrarAlumnoRequest,
    use_case: RegistrarAlumnoUseCase = Depends(get_registrar_alumno_uc),
) -> AlumnoResponse:
    return use_case.execute(request)


@router.get("", response_model=ListarNominaResponse)
def listar_nomina(
    anio: Optional[str] = None,
    division: Optional[str] = None,
    use_case: ListarNominaUseCase = Depends(get_listar_nomina_uc),
) -> ListarNominaResponse:
    return use_case.execute(ListarNominaRequest(anio=anio, division=division))
