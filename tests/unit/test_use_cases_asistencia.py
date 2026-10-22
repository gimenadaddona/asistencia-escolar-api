from datetime import date

import pytest

from src.application.asistencia_escolar.dtos.asistencia_dto import (
    PasarListaRequest,
    RegistroAsistenciaItem,
)
from src.application.asistencia_escolar.use_cases.pasar_lista_asistencia import (
    PasarListaAsistenciaUseCase,
)
from src.domain.asistencia_escolar.entities import Alumno
from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.domain.asistencia_escolar.value_objects import AnioEscolar, Ciclo, Division
from tests.unit.fakes import FakeAlumnoRepository, FakeAsistenciaRepository

FECHA = date(2026, 9, 29)


def _armar():
    alumnos = FakeAlumnoRepository()
    asistencia = FakeAsistenciaRepository()
    for numero in range(3):
        alumnos.guardar(
            Alumno(
                nombre=f"Alumno{numero}",
                apellido="Prueba",
                ciclo=Ciclo.CICLO_1,
                anio=AnioEscolar("2°"),
                division=Division("A"),
            )
        )
    caso_de_uso = PasarListaAsistenciaUseCase(
        asistencia_repository=asistencia, alumno_repository=alumnos
    )
    return caso_de_uso, asistencia


def _request(registros, anio="2°", division="A"):
    return PasarListaRequest(anio=anio, division=division, fecha=FECHA, registros=registros)


class TestPasarListaAsistenciaUseCase:
    def test_registra_asistencia_de_varios_alumnos(self) -> None:
        caso_de_uso, _ = _armar()

        response = caso_de_uso.execute(
            _request(
                [
                    RegistroAsistenciaItem(alumno_id=1, presente=True),
                    RegistroAsistenciaItem(alumno_id=2, presente=False, motivo_inasistencia="climatico"),
                    RegistroAsistenciaItem(alumno_id=3, presente=False, motivo_inasistencia="injustificado"),
                ]
            )
        )

        assert response.cantidad_registrados == 3
        assert response.fecha == FECHA

    def test_alumno_presente_no_tiene_motivo(self) -> None:
        caso_de_uso, asistencia = _armar()

        caso_de_uso.execute(_request([RegistroAsistenciaItem(alumno_id=1, presente=True)]))

        registros = asistencia.listar_por_alumno(1)
        assert len(registros) == 1
        assert registros[0].motivo_inasistencia is None

    def test_falta_injustificada_cuenta_para_alertas(self) -> None:
        caso_de_uso, asistencia = _armar()

        caso_de_uso.execute(
            _request([RegistroAsistenciaItem(alumno_id=1, presente=False, motivo_inasistencia="injustificado")])
        )

        assert asistencia.contar_faltas_injustificadas(1) == 1

    def test_falta_climatica_no_cuenta_para_alertas(self) -> None:
        caso_de_uso, asistencia = _armar()

        caso_de_uso.execute(
            _request([RegistroAsistenciaItem(alumno_id=1, presente=False, motivo_inasistencia="climatico")])
        )

        assert asistencia.contar_faltas_injustificadas(1) == 0

    def test_rechaza_pasar_lista_dos_veces_el_mismo_dia(self) -> None:
        caso_de_uso, _ = _armar()
        request = _request([RegistroAsistenciaItem(alumno_id=1, presente=True)])
        caso_de_uso.execute(request)

        with pytest.raises(DatosInvalidosError):
            caso_de_uso.execute(request)

    def test_rechaza_alumno_inexistente(self) -> None:
        caso_de_uso, _ = _armar()

        with pytest.raises(DatosInvalidosError):
            caso_de_uso.execute(_request([RegistroAsistenciaItem(alumno_id=999, presente=True)]))

    def test_rechaza_alumno_de_otra_division(self) -> None:
        caso_de_uso, _ = _armar()

        with pytest.raises(DatosInvalidosError):
            caso_de_uso.execute(
                _request([RegistroAsistenciaItem(alumno_id=1, presente=True)], division="B")
            )

    def test_rechaza_anio_invalido(self) -> None:
        caso_de_uso, _ = _armar()

        with pytest.raises(DatosInvalidosError):
            caso_de_uso.execute(
                _request([RegistroAsistenciaItem(alumno_id=1, presente=True)], anio="string")
            )

    def test_rechaza_alumno_repetido_en_la_planilla(self) -> None:
        caso_de_uso, _ = _armar()

        with pytest.raises(DatosInvalidosError):
            caso_de_uso.execute(
                _request(
                    [
                        RegistroAsistenciaItem(alumno_id=1, presente=True),
                        RegistroAsistenciaItem(alumno_id=1, presente=True),
                    ]
                )
            )

    def test_no_guarda_nada_si_un_alumno_de_la_planilla_es_invalido(self) -> None:
        caso_de_uso, asistencia = _armar()

        with pytest.raises(DatosInvalidosError):
            caso_de_uso.execute(
                _request(
                    [
                        RegistroAsistenciaItem(alumno_id=1, presente=True),
                        RegistroAsistenciaItem(alumno_id=999, presente=True),
                    ]
                )
            )

        assert asistencia.listar_por_alumno(1) == []
