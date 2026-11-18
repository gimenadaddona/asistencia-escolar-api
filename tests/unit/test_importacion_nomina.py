import pytest

from src.application.asistencia_escolar.dtos.importacion_dto import (
    AlumnoAImportar,
    ImportarNominaRequest,
    VistaPreviaNominaRequest,
)
from src.application.asistencia_escolar.use_cases.importar_nomina import ImportarNominaUseCase
from src.application.asistencia_escolar.use_cases.vista_previa_nomina import (
    VistaPreviaNominaUseCase,
)
from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from tests.unit.fakes import FakeAlumnoRepository


def _vista(texto: str):
    return VistaPreviaNominaUseCase().execute(VistaPreviaNominaRequest(texto=texto))


def _pedido(alumnos, anio="2°", division="A"):
    return ImportarNominaRequest(anio=anio, division=division, alumnos=alumnos)


class TestVistaPrevia:
    def test_apellido_coma_nombre(self) -> None:
        c = _vista("PEREZ, juan").candidatos[0]
        assert (c.apellido, c.nombre, c.revisar) == ("Perez", "Juan", False)

    def test_apellido_y_nombre_sin_coma(self) -> None:
        c = _vista("Gomez Ana").candidatos[0]
        assert (c.apellido, c.nombre, c.revisar) == ("Gomez", "Ana", False)

    def test_quita_numeracion_y_numeros(self) -> None:
        c = _vista("12. Diaz Luis 45123456").candidatos[0]
        assert (c.apellido, c.nombre) == ("Diaz", "Luis")

    def test_tres_palabras_sin_coma_se_marcan_para_revisar(self) -> None:
        assert _vista("Garcia Lopez Maria").candidatos[0].revisar is True

    def test_ignora_renglones_vacios_y_ruido(self) -> None:
        resultado = _vista("\n  \nPerez Juan\n|||\nX\n")
        assert len(resultado.candidatos) == 1
        assert resultado.lineas_ignoradas == 2


class TestImportarNomina:
    def test_registra_varios_alumnos_con_su_ciclo(self) -> None:
        repo = FakeAlumnoRepository()
        resultado = ImportarNominaUseCase(repo).execute(
            _pedido([AlumnoAImportar(apellido="Perez", nombre="Juan"),
                     AlumnoAImportar(apellido="Gomez", nombre="Ana")])
        )
        assert len(resultado.registrados) == 2
        assert resultado.registrados[0].ciclo == "1"
        assert resultado.registrados[0].turno == "mañana"

    def test_omite_duplicados_sin_importar_mayusculas(self) -> None:
        caso_de_uso = ImportarNominaUseCase(FakeAlumnoRepository())
        caso_de_uso.execute(_pedido([AlumnoAImportar(apellido="Perez", nombre="Juan")]))

        resultado = caso_de_uso.execute(
            _pedido([AlumnoAImportar(apellido="PEREZ", nombre="juan"),
                     AlumnoAImportar(apellido="Gomez", nombre="Ana")])
        )

        assert len(resultado.registrados) == 1
        assert resultado.omitidos_por_duplicado == ["PEREZ, juan"]

    def test_rechaza_grado_invalido(self) -> None:
        with pytest.raises(DatosInvalidosError):
            ImportarNominaUseCase(FakeAlumnoRepository()).execute(
                _pedido([AlumnoAImportar(apellido="Perez", nombre="Juan")], anio="9°")
            )

    def test_no_guarda_nada_si_un_nombre_esta_en_blanco(self) -> None:
        repo = FakeAlumnoRepository()
        with pytest.raises(DatosInvalidosError):
            ImportarNominaUseCase(repo).execute(
                _pedido([AlumnoAImportar(apellido="Perez", nombre="Juan"),
                         AlumnoAImportar(apellido="Gomez", nombre="   ")])
            )
        assert repo.listar_todos() == []
