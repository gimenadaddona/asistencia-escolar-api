from src.application.asistencia_escolar.dtos.alumno_dto import (
    AlumnoResponse,
    RegistrarAlumnoRequest,
)
from src.domain.asistencia_escolar.entities import Alumno
from src.domain.asistencia_escolar.value_objects import AnioEscolar, Ciclo, Division


class AlumnoMapper:
    """Traduce entre Alumno (Domain) y sus DTOs (Application)."""

    @staticmethod
    def a_entidad(request: RegistrarAlumnoRequest) -> Alumno:
        """DTO de entrada -> Entidad de dominio (valida las reglas de negocio)."""
        return Alumno(
            nombre=request.nombre,
            apellido=request.apellido,
            ciclo=Ciclo(request.ciclo),
            anio=AnioEscolar(request.anio),
            division=Division(request.division),
        )

    @staticmethod
    def a_response(alumno: Alumno) -> AlumnoResponse:
        """Entidad de dominio -> DTO de salida (para mostrar por API)."""
        return AlumnoResponse(
            id=alumno.id if alumno.id is not None else 0,
            nombre=alumno.nombre,
            apellido=alumno.apellido,
            nombre_completo=alumno.nombre_completo(),
            ciclo=alumno.ciclo.value,
            anio=alumno.anio.valor,
            division=alumno.division.valor,
            turno=alumno.division.obtener_turno(),
        )
        