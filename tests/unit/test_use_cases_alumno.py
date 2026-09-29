from src.application.asistencia_escolar.dtos.alumno_dto import RegistrarAlumnoRequest
from src.application.asistencia_escolar.use_cases.registrar_alumno import (
    RegistrarAlumnoUseCase,
)
from tests.unit.fakes import FakeAlumnoRepository


class TestRegistrarAlumnoUseCase:
    def test_registra_un_alumno_correctamente(self) -> None:
        repositorio = FakeAlumnoRepository()
        caso_de_uso = RegistrarAlumnoUseCase(alumno_repository=repositorio)

        request = RegistrarAlumnoRequest(
            nombre="Juan",
            apellido="Perez",
            ciclo="1",
            anio="2°",
            division="A",
        )

        response = caso_de_uso.execute(request)

        assert response.id == 1
        assert response.nombre_completo == "Perez, Juan"
        assert response.turno == "mañana"

    def test_asigna_ids_incrementales_a_varios_alumnos(self) -> None:
        repositorio = FakeAlumnoRepository()
        caso_de_uso = RegistrarAlumnoUseCase(alumno_repository=repositorio)

        request_1 = RegistrarAlumnoRequest(
            nombre="Juan", apellido="Perez", ciclo="1", anio="2°", division="A",
        )
        request_2 = RegistrarAlumnoRequest(
            nombre="Ana", apellido="Gomez", ciclo="2", anio="5°", division="C",
        )

        response_1 = caso_de_uso.execute(request_1)
        response_2 = caso_de_uso.execute(request_2)

        assert response_1.id == 1
        assert response_2.id == 2
        assert response_2.turno == "tarde"

    def test_el_alumno_queda_persistido_en_el_repositorio(self) -> None:
        repositorio = FakeAlumnoRepository()
        caso_de_uso = RegistrarAlumnoUseCase(alumno_repository=repositorio)

        request = RegistrarAlumnoRequest(
            nombre="Juan", apellido="Perez", ciclo="1", anio="2°", division="A",
        )
        response = caso_de_uso.execute(request)

        alumno_guardado = repositorio.obtener_por_id(response.id)
        assert alumno_guardado is not None
        assert alumno_guardado.nombre == "Juan"
        