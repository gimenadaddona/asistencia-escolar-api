import io
import shutil
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

from src.application.asistencia_escolar.lector_de_texto import (
    ImagenInvalidaError,
    LectorDeTexto,
    LectorDeTextoNoDisponibleError,
)

TAMANO_MAXIMO_BYTES = 8 * 1024 * 1024
LADO_MAXIMO_PX = 3000
RUTA_WINDOWS = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")


class TesseractLectorDeTexto(LectorDeTexto):
    """Lee texto de una imagen con Tesseract, en esta computadora (sin enviar la foto a internet)."""

    def __init__(self, idioma: str = "spa") -> None:
        self._idioma = idioma

    def leer(self, imagen: bytes) -> str:
        preparada = self._preparar(imagen)
        try:
            import pytesseract
        except ImportError as error:
            raise LectorDeTextoNoDisponibleError("Falta instalar pytesseract") from error

        ruta = shutil.which("tesseract")
        if ruta is None and RUTA_WINDOWS.exists():
            ruta = str(RUTA_WINDOWS)
        if ruta is None:
            raise LectorDeTextoNoDisponibleError("No se encontró Tesseract en esta computadora")
        pytesseract.pytesseract.tesseract_cmd = ruta

        try:
            return str(pytesseract.image_to_string(preparada, lang=self._idioma, config="--psm 6"))
        except (pytesseract.TesseractNotFoundError, pytesseract.TesseractError) as error:
            raise LectorDeTextoNoDisponibleError(
                f"Tesseract no pudo leer la imagen (¿falta el idioma '{self._idioma}'?)"
            ) from error

    def _preparar(self, imagen: bytes) -> Image.Image:
        if len(imagen) > TAMANO_MAXIMO_BYTES:
            raise ImagenInvalidaError("La imagen pesa más de 8 MB")
        try:
            foto = Image.open(io.BytesIO(imagen))
            foto.load()
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as error:
            raise ImagenInvalidaError("El archivo no es una imagen válida") from error
        foto = ImageOps.exif_transpose(foto)
        gris = ImageOps.autocontrast(ImageOps.grayscale(foto))
        gris.thumbnail((LADO_MAXIMO_PX, LADO_MAXIMO_PX))
        return gris
