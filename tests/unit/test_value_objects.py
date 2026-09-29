import pytest

from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.domain.asistencia_escolar.value_objects import (
    AnioEscolar,
    Ciclo,
    Division,
    TipoAccion,
)


class TestAnioEscolar:
    def test_crea_anio_valido(self) -> None:
        anio = AnioEscolar("3°")
        assert anio.valor == "3°"

    def test_rechaza_anio_invalido(self) -> None:
        with pytest.raises(DatosInvalidosError):
            AnioEscolar("7°")

    def test_pertenece_a_ciclo_1(self) -> None:
        anio = AnioEscolar("2°")
        assert anio.pertenece_a_ciclo(Ciclo.CICLO_1) is True
        assert anio.pertenece_a_ciclo(Ciclo.CICLO_2) is False

    def test_pertenece_a_ciclo_2(self) -> None:
        anio = AnioEscolar("5°")
        assert anio.pertenece_a_ciclo(Ciclo.CICLO_2) is True
        assert anio.pertenece_a_ciclo(Ciclo.CICLO_1) is False


class TestDivision:
    def test_crea_division_valida(self) -> None:
        division = Division("A")
        assert division.valor == "A"

    def test_rechaza_division_invalida(self) -> None:
        with pytest.raises(DatosInvalidosError):
            Division("Z")


class TestDivisionTurno:
    def test_division_a_es_turno_manana(self) -> None:
        assert Division("A").obtener_turno() == "mañana"

    def test_division_b_es_turno_manana(self) -> None:
        assert Division("B").obtener_turno() == "mañana"

    def test_division_c_es_turno_tarde(self) -> None:
        assert Division("C").obtener_turno() == "tarde"

    def test_division_d_es_turno_tarde(self) -> None:
        assert Division("D").obtener_turno() == "tarde"


class TestTipoAccion:
    def test_crea_tipo_valido(self) -> None:
        tipo = TipoAccion("llamado_familia")
        assert tipo.valor == "llamado_familia"

    def test_rechaza_tipo_invalido(self) -> None:
        with pytest.raises(DatosInvalidosError):
            TipoAccion("mandarle_una_carta")
