# Red nacional de Puestos de Mando

TRIA no es solo para Pitalito: cada municipio o departamento que lo adopte tiene su propio **Puesto de Mando (PMU)** con TRIA, y todos se conectan en una red nacional con la **Sala de Crisis Nacional de la UNGRD**.

**Demostración:** `prototipo/red.html` (en Render: `/red.html`, o desde el menú **Más → Red nacional** del prototipo).

## Qué pasa si un PMU se cae

| Paso | Qué hace la red |
|---|---|
| 1. Latidos | Cada PMU envía un latido cada 30 s a la UNGRD y a dos PMU vecinos, por internet o por satélite. |
| 2. Réplica | Cada 5 min copia su estado (cola de prioridades, equipos, hospitales, bitácora) en esos vecinos. |
| 3. Detección | Si se pierden 3 latidos seguidos (90 s), se genera una alerta en la UNGRD y en los vecinos. |
| 4. Respaldo | El vecino en operación (primero la capital del mismo departamento) asume el mando con la última réplica y sigue priorizando la zona. |
| 5. Recuperación | Se despacha un kit satelital móvil al PMU caído; cuando vuelve, sincroniza lo ocurrido y retoma el mando. |

## La historia de la demostración

1. **Red operando.** 17 PMU y la Sala de Crisis Nacional intercambian latidos.
2. **Sismo en el Huila.** Pitalito pierde internet y sigue por satélite (ámbar).
3. **Falla del PMU.** Una réplica deja a Pitalito sin energía ni antena (rojo). Se cuentan los latidos perdidos: 1 de 3, 2 de 3…
4. **Alerta y respaldo.** A los 90 s, Neiva (capital del Huila) asume el respaldo con la última réplica, y se avisa a la UNGRD y a Popayán.
5. **Recuperación.** Llega el kit satelital, Pitalito vuelve, sincroniza y retoma el mando.

Se puede hacer clic en cualquier PMU para simular su caída o su regreso.

*Las ubicaciones de las ciudades son aproximadas; la red, los enlaces y los tiempos son ilustrativos.*
