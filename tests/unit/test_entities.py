from datetime import date

import pytest

from src.domain.asistencia_escolar.entities import (
    AccionSeguimiento,
    Alumno,
    RegistroAsistencia,
)
from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.domain.asistencia_escolar.value_objects import (
    AnioEscolar,
    Ciclo,
    Division,
    EstadoAsistencia,
    MotivoInasistencia,
    RolUsuario,
    TipoAccion,
)


def crear_alumno_valido() -> Alumno:
    return Alumno(
        nombre="Juan",
        apellido="Perez",
        ciclo=Ciclo.CICLO_1,
        anio=AnioEscolar("2°"),
        division=Division("A"),
    )


class TestAlumno:
    def test_crea_alumno_valido(self) -> None:
        alumno = crear_alumno_valido()
        assert alumno.nombre_completo() == "Perez, Juan"

    def test_rechaza_nombre_vacio(self) -> None:
        with pytest.raises(DatosInvalidosError):
            Alumno(nombre="   ", apellido="Perez", ciclo=Ciclo.CICLO_1, anio=AnioEscolar("2°"), division=Division("A"))

    def test_rechaza_apellido_vacio(self) -> None:
        with pytest.raises(DatosInvalidosError):
            Alumno(nombre="Juan", apellido="", ciclo=Ciclo.CICLO_1, anio=AnioEscolar("2°"), division=Division("A"))

    def test_rechaza_anio_que_no_corresponde_al_ciclo(self) -> None:
        with pytest.raises(DatosInvalidosError):
            Alumno(nombre="Juan", apellido="Perez", ciclo=Ciclo.CICLO_1, anio=AnioEscolar("5°"), division=Division("A"))


class TestRegistroAsistencia:
    def test_presente_es_valido(self) -> None:
        registro = RegistroAsistencia(alumno_id=1, fecha=date(2026, 9, 3), estado=EstadoAsistencia.PRESENTE)
        assert registro.es_falta_injustificada() is False

    def test_ausente_injustificado_cuenta_para_alerta(self) -> None:
        registro = RegistroAsistencia(
            alumno_id=1, fecha=date(2026, 9, 3), estado=EstadoAsistencia.AUSENTE,
            motivo_inasistencia=MotivoInasistencia.INJUSTIFICADO,
        )
        assert registro.es_falta_injustificada() is True

    def test_ausente_climatico_no_cuenta_para_alerta(self) -> None:
        registro = RegistroAsistencia(
            alumno_id=1, fecha=date(2026, 9, 3), estado=EstadoAsistencia.AUSENTE,
            motivo_inasistencia=MotivoInasistencia.CLIMATICO,
        )
        assert registro.es_falta_injustificada() is False

    def test_ausente_justificado_no_cuenta_para_alerta(self) -> None:
        registro = RegistroAsistencia(
            alumno_id=1, fecha=date(2026, 9, 3), estado=EstadoAsistencia.AUSENTE,
            motivo_inasistencia=MotivoInasistencia.JUSTIFICADO,
        )
        assert registro.es_falta_injustificada() is False

    def test_rechaza_presente_con_motivo(self) -> None:
        with pytest.raises(DatosInvalidosError):
            RegistroAsistencia(
                alumno_id=1, fecha=date(2026, 9, 3), estado=EstadoAsistencia.PRESENTE,
                motivo_inasistencia=MotivoInasistencia.JUSTIFICADO,
            )

    def test_rechaza_ausente_sin_motivo(self) -> None:
        with pytest.raises(DatosInvalidosError):
            RegistroAsistencia(alumno_id=1, fecha=date(2026, 9, 3), estado=EstadoAsistencia.AUSENTE)


class TestAccionSeguimiento:
    def test_crea_accion_valida(self) -> None:
        accion = AccionSeguimiento(
            alumno_id=1,
            fecha=date(2026, 9, 3),
            tipo_accion=TipoAccion("llamado_familia"),
            descripcion="Se llamo a la madre, no atendio",
            realizado_por="Marta Gomez",
            rol_autor=RolUsuario.DOCENTE,
        )
        assert accion.realizado_por == "Marta Gomez"

    def test_rechaza_descripcion_vacia(self) -> None:
        with pytest.raises(DatosInvalidosError):
            AccionSeguimiento(
                alumno_id=1, fecha=date(2026, 9, 3), tipo_accion=TipoAccion("llamado_familia"),
                descripcion="   ", realizado_por="Marta Gomez", rol_autor=RolUsuario.DOCENTE,
            )

    def test_rechaza_realizado_por_vacio(self) -> None:
        with pytest.raises(DatosInvalidosError):
            AccionSeguimiento(
                alumno_id=1, fecha=date(2026, 9, 3), tipo_accion=TipoAccion("llamado_familia"),
                descripcion="Se llamo a la madre", realizado_por="", rol_autor=RolUsuario.DOCENTE,
            )
            