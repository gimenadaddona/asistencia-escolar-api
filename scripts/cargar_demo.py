"""Carga alumnos de ejemplo (inventados) para probar la pantalla de pasar lista."""

from src.application.asistencia_escolar.dtos.alumno_dto import RegistrarAlumnoRequest
from src.application.asistencia_escolar.use_cases.registrar_alumno import RegistrarAlumnoUseCase
from src.infrastructure.sqlalchemy.database import SessionLocal, engine
from src.infrastructure.sqlalchemy.models import orm_models
from src.infrastructure.sqlalchemy.repositories.alumno_repository import SqlAlchemyAlumnoRepository

NOMBRES = ["Sofía", "Mateo", "Valentina", "Joaquín", "Camila"]
APELLIDOS = ["Álvarez", "Benítez", "Cabrera", "Domínguez", "Esquivel"]
CURSOS = [("2°", "A"), ("2°", "C"), ("5°", "B")]


def main() -> None:
    orm_models.Base.metadata.create_all(engine)
    with SessionLocal() as sesion:
        repositorio = SqlAlchemyAlumnoRepository(sesion)
        if repositorio.listar_todos():
            print("Ya hay alumnos cargados: no se agrega nada.")
            return
        caso_de_uso = RegistrarAlumnoUseCase(alumno_repository=repositorio)
        for anio, division in CURSOS:
            ciclo = "1" if anio in ("1°", "2°", "3°") else "2"
            for nombre, apellido in zip(NOMBRES, APELLIDOS):
                caso_de_uso.execute(
                    RegistrarAlumnoRequest(
                        nombre=nombre, apellido=apellido, ciclo=ciclo, anio=anio, division=division
                    )
                )
    print("Alumnos de ejemplo cargados.")


if __name__ == "__main__":
    main()
