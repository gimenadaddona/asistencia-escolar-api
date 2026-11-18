from typing import List, Set, Tuple

from src.application.asistencia_escolar.dtos.importacion_dto import (
    ImportarNominaRequest,
    ImportarNominaResponse,
)
from src.application.asistencia_escolar.mappers.alumno_mapper import AlumnoMapper
from src.domain.asistencia_escolar.entities import Alumno
from src.domain.asistencia_escolar.repositories import AlumnoRepository
from src.domain.asistencia_escolar.value_objects import AnioEscolar, Ciclo, Division


def _clave(apellido: str, nombre: str) -> Tuple[str, str]:
    return (" ".join(apellido.split()).casefold(), " ".join(nombre.split()).casefold())


class ImportarNominaUseCase:
    """Registra varios alumnos de un curso. Valida todo antes de guardar y omite duplicados."""

    def __init__(self, alumno_repository: AlumnoRepository) -> None:
        self._alumno_repository = alumno_repository

    def execute(self, request: ImportarNominaRequest) -> ImportarNominaResponse:
        anio = AnioEscolar(request.anio)
        division = Division(request.division)
        ciclo = Ciclo.CICLO_1 if anio.pertenece_a_ciclo(Ciclo.CICLO_1) else Ciclo.CICLO_2

        existentes: Set[Tuple[str, str]] = {
            _clave(a.apellido, a.nombre)
            for a in self._alumno_repository.listar_por_anio_division(anio, division)
        }

        nuevos: List[Alumno] = []
        omitidos: List[str] = []
        for item in request.alumnos:
            apellido = item.apellido.strip()
            nombre = item.nombre.strip()
            clave = _clave(apellido, nombre)
            if clave in existentes:
                omitidos.append(f"{apellido}, {nombre}")
                continue
            existentes.add(clave)
            nuevos.append(
                Alumno(nombre=nombre, apellido=apellido, ciclo=ciclo, anio=anio, division=division)
            )

        registrados = [
            AlumnoMapper.a_response(self._alumno_repository.guardar(alumno)) for alumno in nuevos
        ]
        return ImportarNominaResponse(registrados=registrados, omitidos_por_duplicado=omitidos)
