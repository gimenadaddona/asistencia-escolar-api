from datetime import date

import pytest

from src.application.asistencia_escolar.dtos.asistencia_dto import (
    PasarListaRequest,
    RegistroAsistenciaItem,
)
from src.application.asistencia_escolar.use_cases.pasar_lista_asistencia import (
    PasarListaAsistenciaUseCase,
)
from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from tests.unit.fakes import FakeAsistenciaRepository


class TestPasarListaAsistenciaUseCase:
    def test_registra_asistencia_de_varios_alumnos(self) -> None:
        repositorio = FakeAsistenciaRepository()
        caso_de_uso = PasarListaAsistenciaUseCase(asistencia_repository=repositorio)

        request = PasarListaRequest(
            anio="2°",
            division="A",
            fecha=date(2026, 9, 29),
            registros=[
                RegistroAsistenciaItem(alumno_id=1, presente=True),
                RegistroAsistenciaItem(alumno_id=2, presente=False, motivo_inasistencia="climatico"),
                RegistroAsistenciaItem(alumno_id=3, presente=False, motivo_inasistencia="injustificado"),
            ],
        )

        response = caso_de_uso.execute(request)

        assert response.cantidad_registrados == 3
        assert response.fecha == date(2026, 9, 29)

    def test_alumno_presente_no_tiene_motivo(self) -> None:
        repositorio = FakeAsistenciaRepository()
        caso_de_uso = PasarListaAsistenciaUseCase(asistencia_repository=repositorio)

        request = PasarListaRequest(
            anio="2°", division="A", fecha=date(2026, 9, 29),
            registros=[RegistroAsistenciaItem(alumno_id=1, presente=True)],
        )
        caso_de_uso.execute(request)

        registros = repositorio.listar_por_alumno(1)
        assert len(registros) == 1
        assert registros[0].motivo_inasistencia is None

    def test_falta_injustificada_cuenta_para_alertas(self) -> None:
        repositorio = FakeAsistenciaRepository()
        caso_de_uso = PasarListaAsistenciaUseCase(asistencia_repository=repositorio)

        request = PasarListaRequest(
            anio="2°", division="A", fecha=date(2026, 9, 29),
            registros=[
                RegistroAsistenciaItem(alumno_id=1, presente=False, motivo_inasistencia="injustificado"),
            ],
        )
        caso_de_uso.execute(request)

        assert repositorio.contar_faltas_injustificadas(1) == 1

    def test_falta_climatica_no_cuenta_para_alertas(self) -> None:
        repositorio = FakeAsistenciaRepository()
        caso_de_uso = PasarListaAsistenciaUseCase(asistencia_repository=repositorio)

        request = PasarListaRequest(
            anio="2°", division="A", fecha=date(2026, 9, 29),
            registros=[
                RegistroAsistenciaItem(alumno_id=1, presente=False, motivo_inasistencia="climatico"),
            ],
        )
        caso_de_uso.execute(request)

        assert repositorio.contar_faltas_injustificadas(1) == 0

    def test_rechaza_pasar_lista_dos_veces_el_mismo_dia(self) -> None:
        repositorio = FakeAsistenciaRepository()
        caso_de_uso = PasarListaAsistenciaUseCase(asistencia_repository=repositorio)

        request = PasarListaRequest(
            anio="2°", division="A", fecha=date(2026, 9, 29),
            registros=[RegistroAsistenciaItem(alumno_id=1, presente=True)],
        )
        caso_de_uso.execute(request)

        with pytest.raises(DatosInvalidosError):
            caso_de_uso.execute(request)
            