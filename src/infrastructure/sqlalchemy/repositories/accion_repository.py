from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.asistencia_escolar.entities import AccionSeguimiento
from src.domain.asistencia_escolar.repositories import AccionSeguimientoRepository
from src.domain.asistencia_escolar.value_objects import RolUsuario, TipoAccion
from src.infrastructure.sqlalchemy.models.orm_models import AccionModel


def _a_entidad(modelo: AccionModel) -> AccionSeguimiento:
    return AccionSeguimiento(
        id=modelo.id,
        alumno_id=modelo.alumno_id,
        fecha=modelo.fecha,
        tipo_accion=TipoAccion(modelo.tipo_accion),
        descripcion=modelo.descripcion,
        realizado_por=modelo.realizado_por,
        rol_autor=RolUsuario(modelo.rol_autor),
    )


class SqlAlchemyAccionSeguimientoRepository(AccionSeguimientoRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def guardar(self, accion: AccionSeguimiento) -> AccionSeguimiento:
        modelo = AccionModel(
            alumno_id=accion.alumno_id,
            fecha=accion.fecha,
            tipo_accion=accion.tipo_accion.valor,
            descripcion=accion.descripcion,
            realizado_por=accion.realizado_por,
            rol_autor=accion.rol_autor.value,
        )
        self._session.add(modelo)
        self._session.commit()
        return _a_entidad(modelo)

    def listar_por_alumno(self, alumno_id: int) -> List[AccionSeguimiento]:
        stmt = (
            select(AccionModel)
            .where(AccionModel.alumno_id == alumno_id)
            .order_by(AccionModel.fecha, AccionModel.id)
        )
        return [_a_entidad(m) for m in self._session.scalars(stmt).all()]
