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

1. Elija el escenario arriba: **sismo** (apagón total o red parcial), **avenida torrencial**, **alud o deslizamiento**, **inundación lenta** o **tormenta y vendaval**. Ver [escenarios](escenarios.md).
2. Pulse **▶** para reproducir o **+15 min** para avanzar un ciclo de recálculo.
3. Ajuste la velocidad: **Lenta** (ideal para grabar video), **Normal** o **Rápida**.
4. **Reiniciar** vuelve al minuto 0.
5. **Atajos de teclado** para presentar: <kbd>Espacio</kbd> reproduce o pausa, <kbd>→</kbd> avanza 15 min, <kbd>R</kbd> reinicia.
6. El botón de **tema claro u oscuro** cambia la apariencia (el claro se ve mejor con proyector).

> **Instalable y sin conexión:** abierto desde Render, el navegador ofrece **instalarlo como app**. Después de la primera visita abre aunque no haya internet y conserva las partes del mapa que ya se vieron.

**Línea de tiempo:** arrástrela (o haga clic) para ir a cualquier minuto; con el foco en ella, las flechas avanzan o retroceden 5 min, *Re Pág/Av Pág* 15 min, *Inicio* y *Fin* van al principio y al final. Para retroceder, TRIA vuelve a reproducir el escenario desde el inicio (las vías marcadas a mano se pierden).

**Panel lateral:** en pantallas grandes, *Ocultar panel* deja el mapa a todo el ancho; la elección se recuerda. En el celular, la **barra inferior** lleva a Mapa, Prioridades, Recursos, Bitácora y En vivo, y marca en rojo la Bitácora si hay alertas sin leer.

**Compartir, informe y CSV** (botones sobre el mapa):

- **Compartir** copia un enlace que abre el mismo escenario, minuto y zona, por ejemplo `…/?escenario=alud&t=90&zona=BRU` (también acepta `&tema=claro`). En el celular abre el menú de compartir.
- **Informe** abre la impresión con un resumen limpio: indicadores, prioridades con equipos asignados, hospitales y bitácora completa. Elija "Guardar como PDF" para enviarlo.
- **Bitácora CSV** descarga la bitácora para Excel (separador `;`, con tildes).

**Pestañas con teclado:** con el foco en una pestaña, las flechas ← → pasan a la anterior o la siguiente; *Inicio* y *Fin* van a la primera y la última.

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

**Capas del mapa** (botón arriba a la derecha):

- *Bases:* Oscuro y Claro (CARTO) cambian solas con el tema; también hay OSM oscurecido, Satélite, Calles y Relieve. Si elige una base a mano, se recuerda.
- *Nivel de amenaza del fenómeno:* cuando llega el mapa del fenómeno activo (intensidad del SGC en el sismo; alerta hidrológica, lluvia acumulada o ráfagas del IDEAM en los demás), un círculo por zona con su nivel (amarillo, naranja, rojo de menor a mayor).
- *Cupo de hospitales:* el círculo punteado crece con las camas libres y cambia de color con la ocupación (verde, ámbar, rojo; gris sin energía).
- **◎ Mi ubicación** (bajo el zoom) centra el mapa donde está el equipo; necesita permiso del navegador y conexión segura (https).

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

## 6. Pestaña En vivo (motor real)

Funciona cuando el prototipo se abre desde la API (Render, Docker o `uvicorn tria.api:app`) y también desde Vercel o GitHub Pages: ahí se conecta por defecto a la API de Render (`https://tria-rally2026.onrender.com`). El campo **Servidor de la API** permite usar otra (por ejemplo la del PMU en la red local); también se puede abrir con `?api=https://…`. La API acepta peticiones de Vercel, GitHub Pages y localhost; para otros dominios se define `TRIA_ORIGENES` (expresión regular). Al abrirla, el punto junto a **En vivo** se pone verde.

1. La lista muestra las prioridades que calcula el **motor en Python** (AHP + Bayes) con los reportes que recibe la API, con el aporte de cada criterio. Se actualiza cada 5 s; cuando una zona cambia, parpadea y aparece un aviso.
2. **Sincronizar reloj** pone el motor en el minuto de la simulación, para comparar ambas listas.
   Debajo aparece la **asignación del motor** (programación lineal entera con PuLP): qué equipo va a cada zona, por qué ruta y en cuántos minutos. Mientras la pestaña está abierta, esas rutas se dibujan en el mapa con líneas punteadas.
3. **Probar sin hardware**: envía un reporte (zona, color, personas, heridos) como si llegara de una baliza, o marca una baliza como destruida.
4. Con el receptor LoRa conectado, `herramientas/puente_serial.py` envía los reportes reales a la misma API y aparecen aquí.

**Clave de la API.** Si el servidor tiene la variable `TRIA_CLAVE`, todo lo que cambia el estado (reportes, latidos, vías, intensidad, reloj) exige esa clave; consultar sigue abierto. En Render la clave se genera sola: se ve en el panel del servicio, en *Environment*. En el prototipo se escribe en **Probar sin hardware → Clave de TRIA** (queda guardada solo en ese navegador), y en el puente LoRa con `--clave` o la variable `TRIA_CLAVE`:

```bash
python herramientas/puente_serial.py --puerto COM3 --api https://<servicio>.onrender.com --clave <clave>
```

En la red local del PMU, sin `TRIA_CLAVE`, la API sigue abierta como antes.

## 7. API (para desarrolladores)

En la ruta `/docs` de la dirección de Render (o `http://localhost:8000/docs` en local) se pueden probar:

Si la API tiene clave, las rutas `POST` necesitan la cabecera `X-TRIA-Clave`.

| Ruta | Uso |
|---|---|
| `POST /reportes` | Registrar un reporte (zona, color `rojo`/`amarillo`/`verde`, personas, heridos, canal). |
| `POST /latidos` | Registrar si la baliza de una zona sigue viva. |
| `POST /vias/{a}/{b}?caida=true` | Marcar una vía como caída o habilitada. |
| `POST /intensidad/{zona}/{mmi}` | Cargar la intensidad sísmica del SGC. |
| `GET /prioridades` | Cola de prioridades con el aporte de cada criterio y el estado de cada zona. |
| `GET /asignacion` | Asignación óptima (programación lineal entera). |
| `GET /hospital?origen=BRU&heridos=4` | Hospital recomendado. |
| `GET /estado` | Minuto del motor, pesos AHP y razón de consistencia. |
| `POST /reloj/{minuto}` | Fijar el minuto del motor. |
| `GET /version` | Versión desplegada. |

---

*Datos del escenario: ubicaciones reales de la alcaldía, los hospitales y los centros poblados; poblaciones, tiempos de viaje y probabilidades son estimados para la demostración.*
