from src.application.asistencia_escolar.dtos.alumno_dto import (
    ListarNominaRequest,
    RegistrarAlumnoRequest,
)
from src.application.asistencia_escolar.use_cases.listar_nomina import ListarNominaUseCase
from src.application.asistencia_escolar.use_cases.registrar_alumno import (
    RegistrarAlumnoUseCase,
)
from tests.unit.fakes import FakeAlumnoRepository


def _registrar_alumnos_de_prueba(repositorio: FakeAlumnoRepository) -> None:
    caso_de_uso = RegistrarAlumnoUseCase(alumno_repository=repositorio)
    caso_de_uso.execute(
        RegistrarAlumnoRequest(nombre="Juan", apellido="Perez", ciclo="1", anio="2°", division="A")
    )
    caso_de_uso.execute(
        RegistrarAlumnoRequest(nombre="Ana", apellido="Gomez", ciclo="1", anio="2°", division="A")
    )
    caso_de_uso.execute(
        RegistrarAlumnoRequest(nombre="Luis", apellido="Diaz", ciclo="2", anio="5°", division="C")
    )


class TestListarNominaUseCase:
    def test_lista_todos_los_alumnos_sin_filtro(self) -> None:
        repositorio = FakeAlumnoRepository()
        _registrar_alumnos_de_prueba(repositorio)
        caso_de_uso = ListarNominaUseCase(alumno_repository=repositorio)

        response = caso_de_uso.execute(ListarNominaRequest())

        assert response.total == 3

    def test_filtra_por_anio_y_division(self) -> None:
        repositorio = FakeAlumnoRepository()
        _registrar_alumnos_de_prueba(repositorio)
        caso_de_uso = ListarNominaUseCase(alumno_repository=repositorio)

        response = caso_de_uso.execute(ListarNominaRequest(anio="2°", division="A"))

        assert response.total == 2
        nombres = {a.nombre for a in response.alumnos}
        assert nombres == {"Juan", "Ana"}

    def test_filtro_sin_coincidencias_devuelve_lista_vacia(self) -> None:
        repositorio = FakeAlumnoRepository()
        _registrar_alumnos_de_prueba(repositorio)
        caso_de_uso = ListarNominaUseCase(alumno_repository=repositorio)

        response = caso_de_uso.execute(ListarNominaRequest(anio="6°", division="D"))

        assert response.total == 0
        assert response.alumnos == []
        