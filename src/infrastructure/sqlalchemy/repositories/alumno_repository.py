from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.asistencia_escolar.entities import Alumno
from src.domain.asistencia_escolar.repositories import AlumnoRepository
from src.domain.asistencia_escolar.value_objects import AnioEscolar, Ciclo, Division
from src.infrastructure.sqlalchemy.models.orm_models import AlumnoModel


def _a_entidad(modelo: AlumnoModel) -> Alumno:
    return Alumno(
        id=modelo.id,
        nombre=modelo.nombre,
        apellido=modelo.apellido,
        ciclo=Ciclo(modelo.ciclo),
        anio=AnioEscolar(modelo.anio),
        division=Division(modelo.division),
    )


class SqlAlchemyAlumnoRepository(AlumnoRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def guardar(self, alumno: Alumno) -> Alumno:
        modelo: Optional[AlumnoModel] = None
        if alumno.id is not None:
            modelo = self._session.get(AlumnoModel, alumno.id)
        if modelo is None:
            modelo = AlumnoModel()
            self._session.add(modelo)
        modelo.nombre = alumno.nombre
        modelo.apellido = alumno.apellido
        modelo.ciclo = alumno.ciclo.value
        modelo.anio = alumno.anio.valor
        modelo.division = alumno.division.valor
        self._session.commit()
        return _a_entidad(modelo)

    def obtener_por_id(self, alumno_id: int) -> Optional[Alumno]:
        modelo = self._session.get(AlumnoModel, alumno_id)
        return _a_entidad(modelo) if modelo is not None else None

    def listar_por_anio_division(self, anio: AnioEscolar, division: Division) -> List[Alumno]:
        stmt = (
            select(AlumnoModel)
            .where(AlumnoModel.anio == anio.valor, AlumnoModel.division == division.valor)
            .order_by(AlumnoModel.apellido, AlumnoModel.nombre)
        )
        return [_a_entidad(m) for m in self._session.scalars(stmt).all()]

    def listar_todos(self) -> List[Alumno]:
        stmt = select(AlumnoModel).order_by(
            AlumnoModel.anio, AlumnoModel.division, AlumnoModel.apellido, AlumnoModel.nombre
        )
        return [_a_entidad(m) for m in self._session.scalars(stmt).all()]

    def eliminar(self, alumno_id: int) -> None:
        modelo = self._session.get(AlumnoModel, alumno_id)
        if modelo is not None:
            self._session.delete(modelo)
            self._session.commit()
