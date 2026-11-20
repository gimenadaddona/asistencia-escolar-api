from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.application.asistencia_escolar.dtos.importacion_dto import (
    ImportarNominaRequest,
    ImportarNominaResponse,
    VistaPreviaNominaRequest,
    VistaPreviaNominaResponse,
)
from src.application.asistencia_escolar.use_cases.importar_nomina import ImportarNominaUseCase
from src.application.asistencia_escolar.use_cases.vista_previa_nomina import (
    VistaPreviaNominaUseCase,
)
from src.infrastructure.fastapi.dependencies import get_session
from src.infrastructure.sqlalchemy.repositories.alumno_repository import (
    SqlAlchemyAlumnoRepository,
)

router = APIRouter(prefix="/alumnos/importar", tags=["Carga de nómina"])


def get_importar_nomina_uc(session: Session = Depends(get_session)) -> ImportarNominaUseCase:
    return ImportarNominaUseCase(alumno_repository=SqlAlchemyAlumnoRepository(session))


@router.post("/vista-previa", response_model=VistaPreviaNominaResponse)
def vista_previa(request: VistaPreviaNominaRequest) -> VistaPreviaNominaResponse:
    return VistaPreviaNominaUseCase().execute(request)


@router.post("", response_model=ImportarNominaResponse, status_code=status.HTTP_201_CREATED)
def importar(
    request: ImportarNominaRequest,
    use_case: ImportarNominaUseCase = Depends(get_importar_nomina_uc),
) -> ImportarNominaResponse:
    return use_case.execute(request)
