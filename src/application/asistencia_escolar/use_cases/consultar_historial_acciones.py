from src.application.asistencia_escolar.dtos.accion_dto import HistorialAccionesResponse
from src.application.asistencia_escolar.mappers.accion_mapper import AccionMapper
from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.domain.asistencia_escolar.repositories import AccionSeguimientoRepository, AlumnoRepository


class ConsultarHistorialAccionesUseCase:
    def __init__(
        self,
        accion_repository: AccionSeguimientoRepository,
        alumno_repository: AlumnoRepository,
    ) -> None:
        self._accion_repository = accion_repository
        self._alumno_repository = alumno_repository

    def execute(self, alumno_id: int) -> HistorialAccionesResponse:
        alumno = self._alumno_repository.obtener_por_id(alumno_id)
        if alumno is None:
            raise DatosInvalidosError(f"No existe un alumno con id {alumno_id}")

        acciones = self._accion_repository.listar_por_alumno(alumno_id)
        acciones_response = [AccionMapper.a_response(a) for a in acciones]

        return HistorialAccionesResponse(
            alumno_id=alumno_id,
            nombre_completo_alumno=alumno.nombre_completo(),
            acciones=acciones_response,
        )
