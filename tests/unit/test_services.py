from src.domain.asistencia_escolar.entities import Alumno
from src.domain.asistencia_escolar.services import ServicioDeteccionAlertaInasistencia
from src.domain.asistencia_escolar.value_objects import AnioEscolar, Ciclo, Division


def crear_alumno(id_: int = 1) -> Alumno:
    return Alumno(
        id=id_,
        nombre="Juan",
        apellido="Perez",
        ciclo=Ciclo.CICLO_1,
        anio=AnioEscolar("2°"),
        division=Division("A"),
    )


class TestServicioDeteccionAlertaInasistencia:
    def test_no_genera_alerta_por_debajo_del_limite(self) -> None:
        servicio = ServicioDeteccionAlertaInasistencia()
        alumno = crear_alumno()
        resultado = servicio.evaluar(alumno, cantidad_faltas_injustificadas=3, limite=5)
        assert resultado is None

    def test_genera_alerta_al_alcanzar_el_limite(self) -> None:
        servicio = ServicioDeteccionAlertaInasistencia()
        alumno = crear_alumno()
        resultado = servicio.evaluar(alumno, cantidad_faltas_injustificadas=5, limite=5)
        assert resultado is not None
        assert resultado.alumno_id == 1
        assert resultado.nombre_completo == "Perez, Juan"
        assert resultado.cantidad_faltas_injustificadas == 5

    def test_genera_alerta_por_encima_del_limite(self) -> None:
        servicio = ServicioDeteccionAlertaInasistencia()
        alumno = crear_alumno()
        resultado = servicio.evaluar(alumno, cantidad_faltas_injustificadas=8, limite=5)
        assert resultado is not None

    def test_evaluar_lote_filtra_solo_los_que_superan_el_limite(self) -> None:
        servicio = ServicioDeteccionAlertaInasistencia()
        alumno_1 = crear_alumno(id_=1)
        alumno_2 = crear_alumno(id_=2)
        alertas = servicio.evaluar_lote(alumnos_con_faltas=[(alumno_1, 2), (alumno_2, 6)], limite=5)
        assert len(alertas) == 1
        assert alertas[0].alumno_id == 2
