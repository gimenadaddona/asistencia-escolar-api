from datetime import date, timedelta

from src.application.asistencia_escolar.dtos.accion_dto import RegistrarAccionRequest
from src.application.asistencia_escolar.dtos.asistencia_dto import ReporteAlertasRequest
from src.application.asistencia_escolar.use_cases.generar_reporte_alertas import (
    GenerarReporteAlertasUseCase,
)
from src.application.asistencia_escolar.use_cases.generar_reporte_seguimiento import (
    GenerarReporteSeguimientoUseCase,
)
from src.application.asistencia_escolar.use_cases.registrar_accion_seguimiento import (
    RegistrarAccionSeguimientoUseCase,
)
from src.domain.asistencia_escolar.entities import Alumno, RegistroAsistencia
from src.domain.asistencia_escolar.services import ServicioDeteccionAlertaInasistencia
from src.domain.asistencia_escolar.value_objects import (
    AnioEscolar, Ciclo, Division, EstadoAsistencia, MotivoInasistencia,
)
from tests.unit.fakes import (
    FakeAccionSeguimientoRepository, FakeAlumnoRepository, FakeAsistenciaRepository,
)


class TestGenerarReporteSeguimientoUseCase:
    def test_combina_alerta_con_acciones_ya_tomadas(self) -> None:
        alumno_repo = FakeAlumnoRepository()
        asistencia_repo = FakeAsistenciaRepository()
        accion_repo = FakeAccionSeguimientoRepository()

        alumno = alumno_repo.guardar(
            Alumno(nombre="Juan", apellido="Perez", ciclo=Ciclo.CICLO_1, anio=AnioEscolar("2°"), division=Division("A"))
        )

        for i in range(5):
            asistencia_repo.guardar(RegistroAsistencia(
                alumno_id=alumno.id, fecha=date(2026, 9, 1) + timedelta(days=i),
                estado=EstadoAsistencia.AUSENTE, motivo_inasistencia=MotivoInasistencia.INJUSTIFICADO,
            ))

        registrar_accion = RegistrarAccionSeguimientoUseCase(accion_repository=accion_repo)
        registrar_accion.execute(RegistrarAccionRequest(
            alumno_id=alumno.id, tipo_accion="llamado_familia",
            descripcion="Se llamo a la madre", realizado_por="Marta Gomez", rol_autor="docente",
        ))

        reporte_alertas_uc = GenerarReporteAlertasUseCase(
            alumno_repository=alumno_repo, asistencia_repository=asistencia_repo,
            servicio_alertas=ServicioDeteccionAlertaInasistencia(),
        )
        caso_de_uso = GenerarReporteSeguimientoUseCase(
            reporte_alertas_use_case=reporte_alertas_uc,
            accion_repository=accion_repo, alumno_repository=alumno_repo,
        )

        response = caso_de_uso.execute(ReporteAlertasRequest(limite_faltas_injustificadas=5))

        assert len(response.alumnos_en_seguimiento) == 1
        alumno_seguimiento = response.alumnos_en_seguimiento[0]
        assert alumno_seguimiento.nombre_completo == "Perez, Juan"
        assert alumno_seguimiento.cantidad_faltas_injustificadas == 5
        assert len(alumno_seguimiento.acciones) == 1
        assert alumno_seguimiento.acciones[0]["tipo_accion"] == "llamado_familia"
        assert alumno_seguimiento.acciones[0]["realizado_por"] == "Marta Gomez"

    def test_alumno_en_alerta_sin_acciones_muestra_lista_vacia(self) -> None:
        alumno_repo = FakeAlumnoRepository()
        asistencia_repo = FakeAsistenciaRepository()
        accion_repo = FakeAccionSeguimientoRepository()

        alumno = alumno_repo.guardar(
            Alumno(nombre="Ana", apellido="Gomez", ciclo=Ciclo.CICLO_1, anio=AnioEscolar("2°"), division=Division("A"))
        )
        for i in range(5):
            asistencia_repo.guardar(RegistroAsistencia(
                alumno_id=alumno.id, fecha=date(2026, 9, 1) + timedelta(days=i),
                estado=EstadoAsistencia.AUSENTE, motivo_inasistencia=MotivoInasistencia.INJUSTIFICADO,
            ))

        reporte_alertas_uc = GenerarReporteAlertasUseCase(
            alumno_repository=alumno_repo, asistencia_repository=asistencia_repo,
            servicio_alertas=ServicioDeteccionAlertaInasistencia(),
        )
        caso_de_uso = GenerarReporteSeguimientoUseCase(
            reporte_alertas_use_case=reporte_alertas_uc,
            accion_repository=accion_repo, alumno_repository=alumno_repo,
        )

        response = caso_de_uso.execute(ReporteAlertasRequest(limite_faltas_injustificadas=5))

        assert len(response.alumnos_en_seguimiento) == 1
        assert response.alumnos_en_seguimiento[0].acciones == []

    def test_sin_alertas_no_hay_alumnos_en_seguimiento(self) -> None:
        alumno_repo = FakeAlumnoRepository()
        asistencia_repo = FakeAsistenciaRepository()
        accion_repo = FakeAccionSeguimientoRepository()

        reporte_alertas_uc = GenerarReporteAlertasUseCase(
            alumno_repository=alumno_repo, asistencia_repository=asistencia_repo,
            servicio_alertas=ServicioDeteccionAlertaInasistencia(),
        )
        caso_de_uso = GenerarReporteSeguimientoUseCase(
            reporte_alertas_use_case=reporte_alertas_uc,
            accion_repository=accion_repo, alumno_repository=alumno_repo,
        )

        response = caso_de_uso.execute(ReporteAlertasRequest(limite_faltas_injustificadas=5))

        assert response.alumnos_en_seguimiento == []
