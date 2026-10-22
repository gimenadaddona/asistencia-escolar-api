from datetime import date
from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.domain.asistencia_escolar.entities import RegistroAsistencia
from src.domain.asistencia_escolar.repositories import AsistenciaRepository
from src.domain.asistencia_escolar.value_objects import EstadoAsistencia, MotivoInasistencia
from src.infrastructure.sqlalchemy.models.orm_models import AsistenciaModel


def _a_entidad(modelo: AsistenciaModel) -> RegistroAsistencia:
    motivo = (
        MotivoInasistencia(modelo.motivo_inasistencia)
        if modelo.motivo_inasistencia
        else None
    )
    return RegistroAsistencia(
        id=modelo.id,
        alumno_id=modelo.alumno_id,
        fecha=modelo.fecha,
        estado=EstadoAsistencia(modelo.estado),
        motivo_inasistencia=motivo,
    )


class SqlAlchemyAsistenciaRepository(AsistenciaRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def guardar(self, registro: RegistroAsistencia) -> RegistroAsistencia:
        modelo = AsistenciaModel(
            alumno_id=registro.alumno_id,
            fecha=registro.fecha,
            estado=registro.estado.value,
            motivo_inasistencia=(
                registro.motivo_inasistencia.value
                if registro.motivo_inasistencia is not None
                else None
            ),
        )
        self._session.add(modelo)
        self._session.commit()
        return _a_entidad(modelo)

    def listar_por_alumno(self, alumno_id: int) -> List[RegistroAsistencia]:
        stmt = (
            select(AsistenciaModel)
            .where(AsistenciaModel.alumno_id == alumno_id)
            .order_by(AsistenciaModel.fecha)
        )
        return [_a_entidad(m) for m in self._session.scalars(stmt).all()]

    def contar_faltas_injustificadas(self, alumno_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(AsistenciaModel)
            .where(
                AsistenciaModel.alumno_id == alumno_id,
                AsistenciaModel.estado == EstadoAsistencia.AUSENTE.value,
                AsistenciaModel.motivo_inasistencia == MotivoInasistencia.INJUSTIFICADO.value,
            )
        )
        return int(self._session.scalar(stmt) or 0)

    def existe_registro(self, alumno_id: int, fecha: date) -> bool:
        stmt = (
            select(AsistenciaModel.id)
            .where(AsistenciaModel.alumno_id == alumno_id, AsistenciaModel.fecha == fecha)
            .limit(1)
        )
        return self._session.scalar(stmt) is not None
