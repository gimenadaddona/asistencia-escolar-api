import re
from typing import List, Optional

from src.application.asistencia_escolar.dtos.importacion_dto import (
    CandidatoAlumno,
    VistaPreviaNominaRequest,
    VistaPreviaNominaResponse,
)

_NUMERACION = re.compile(r"^\s*\d{1,3}\s*[\.\)\-:]*\s+")


def _limpiar(texto: str) -> List[str]:
    sin_simbolos = re.sub(r"[^\w\s'\-]", " ", texto).replace("_", " ")
    return [
        t
        for t in sin_simbolos.split()
        if re.search(r"[^\W\d_]", t) and not re.search(r"\d", t)
    ]


class VistaPreviaNominaUseCase:
    """Convierte texto libre (una lista de alumnos) en un borrador para revisar."""

    def execute(self, request: VistaPreviaNominaRequest) -> VistaPreviaNominaResponse:
        candidatos: List[CandidatoAlumno] = []
        ignoradas = 0
        for cruda in request.texto.splitlines():
            if not cruda.strip():
                continue
            candidato = self._analizar_linea(cruda)
            if candidato is None:
                ignoradas += 1
            else:
                candidatos.append(candidato)
        return VistaPreviaNominaResponse(candidatos=candidatos, lineas_ignoradas=ignoradas)

    def _analizar_linea(self, cruda: str) -> Optional[CandidatoAlumno]:
        linea = _NUMERACION.sub("", cruda).strip()
        if "," in linea:
            parte_apellido, _, parte_nombre = linea.partition(",")
            apellido = _limpiar(parte_apellido)
            nombre = _limpiar(parte_nombre)
            if not apellido or not nombre:
                return None
            revisar = False
        else:
            palabras = _limpiar(linea)
            if len(palabras) < 2:
                return None
            apellido, nombre = palabras[:1], palabras[1:]
            revisar = len(palabras) > 2
        return CandidatoAlumno(
            apellido=" ".join(apellido).title(),
            nombre=" ".join(nombre).title(),
            revisar=revisar,
            linea_original=cruda.strip(),
        )
