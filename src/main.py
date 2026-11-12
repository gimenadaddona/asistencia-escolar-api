from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.infrastructure.fastapi.routers import acciones, alumnos, asistencia, reportes, web
from src.infrastructure.settings.config import get_settings
from src.infrastructure.settings.logger import logger
from src.infrastructure.sqlalchemy.database import engine
from src.infrastructure.sqlalchemy.models import orm_models


def create_app() -> FastAPI:
    settings = get_settings()
    orm_models.Base.metadata.create_all(engine)

    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

    @app.exception_handler(DatosInvalidosError)
    async def manejar_datos_invalidos(request: Request, exc: DatosInvalidosError) -> JSONResponse:
        logger.warning("Dato invalido en %s %s: %s", request.method, request.url.path, exc)
        return JSONResponse(status_code=400, content={"detalle": str(exc)})

    @app.exception_handler(ValueError)
    async def manejar_valor_invalido(request: Request, exc: ValueError) -> JSONResponse:
        logger.warning("Valor invalido en %s %s: %s", request.method, request.url.path, exc)
        return JSONResponse(status_code=422, content={"detalle": str(exc)})

    @app.exception_handler(Exception)
    async def manejar_error_inesperado(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Error inesperado en %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={"detalle": "Ocurrió un error interno. Intentá de nuevo más tarde."},
        )

    app.include_router(web.router)
    for router in (alumnos.router, asistencia.router, acciones.router, reportes.router):
        app.include_router(router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
