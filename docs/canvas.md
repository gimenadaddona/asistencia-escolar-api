# Canvas del proyecto: Sistema de Asistencia Escolar

> Validado con docentes en el issue #9. Los datos marcados [medir] se completan en la prueba piloto.

## Problema

- En la escuela primaria pública la asistencia se registra en papel, y a fin de mes la docente calcula a mano el porcentaje de asistencia e inasistencia para volcarlo en las planillas formales.
- Al cierre de cada trimestre vuelve a sumar las inasistencias y los días hábiles para el boletín.
- La inasistencia reiterada se detecta tarde, y lo que hace cada docente con las familias (llamados, reuniones, notas) no queda visible para orientación y dirección.
- Alternativas actuales: papel y planillas propias. A consultar con la inspección: si existe un sistema oficial.

## Solución

Una aplicación web que se usa desde el celular o la tablet, dentro de la red de la escuela:

- Pasar lista con pocos toques: todos figuran presentes, se marca solo a quien falta y el motivo (climático, justificado o injustificado).
- Alertas de alumnos con faltas injustificadas reiteradas.
- Registro de las acciones del docente, visible para orientación y dirección.
- Reporte de seguimiento: cada alumno en alerta junto con lo que ya se hizo.
- Próximo: calendario con días hábiles y reportes mensual y trimestral con porcentajes, para las planillas y el boletín.

## Métricas clave

| Métrica | Hoy | Objetivo |
|---|---|---|
| Tiempo de pasar lista de un curso | [medir] | menos de 1 minuto, sin ayuda |
| Docentes que completan la tarea sin ayuda | [medir] | todas las de la prueba de uso |
| Tiempo del cierre mensual de porcentajes | [medir] | [definir meta] |
| Alertas con una acción registrada | no se registra | [definir meta] |
| Docentes que lo usan cada semana | 0 | [definir meta] |

## Ventaja

- La autora es docente: conoce el problema desde adentro y las reglas reales (tres motivos de inasistencia, turnos, trimestres), contrastadas con colegas.
- Funciona en la red local de la escuela: no depende de internet y los datos de los alumnos quedan dentro de la institución.
- Sin costo de licencias, con código abierto, documentación y pruebas automáticas.
- Un único lugar donde docente, orientación y dirección ven lo mismo.

## Alcance del MVP

**Dentro (hecho):**

- Pantalla de pasar lista para celular y tablet.
- API: alumnos, asistencia, acciones de seguimiento, reporte de alertas y de seguimiento.
- Manejo de errores con logging, pruebas automáticas e integración continua.
- Carga masiva de nómina desde una lista (en revisión).

**Fuera por ahora, en este orden según la validación con docentes:**

1. Calendario: días no lectivos y días hábiles.
2. Reporte mensual con porcentajes y reporte trimestral para el boletín.
3. Login por rol, obligatorio antes de usarlo con datos reales.
4. Carga de nómina desde una foto: falta comprobar la viabilidad, porque el registro es manuscrito.
