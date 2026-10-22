from datetime import date
from typing import Optional

from sqlalchemy import Date, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlalchemy.database import Base


class AlumnoModel(Base):
    __tablename__ = "alumnos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100))
    apellido: Mapped[str] = mapped_column(String(100))
    ciclo: Mapped[str] = mapped_column(String(1))
    anio: Mapped[str] = mapped_column(String(5))
    division: Mapped[str] = mapped_column(String(1))


class AsistenciaModel(Base):
    __tablename__ = "asistencias"
    __table_args__ = (UniqueConstraint("alumno_id", "fecha"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumnos.id"))
    fecha: Mapped[date] = mapped_column(Date)
    estado: Mapped[str] = mapped_column(String(10))
    motivo_inasistencia: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)


class AccionModel(Base):
    __tablename__ = "acciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumnos.id"))
    fecha: Mapped[date] = mapped_column(Date)
    tipo_accion: Mapped[str] = mapped_column(String(50))
    descripcion: Mapped[str] = mapped_column(Text)
    realizado_por: Mapped[str] = mapped_column(String(100))
    rol_autor: Mapped[str] = mapped_column(String(20))
