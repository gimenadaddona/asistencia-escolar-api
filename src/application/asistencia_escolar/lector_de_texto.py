from abc import ABC, abstractmethod

from src.domain.asistencia_escolar.exceptions import DatosInvalidosError


class ImagenInvalidaError(DatosInvalidosError):
    """El archivo recibido no es una imagen utilizable."""


class LectorDeTextoNoDisponibleError(Exception):
    """El programa que lee texto de imágenes no está instalado o configurado."""


class LectorDeTexto(ABC):
    """Convierte una imagen en texto. Es un puerto: la implementación es intercambiable."""

    @abstractmethod
    def leer(self, imagen: bytes) -> str:
        ...
