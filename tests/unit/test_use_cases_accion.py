from src.application.asistencia_escolar.dtos.accion_dto import RegistrarAccionRequest
from src.application.asistencia_escolar.use_cases.registrar_accion_seguimiento import (
    RegistrarAccionSeguimientoUseCase,
)
from tests.unit.fakes import FakeAccionSeguimientoRepository


class TestRegistrarAccionSeguimientoUseCase:
    def test_registra_una_accion_correctamente(self) -> None:
        repositorio = FakeAccionSeguimientoRepository()
        caso_de_uso = RegistrarAccionSeguimientoUseCase(accion_repository=repositorio)

        request = RegistrarAccionRequest(
            alumno_id=1,
            tipo_accion="llamado_familia",
            descripcion="Se llamo a la madre, no atendio",
            realizado_por="Marta Gomez",
            rol_autor="docente",
        )

        response = caso_de_uso.execute(request)

        assert response.id == 1
        assert response.alumno_id == 1
        assert response.tipo_accion == "llamado_familia"
        assert response.rol_autor == "docente"

    def test_la_accion_queda_persistida(self) -> None:
        repositorio = FakeAccionSeguimientoRepository()
        caso_de_uso = RegistrarAccionSeguimientoUseCase(accion_repository=repositorio)

        request = RegistrarAccionRequest(
            alumno_id=5,
            tipo_accion="reunion_familia",
            descripcion="Reunion con la madre y el padre",
            realizado_por="Marta Gomez",
            rol_autor="docente",
        )
        caso_de_uso.execute(request)

        acciones = repositorio.listar_por_alumno(5)
        assert len(acciones) == 1
        assert acciones[0].descripcion == "Reunion con la madre y el padre"
