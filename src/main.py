from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.infrastructure.fastapi.routers import acciones, alumnos, asistencia, reportes
from src.infrastructure.settings.config import get_settings
from src.infrastructure.sqlalchemy.database import engine
from src.infrastructure.sqlalchemy.models import orm_models


def create_app() -> FastAPI:
    settings = get_settings()
    orm_models.Base.metadata.create_all(engine)

    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

    @app.exception_handler(DatosInvalidosError)
    async def manejar_datos_invalidos(request: Request, exc: DatosInvalidosError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detalle": str(exc)})

    @app.exception_handler(ValueError)
    async def manejar_valor_invalido(request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detalle": str(exc)})

    for router in (alumnos.router, asistencia.router, acciones.router, reportes.router):
        app.include_router(router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
