from typing import List, Optional

from src.domain.asistencia_escolar.entities import Alumno
from src.domain.asistencia_escolar.events import AlertaInasistenciaGenerada


class ServicioDeteccionAlertaInasistencia:
    def evaluar(
        self,
        alumno: Alumno,
        cantidad_faltas_injustificadas: int,
        limite: int,
    ) -> Optional[AlertaInasistenciaGenerada]:
        if cantidad_faltas_injustificadas < limite:
            return None

        return AlertaInasistenciaGenerada(
            alumno_id=alumno.id if alumno.id is not None else 0,
            nombre_completo=alumno.nombre_completo(),
            cantidad_faltas_injustificadas=cantidad_faltas_injustificadas,
            limite_configurado=limite,
        )

    def evaluar_lote(
        self,
        alumnos_con_faltas: List[tuple[Alumno, int]],
        limite: int,
    ) -> List[AlertaInasistenciaGenerada]:
        alertas: List[AlertaInasistenciaGenerada] = []
        for alumno, faltas in alumnos_con_faltas:
            alerta = self.evaluar(alumno, faltas, limite)
            if alerta is not None:
                alertas.append(alerta)
        return alertas
