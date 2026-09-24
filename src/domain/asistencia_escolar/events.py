from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class AlertaInasistenciaGenerada:
    alumno_id: int
    nombre_completo: str
    cantidad_faltas_injustificadas: int
    limite_configurado: int
    generado_en: datetime = field(default_factory=datetime.now)
