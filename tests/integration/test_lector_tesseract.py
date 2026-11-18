import io

import pytest
from PIL import Image, ImageDraw, ImageFont

from src.application.asistencia_escolar.lector_de_texto import (
    ImagenInvalidaError,
    LectorDeTextoNoDisponibleError,
)
from src.infrastructure.ocr.tesseract_lector import TesseractLectorDeTexto


def _imagen_con_texto(lineas: list[str]) -> bytes:
    lienzo = Image.new("RGB", (900, 120 + 90 * len(lineas)), "white")
    pincel = ImageDraw.Draw(lienzo)
    fuente = ImageFont.load_default(size=52)
    for numero, linea in enumerate(lineas):
        pincel.text((40, 40 + 90 * numero), linea, fill="black", font=fuente)
    salida = io.BytesIO()
    lienzo.save(salida, format="PNG")
    return salida.getvalue()


def test_rechaza_un_archivo_que_no_es_imagen() -> None:
    with pytest.raises(ImagenInvalidaError):
        TesseractLectorDeTexto().leer(b"esto no es una imagen")


def test_rechaza_una_imagen_demasiado_pesada() -> None:
    with pytest.raises(ImagenInvalidaError):
        TesseractLectorDeTexto().leer(b"0" * (9 * 1024 * 1024))


def test_lee_una_lista_impresa_de_nombres_inventados() -> None:
    imagen = _imagen_con_texto(["PEREZ JUAN", "GOMEZ ANA", "DIAZ LUIS"])
    try:
        texto = TesseractLectorDeTexto().leer(imagen).upper()
    except LectorDeTextoNoDisponibleError as error:
        pytest.skip(str(error))
    for apellido in ("PEREZ", "GOMEZ", "DIAZ"):
        assert apellido in texto
