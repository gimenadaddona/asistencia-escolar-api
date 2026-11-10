from typing import Any, Dict, Iterator, List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.infrastructure.fastapi.dependencies import get_session
from src.infrastructure.sqlalchemy.models import orm_models
from src.main import create_app

JUAN = {"nombre": "Juan", "apellido": "Perez", "ciclo": "1", "anio": "2°", "division": "A"}


@pytest.fixture
def cliente() -> Iterator[TestClient]:
    motor = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    orm_models.Base.metadata.create_all(motor)
    fabrica = sessionmaker(bind=motor, autoflush=False, expire_on_commit=False)

    def sesion_de_prueba() -> Iterator[Session]:
        with fabrica() as sesion:
            yield sesion

    app = create_app()
    app.dependency_overrides[get_session] = sesion_de_prueba
    with TestClient(app) as cliente_http:
        yield cliente_http


def planilla(registros: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"anio": "2°", "division": "A", "fecha": "2026-10-23", "registros": registros}


def test_la_pantalla_de_pasar_lista_se_sirve(cliente: TestClient) -> None:
    respuesta = cliente.get("/")

    assert respuesta.status_code == 200
    assert "Pasar lista" in respuesta.text


def test_flujo_completo_hasta_el_reporte_de_seguimiento(cliente: TestClient) -> None:
    id_juan = cliente.post("/api/v1/alumnos", json=JUAN).json()["id"]
    nomina = cliente.get("/api/v1/alumnos", params={"anio": "2°", "division": "A"}).json()
    assert nomina["total"] == 1

    guardado = cliente.post(
        "/api/v1/asistencia",
        json=planilla([{"alumno_id": id_juan, "presente": False, "motivo_inasistencia": "injustificado"}]),
    )
    assert guardado.status_code == 201
    alertas = cliente.get("/api/v1/reportes/alertas", params={"limite": 1}).json()
    assert alertas["total_alumnos_en_alerta"] == 1

    accion = cliente.post(
        "/api/v1/acciones",
        json={
            "alumno_id": id_juan,
            "tipo_accion": "llamado_familia",
            "descripcion": "Se llamo a la madre",
            "realizado_por": "Docente de prueba",
            "rol_autor": "docente",
        },
    )
    assert accion.status_code == 201
    seguimiento = cliente.get("/api/v1/reportes/seguimiento", params={"limite": 1}).json()
    assert len(seguimiento["alumnos_en_seguimiento"][0]["acciones"]) == 1


def test_rechaza_datos_invalidos_y_pasar_lista_dos_veces(cliente: TestClient) -> None:
    invalida = cliente.post(
        "/api/v1/asistencia",
        json={
            "anio": "string",
            "division": "string",
            "fecha": "2026-10-23",
            "registros": [{"alumno_id": 0, "presente": False, "motivo_inasistencia": "climatico"}],
        },
    )
    assert invalida.status_code == 400

    id_juan = cliente.post("/api/v1/alumnos", json=JUAN).json()["id"]
    datos = planilla([{"alumno_id": id_juan, "presente": True, "motivo_inasistencia": None}])
    assert cliente.post("/api/v1/asistencia", json=datos).status_code == 201
    assert cliente.post("/api/v1/asistencia", json=datos).status_code == 400
