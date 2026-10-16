# Manual de uso del prototipo de TRIA

El prototipo simula la consola del **Puesto de Mando Unificado (PMU)** de Pitalito durante un sismo nocturno. Funciona en cualquier navegador; no requiere instalación.

- **En línea:** la dirección de Render del equipo (raíz `/`).
- **Sin internet:** abrir `prototipo/index.html`. El mapa de fondo necesita internet; zonas, vías y equipos se ven igual.

---

## 1. Partes de la pantalla

| Zona de la pantalla | Qué muestra |
|---|---|
| **Barra superior** | Estado de operación, selector de escenario y hora del evento (T+ minutos desde el sismo). |
| **Indicadores** | Zonas con reporte, zonas sin contacto, personas reportadas, heridos trasladados, equipos libres y vías caídas. |
| **Mapa operativo** | Zonas, hospitales, PMU, vías, rutas y equipos sobre el mapa real de Pitalito. |
| **Línea de tiempo** | Avance del evento; cada marca es un suceso del escenario. |
| **Panel derecho** | Pestañas *Prioridades*, *Recursos*, *Bitácora* y *Modelo*. |

## 2. Cómo reproducir la simulación

1. Elija el escenario arriba: **Peor caso: apagón total** (recomendado) o **Apagón parcial**.
2. Pulse **▶** para reproducir o **+15 min** para avanzar un ciclo de recálculo.
3. Ajuste la velocidad: **Lenta** (ideal para grabar video), **Normal** o **Rápida**.
4. **Reiniciar** vuelve al minuto 0.

## 3. Cómo leer el mapa

| Símbolo | Significado |
|---|---|
| Círculo rojo, amarillo o verde con número | Zona que reportó; el número es la cantidad de personas. |
| Círculo violeta punteado con % | Zona sin contacto; el % es la probabilidad estimada de afectación grave. |
| Texto bajo la zona en silencio | Tipo de silencio: *baliza sin reporte*, *baliza destruida* o *sin medio de reporte*. |
| Mancha violeta | Área probable de afectación; crece con la probabilidad. |
| Rombo azul | Puesto de Mando Unificado (Alcaldía). |
| Cuadro con cruz | Hospital; verde con cupo, rojo lleno, gris sin energía. |
| Cuadrito con número | Equipo: rojo rescate, verde atención y traslado, violeta reconocimiento. |
| Línea punteada en movimiento | Ruta del equipo hacia su destino. |
| Línea roja discontinua con ✕ | Vía caída. |

**Controles del mapa:** rueda del mouse o dedos para acercar y alejar · **Capas del mapa** (oscuro, satélite, calles, relieve) · **Centrar** · **Pantalla completa**.

## 4. Interactuar

- **Tumbar o habilitar una vía:** clic sobre la vía. TRIA recalcula rutas y asignaciones al instante.
- **Ver por qué una zona tiene su prioridad:** clic en la zona del mapa o en la lista de *Prioridades*.
- **Comparar con el orden de llegada:** marque *Comparar con orden de llegada*; las zonas incomunicadas aparecen como "nunca".
- **Recursos:** ocupación y energía de cada hospital y estado de cada equipo.
- **Bitácora:** todo lo ocurrido, con hora.
- **Modelo:** la matriz AHP, la razón de consistencia y las fórmulas.

## 5. Corregir ubicaciones

1. Pulse **Ajustar ubicaciones**.
2. Arrastre cada zona, hospital o cruce a su sitio real (use la capa *Satélite* o *Calles*).
3. Pulse **Copiar coordenadas** y pegue el resultado en `GEO_FIJO` dentro de `prototipo/index.html`.

## 6. API (para desarrolladores)

En la ruta `/docs` de la dirección de Render (o `http://localhost:8000/docs` en local) se pueden probar:

| Ruta | Uso |
|---|---|
| `POST /reportes` | Registrar un reporte (zona, color, personas, heridos, canal). |
| `POST /latidos` | Registrar si la baliza de una zona sigue viva. |
| `POST /vias/{a}/{b}?caida=true` | Marcar una vía como caída o habilitada. |
| `POST /intensidad/{zona}/{mmi}` | Cargar la intensidad sísmica del SGC. |
| `GET /prioridades` | Cola de prioridades con el aporte de cada criterio. |
| `GET /asignacion` | Asignación óptima (programación lineal entera). |
| `GET /hospital?origen=BRU&heridos=4` | Hospital recomendado. |
| `GET /version` | Versión desplegada. |

---

*Datos del escenario: ubicaciones reales de la alcaldía, los hospitales y los centros poblados; poblaciones, tiempos de viaje y probabilidades son estimados para la demostración.*
