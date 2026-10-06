import pytest

from src.application.asistencia_escolar.dtos.accion_dto import RegistrarAccionRequest
from src.application.asistencia_escolar.use_cases.consultar_historial_acciones import (
    ConsultarHistorialAccionesUseCase,
)
from src.application.asistencia_escolar.use_cases.registrar_accion_seguimiento import (
    RegistrarAccionSeguimientoUseCase,
)
from src.domain.asistencia_escolar.entities import Alumno
from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.domain.asistencia_escolar.value_objects import AnioEscolar, Ciclo, Division
from tests.unit.fakes import FakeAccionSeguimientoRepository, FakeAlumnoRepository


class TestConsultarHistorialAccionesUseCase:
    def test_devuelve_historial_vacio_si_no_hay_acciones(self) -> None:
        alumno_repo = FakeAlumnoRepository()
        accion_repo = FakeAccionSeguimientoRepository()
        alumno = alumno_repo.guardar(
            Alumno(nombre="Juan", apellido="Perez", ciclo=Ciclo.CICLO_1, anio=AnioEscolar("2°"), division=Division("A"))
        )
        caso_de_uso = ConsultarHistorialAccionesUseCase(
            accion_repository=accion_repo, alumno_repository=alumno_repo
        )

        response = caso_de_uso.execute(alumno.id)

        assert response.acciones == []
        assert response.nombre_completo_alumno == "Perez, Juan"

    def test_devuelve_todas_las_acciones_del_alumno(self) -> None:
        alumno_repo = FakeAlumnoRepository()
        accion_repo = FakeAccionSeguimientoRepository()
        alumno = alumno_repo.guardar(
            Alumno(nombre="Juan", apellido="Perez", ciclo=Ciclo.CICLO_1, anio=AnioEscolar("2°"), division=Division("A"))
        )
        registrar = RegistrarAccionSeguimientoUseCase(accion_repository=accion_repo)
        registrar.execute(RegistrarAccionRequest(
            alumno_id=alumno.id, tipo_accion="llamado_familia",
            descripcion="Primer llamado", realizado_por="Marta", rol_autor="docente",
        ))
        registrar.execute(RegistrarAccionRequest(
            alumno_id=alumno.id, tipo_accion="reunion_familia",
            descripcion="Reunion de seguimiento", realizado_por="Marta", rol_autor="docente",
        ))

        caso_de_uso = ConsultarHistorialAccionesUseCase(
            accion_repository=accion_repo, alumno_repository=alumno_repo
        )
        response = caso_de_uso.execute(alumno.id)

        assert len(response.acciones) == 2

    def test_rechaza_alumno_inexistente(self) -> None:
        alumno_repo = FakeAlumnoRepository()
        accion_repo = FakeAccionSeguimientoRepository()
        caso_de_uso = ConsultarHistorialAccionesUseCase(
            accion_repository=accion_repo, alumno_repository=alumno_repo
        )

        with pytest.raises(DatosInvalidosError):
            caso_de_uso.execute(999)
