from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(include_in_schema=False)

PAGINA_PASAR_LISTA = Path(__file__).resolve().parent.parent / "static" / "pasar_lista.html"


@router.get("/")
def pantalla_pasar_lista() -> FileResponse:
    return FileResponse(PAGINA_PASAR_LISTA, media_type="text/html")
