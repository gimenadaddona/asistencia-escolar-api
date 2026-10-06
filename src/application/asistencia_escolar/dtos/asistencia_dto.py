from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class RegistroAsistenciaItem(BaseModel):
    """Un registro individual dentro de una planilla de asistencia."""
    alumno_id: int
    presente: bool
    motivo_inasistencia: Optional[str] = None


class PasarListaRequest(BaseModel):
    """Datos para pasar lista a una división completa en una fecha."""
    anio: str
    division: str
    fecha: date
    registros: List[RegistroAsistenciaItem] = Field(min_length=1)


class PasarListaResponse(BaseModel):
    """Confirmación de que se registró la asistencia."""
    fecha: date
    anio: str
    division: str
    cantidad_registrados: int


class ReporteAlertasRequest(BaseModel):
    """Parámetro para generar el reporte de alertas."""
    limite_faltas_injustificadas: int = Field(gt=0)


class AlertaAlumnoResponse(BaseModel):
    """Un alumno en situación de alerta."""
    alumno_id: int
    nombre_completo: str
    cantidad_faltas_injustificadas: int


class ReporteAlertasResponse(BaseModel):
    """Listado completo de alumnos en alerta."""
    limite_configurado: int
    alertas: List[AlertaAlumnoResponse]
    total_alumnos_en_alerta: int
    

class AlumnoEnSeguimientoResponse(BaseModel):
    """Un alumno en alerta, junto con todo lo que ya se hizo por el."""
    alumno_id: int
    nombre_completo: str
    anio: str
    division: str
    cantidad_faltas_injustificadas: int
    acciones: List[dict]


class ReporteSeguimientoResponse(BaseModel):
    """Reporte completo para directivo y orientacion: alertas + acciones ya tomadas."""
    limite_configurado: int
    alumnos_en_seguimiento: List[AlumnoEnSeguimientoResponse]
