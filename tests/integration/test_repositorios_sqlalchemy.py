from datetime import date
from typing import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.domain.asistencia_escolar.entities import (
    AccionSeguimiento,
    Alumno,
    RegistroAsistencia,
)
from src.domain.asistencia_escolar.value_objects import (
    AnioEscolar,
    Ciclo,
    Division,
    EstadoAsistencia,
    MotivoInasistencia,
    RolUsuario,
    TipoAccion,
)
from src.infrastructure.sqlalchemy.database import Base
from src.infrastructure.sqlalchemy.models.orm_models import (
    AccionModel,
    AlumnoModel,
    AsistenciaModel,
)
from src.infrastructure.sqlalchemy.repositories.accion_repository import (
    SqlAlchemyAccionSeguimientoRepository,
)
from src.infrastructure.sqlalchemy.repositories.alumno_repository import (
    SqlAlchemyAlumnoRepository,
)
from src.infrastructure.sqlalchemy.repositories.asistencia_repository import (
    SqlAlchemyAsistenciaRepository,
)


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(
        engine,
        tables=[AlumnoModel.__table__, AsistenciaModel.__table__, AccionModel.__table__],
    )
    fabrica = sessionmaker(bind=engine, expire_on_commit=False)
    with fabrica() as s:
        yield s


def _alumno(nombre: str, apellido: str, anio: str = "2°", division: str = "A") -> Alumno:
    ciclo = Ciclo.CICLO_1 if anio in ("1°", "2°", "3°") else Ciclo.CICLO_2
    return Alumno(
        nombre=nombre,
        apellido=apellido,
        ciclo=ciclo,
        anio=AnioEscolar(anio),
        division=Division(division),
    )


class TestRepositoriosSqlAlchemy:
    def test_guarda_y_recupera_un_alumno(self, session: Session) -> None:
        repo = SqlAlchemyAlumnoRepository(session)

        guardado = repo.guardar(_alumno("Juan", "Perez"))
        recuperado = repo.obtener_por_id(guardado.id)

        assert guardado.id is not None
        assert recuperado is not None
        assert recuperado.nombre_completo() == "Perez, Juan"

    def test_lista_por_anio_y_division(self, session: Session) -> None:
        repo = SqlAlchemyAlumnoRepository(session)
        repo.guardar(_alumno("Juan", "Perez", "2°", "A"))
        repo.guardar(_alumno("Ana", "Gomez", "2°", "A"))
        repo.guardar(_alumno("Luis", "Diaz", "5°", "C"))

        resultado = repo.listar_por_anio_division(AnioEscolar("2°"), Division("A"))

        assert len(resultado) == 2
        assert len(repo.listar_todos()) == 3

    def test_cuenta_solo_faltas_injustificadas(self, session: Session) -> None:
        alumno = SqlAlchemyAlumnoRepository(session).guardar(_alumno("Juan", "Perez"))
        repo = SqlAlchemyAsistenciaRepository(session)

        def registrar(dia: int, estado: EstadoAsistencia, motivo: MotivoInasistencia | None) -> None:
            repo.guardar(
                RegistroAsistencia(
                    alumno_id=alumno.id,
                    fecha=date(2026, 9, dia),
                    estado=estado,
                    motivo_inasistencia=motivo,
                )
            )

        registrar(1, EstadoAsistencia.AUSENTE, MotivoInasistencia.INJUSTIFICADO)
        registrar(2, EstadoAsistencia.AUSENTE, MotivoInasistencia.INJUSTIFICADO)
        registrar(3, EstadoAsistencia.AUSENTE, MotivoInasistencia.CLIMATICO)
        registrar(4, EstadoAsistencia.AUSENTE, MotivoInasistencia.JUSTIFICADO)
        registrar(5, EstadoAsistencia.PRESENTE, None)

        assert repo.contar_faltas_injustificadas(alumno.id) == 2
        assert len(repo.listar_por_alumno(alumno.id)) == 5

    def test_detecta_si_ya_existe_asistencia_ese_dia(self, session: Session) -> None:
        alumno = SqlAlchemyAlumnoRepository(session).guardar(_alumno("Juan", "Perez"))
        repo = SqlAlchemyAsistenciaRepository(session)
        repo.guardar(
            RegistroAsistencia(
                alumno_id=alumno.id, fecha=date(2026, 9, 10), estado=EstadoAsistencia.PRESENTE
            )
        )

        assert repo.existe_registro(alumno.id, date(2026, 9, 10)) is True
        assert repo.existe_registro(alumno.id, date(2026, 9, 11)) is False

    def test_guarda_y_lista_acciones_de_un_alumno(self, session: Session) -> None:
        alumno = SqlAlchemyAlumnoRepository(session).guardar(_alumno("Juan", "Perez"))
        repo = SqlAlchemyAccionSeguimientoRepository(session)
        repo.guardar(
            AccionSeguimiento(
                alumno_id=alumno.id,
                fecha=date(2026, 9, 15),
                tipo_accion=TipoAccion("llamado_familia"),
                descripcion="Se llamo a la madre",
                realizado_por="Marta Gomez",
                rol_autor=RolUsuario.DOCENTE,
            )
        )

        acciones = repo.listar_por_alumno(alumno.id)

        assert len(acciones) == 1
        assert acciones[0].realizado_por == "Marta Gomez"
