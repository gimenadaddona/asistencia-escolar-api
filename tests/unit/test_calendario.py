from datetime import date

import pytest

from src.domain.asistencia_escolar.calendario import (
    DiaNoLectivo,
    TipoDiaNoLectivo,
    Trimestre,
)
from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.domain.asistencia_escolar.servicio_calendario import ServicioCalendarioEscolar

SERVICIO = ServicioCalendarioEscolar()


class TestTrimestre:
    def test_meses_de_cada_trimestre(self) -> None:
        assert Trimestre.PRIMERO.meses() == (3, 4, 5)
        assert Trimestre.SEGUNDO.meses() == (6, 7, 8)
        assert Trimestre.TERCERO.meses() == (9, 10, 11, 12)

    def test_trimestre_de_un_mes(self) -> None:
        assert Trimestre.de_mes(4) == Trimestre.PRIMERO
        assert Trimestre.de_mes(6) == Trimestre.SEGUNDO
        assert Trimestre.de_mes(12) == Trimestre.TERCERO

    def test_enero_y_febrero_no_pertenecen_a_ningun_trimestre(self) -> None:
        assert Trimestre.de_mes(1) is None
        assert Trimestre.de_mes(2) is None


class TestDiasHabiles:
    def test_septiembre_2026_tiene_22_dias_habiles(self) -> None:
        assert SERVICIO.dias_habiles_del_mes(2026, 9, set()) == 22

    def test_descuenta_los_dias_no_lectivos(self) -> None:
        no_lectivos = {date(2026, 10, 12), date(2026, 10, 13)}
        assert SERVICIO.dias_habiles_del_mes(2026, 10, no_lectivos) == 20

    def test_un_dia_no_lectivo_en_fin_de_semana_no_descuenta(self) -> None:
        assert SERVICIO.dias_habiles_del_mes(2026, 10, {date(2026, 10, 10)}) == 22

    def test_tercer_trimestre_2026(self) -> None:
        assert SERVICIO.dias_habiles_del_trimestre(2026, Trimestre.TERCERO, set()) == 88

    def test_tercer_trimestre_descuenta_dias_no_lectivos(self) -> None:
        no_lectivos = {date(2026, 10, 12)}
        assert SERVICIO.dias_habiles_del_trimestre(2026, Trimestre.TERCERO, no_lectivos) == 87

    def test_rechaza_meses_fuera_del_ciclo_lectivo(self) -> None:
        with pytest.raises(DatosInvalidosError):
            SERVICIO.dias_habiles_del_mes(2026, 1, set())

    def test_suma_de_los_meses_lectivos_2026(self) -> None:
        assert sum(SERVICIO.dias_habiles_por_mes(2026, set()).values()) == 219


class TestRangos:
    def test_ignora_sabados_y_domingos(self) -> None:
        fechas = SERVICIO.dias_de_semana_entre(date(2026, 10, 10), date(2026, 10, 18))
        assert len(fechas) == 5
        assert fechas[0] == date(2026, 10, 12)
        assert fechas[-1] == date(2026, 10, 16)

    def test_rechaza_fecha_final_anterior_a_la_inicial(self) -> None:
        with pytest.raises(DatosInvalidosError):
            SERVICIO.dias_de_semana_entre(date(2026, 10, 15), date(2026, 10, 14))

    def test_rechaza_rangos_demasiado_largos(self) -> None:
        with pytest.raises(DatosInvalidosError):
            SERVICIO.dias_de_semana_entre(date(2026, 1, 1), date(2028, 1, 1))


class TestDiaNoLectivo:
    def test_rechaza_descripcion_vacia(self) -> None:
        with pytest.raises(DatosInvalidosError):
            DiaNoLectivo(fecha=date(2026, 10, 12), tipo=TipoDiaNoLectivo.FERIADO, descripcion="  ")
