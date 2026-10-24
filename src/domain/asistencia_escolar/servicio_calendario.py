from calendar import monthrange
from datetime import date, timedelta
from typing import Dict, List, Set

from src.domain.asistencia_escolar.calendario import Trimestre
from src.domain.asistencia_escolar.exceptions import DatosInvalidosError

MESES_LECTIVOS = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
MAXIMO_DIAS_POR_RANGO = 366


class ServicioCalendarioEscolar:
    """Calcula dias habiles: lunes a viernes que no estan registrados como no lectivos."""

    def es_dia_de_clase(self, fecha: date, dias_no_lectivos: Set[date]) -> bool:
        return fecha.weekday() < 5 and fecha not in dias_no_lectivos

    def dias_habiles_del_mes(
        self, ciclo_lectivo: int, mes: int, dias_no_lectivos: Set[date]
    ) -> int:
        if mes not in MESES_LECTIVOS:
            raise DatosInvalidosError(
                f"El mes {mes} no pertenece al ciclo lectivo (marzo a diciembre)"
            )
        ultimo_dia = monthrange(ciclo_lectivo, mes)[1]
        return sum(
            1
            for dia in range(1, ultimo_dia + 1)
            if self.es_dia_de_clase(date(ciclo_lectivo, mes, dia), dias_no_lectivos)
        )

    def dias_habiles_por_mes(
        self, ciclo_lectivo: int, dias_no_lectivos: Set[date]
    ) -> Dict[int, int]:
        return {
            mes: self.dias_habiles_del_mes(ciclo_lectivo, mes, dias_no_lectivos)
            for mes in MESES_LECTIVOS
        }

    def dias_habiles_del_trimestre(
        self, ciclo_lectivo: int, trimestre: Trimestre, dias_no_lectivos: Set[date]
    ) -> int:
        return sum(
            self.dias_habiles_del_mes(ciclo_lectivo, mes, dias_no_lectivos)
            for mes in trimestre.meses()
        )

    def dias_de_semana_entre(self, desde: date, hasta: date) -> List[date]:
        if hasta < desde:
            raise DatosInvalidosError("La fecha final no puede ser anterior a la fecha inicial")
        cantidad = (hasta - desde).days + 1
        if cantidad > MAXIMO_DIAS_POR_RANGO:
            raise DatosInvalidosError(f"El rango no puede superar {MAXIMO_DIAS_POR_RANGO} dias")
        fechas = (desde + timedelta(days=n) for n in range(cantidad))
        return [fecha for fecha in fechas if fecha.weekday() < 5]
