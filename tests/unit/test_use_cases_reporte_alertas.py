from src.application.asistencia_escolar.dtos.asistencia_dto import ReporteAlertasRequest
from src.application.asistencia_escolar.use_cases.generar_reporte_alertas import (
    GenerarReporteAlertasUseCase,
)
from src.domain.asistencia_escolar.entities import Alumno
from src.domain.asistencia_escolar.services import ServicioDeteccionAlertaInasistencia
from src.domain.asistencia_escolar.value_objects import AnioEscolar, Ciclo, Division
from tests.unit.fakes import FakeAlumnoRepository, FakeAsistenciaRepository


def _crear_alumno(repo: FakeAlumnoRepository, nombre: str, apellido: str) -> Alumno:
    alumno = Alumno(
        nombre=nombre, apellido=apellido, ciclo=Ciclo.CICLO_1,
        anio=AnioEscolar("2°"), division=Division("A"),
    )
    return repo.guardar(alumno)


class TestGenerarReporteAlertasUseCase:
    def test_no_hay_alertas_cuando_nadie_supera_el_limite(self) -> None:
        alumno_repo = FakeAlumnoRepository()
        asistencia_repo = FakeAsistenciaRepository()
        _crear_alumno(alumno_repo, "Juan", "Perez")
        caso_de_uso = GenerarReporteAlertasUseCase(
            alumno_repository=alumno_repo,
            asistencia_repository=asistencia_repo,
            servicio_alertas=ServicioDeteccionAlertaInasistencia(),
        )

        response = caso_de_uso.execute(ReporteAlertasRequest(limite_faltas_injustificadas=5))

        assert response.total_alumnos_en_alerta == 0

    def test_detecta_alumno_que_supera_el_limite(self) -> None:
        alumno_repo = FakeAlumnoRepository()
        asistencia_repo = FakeAsistenciaRepository()
        alumno = _crear_alumno(alumno_repo, "Juan", "Perez")

        from datetime import date, timedelta
        from src.domain.asistencia_escolar.entities import RegistroAsistencia
        from src.domain.asistencia_escolar.value_objects import EstadoAsistencia, MotivoInasistencia

        for i in range(5):
            asistencia_repo.guardar(RegistroAsistencia(
                alumno_id=alumno.id, fecha=date(2026, 9, 1) + timedelta(days=i),
                estado=EstadoAsistencia.AUSENTE, motivo_inasistencia=MotivoInasistencia.INJUSTIFICADO,
            ))

        caso_de_uso = GenerarReporteAlertasUseCase(
            alumno_repository=alumno_repo,
            asistencia_repository=asistencia_repo,
            servicio_alertas=ServicioDeteccionAlertaInasistencia(),
        )

        response = caso_de_uso.execute(ReporteAlertasRequest(limite_faltas_injustificadas=5))

        assert response.total_alumnos_en_alerta == 1
        assert response.alertas[0].nombre_completo == "Perez, Juan"
        assert response.alertas[0].cantidad_faltas_injustificadas == 5

    def test_faltas_climaticas_no_generan_alerta(self) -> None:
        alumno_repo = FakeAlumnoRepository()
        asistencia_repo = FakeAsistenciaRepository()
        alumno = _crear_alumno(alumno_repo, "Ana", "Gomez")

        from datetime import date, timedelta
        from src.domain.asistencia_escolar.entities import RegistroAsistencia
        from src.domain.asistencia_escolar.value_objects import EstadoAsistencia, MotivoInasistencia

        for i in range(5):
            asistencia_repo.guardar(RegistroAsistencia(
                alumno_id=alumno.id, fecha=date(2026, 9, 1) + timedelta(days=i),
                estado=EstadoAsistencia.AUSENTE, motivo_inasistencia=MotivoInasistencia.CLIMATICO,
            ))

        caso_de_uso = GenerarReporteAlertasUseCase(
            alumno_repository=alumno_repo,
            asistencia_repository=asistencia_repo,
            servicio_alertas=ServicioDeteccionAlertaInasistencia(),
        )

        response = caso_de_uso.execute(ReporteAlertasRequest(limite_faltas_injustificadas=5))

        assert response.total_alumnos_en_alerta == 0
