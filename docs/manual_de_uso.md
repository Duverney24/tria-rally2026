# Manual de uso del prototipo de TRIA

El prototipo simula la consola del **Puesto de Mando Unificado (PMU)** de Pitalito durante un sismo nocturno. Funciona en cualquier navegador; no requiere instalación.

- **En línea:** la dirección de Render del equipo (raíz `/`).
- **Sin internet:** abrir `prototipo/index.html`. El mapa de fondo necesita internet; zonas, vías y equipos se ven igual.

---

## Guía de bienvenida

La entrada muestra dos opciones: **Explorar la simulación** y **Consultar el motor**. El mapa y los paneles se abren después de elegir una tarea. Al entrar por primera vez a la simulación, aparece una guía de seis pasos: escenario, reproducción, mapa, prioridades, recursos y En vivo. Use **Siguiente** y **Anterior**, o **Omitir** para entrar directamente. **Empezar a usar TRIA** cierra el último paso.

La guía se recuerda en este navegador al terminarla u omitirla (también con Escape). Puede abrirla de nuevo con **Cómo usar**, en la barra superior. Mientras está abierta, la simulación queda pausada y sus atajos no actúan; al cerrarla, pulse Reproducir para continuar. Si borra los datos del sitio o usa otro navegador, volverá a aparecer. Si el navegador bloquea el almacenamiento, la guía funciona, pero puede reaparecer en la siguiente visita.

## 1. Partes de la pantalla

| Zona de la pantalla | Qué muestra |
|---|---|
| **Barra superior** | Identidad de TRIA, ayuda y tema. En simulación, muestra la hora del escenario. |
| **Indicadores** | Zonas con reporte, zonas sin contacto, personas reportadas, heridos trasladados, equipos libres y vías caídas. |
| **Mapa operativo** | Vista principal con zonas, hospitales, PMU, vías, rutas y equipos sobre el mapa real de Pitalito. |
| **Línea de tiempo** | Avance del evento; cada marca es un suceso del escenario. |
| **Panel operativo derecho** | *Prioridades*, *Recursos* y *Bitácora* sin ocultar el mapa. En pantallas angostas aparece debajo del mapa. |
| **Navegación superior** | *Mapa operativo*, *Modelo* y *Motor conectado*. *Inicio* vuelve a las dos opciones de entrada. |

## 2. Cómo reproducir la simulación

1. Elija el escenario arriba: **sismo** (apagón total o red parcial), **avenida torrencial**, **alud o deslizamiento**, **inundación lenta** o **tormenta y vendaval**. Ver [escenarios](escenarios.md).
2. Pulse **▶** para reproducir o **+15 min** para avanzar un ciclo de recálculo.
3. Ajuste la velocidad: **1×** (lenta), **2×** (normal) o **4×** (rápida). En celular se mantiene la velocidad normal.
4. **Reiniciar** vuelve al minuto 0.
5. **Atajos de teclado** para presentar: <kbd>Espacio</kbd> reproduce o pausa, <kbd>→</kbd> avanza 15 min, <kbd>R</kbd> reinicia.
6. El botón de **tema claro u oscuro** cambia la apariencia (el claro se ve mejor con proyector).

> **Instalable y sin conexión:** abierto desde Render, el navegador ofrece **instalarlo como app**. Después de la primera visita abre aunque no haya internet y conserva las partes del mapa que ya se vieron.

**Línea de tiempo:** arrástrela (o haga clic) para ir a cualquier minuto; con el foco en ella, las flechas avanzan o retroceden 5 min, *Re Pág/Av Pág* 15 min, *Inicio* y *Fin* van al principio y al final. Para retroceder, TRIA vuelve a reproducir el escenario desde el inicio (las vías marcadas a mano se pierden).

**Vista operativa:** el mapa permanece como área principal. En escritorio, a la derecha se cambia entre **Prioridades**, **Recursos** y **Bitácora**; en celular, el panel aparece debajo del mapa. El escenario se conserva al cambiar el contenido del panel. Al volver a Inicio o entrar al Motor conectado, la simulación se pausa. Los indicadores y el mapa simulados no se muestran en Motor conectado.

**Compartir, informe y CSV** (en la sección Bitácora):

- **Compartir** copia un enlace que abre el mismo escenario, minuto y zona, por ejemplo `…/?escenario=alud&t=90&zona=BRU` (también acepta `&tema=claro`). En el celular abre el menú de compartir.
- **Informe** abre la impresión con un resumen limpio: indicadores, prioridades con equipos asignados, hospitales y bitácora completa. Elija "Guardar como PDF" para enviarlo.
- **Bitácora CSV** descarga la bitácora para Excel (separador `;`, con tildes).

**Navegación con teclado:** Tab recorre la navegación y las pestañas del panel; las flechas izquierda y derecha cambian entre **Prioridades**, **Recursos** y **Bitácora**. El título recibe el foco al cambiar de vista.

La ayuda rápida sigue disponible con el botón **?** o la tecla **?**. La leyenda del mapa es plegable y empieza cerrada en celular.

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

- *Bases:* Oscuro y Claro usan OpenStreetMap y cambian con el tema; también hay Satélite y Relieve. Ninguna requiere API key. Si elige una base a mano, se recuerda.
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

1. En Mapa, abra **Más** y pulse **Ajustar ubicaciones**.
2. Arrastre cada zona, hospital o cruce a su sitio real (use la capa *Satélite* o *Calles*).
3. Pulse **Copiar coordenadas** y pegue el resultado en `GEO_FIJO` dentro de `prototipo/index.html`.

## 6. Motor conectado (consulta de la API)

Funciona cuando el prototipo se abre desde la API (Render, Docker o `uvicorn tria.api:app`) y también desde Vercel o GitHub Pages: ahí se conecta por defecto a la API de Render (`https://tria-rally2026.onrender.com`). El campo **Servidor de la API** permite usar otra (por ejemplo la del PMU en la red local); también se puede abrir con `?api=https://…`. La API acepta peticiones de Vercel, GitHub Pages y localhost; para otros dominios se define `TRIA_ORIGENES` (expresión regular). La sección muestra el estado de conexión y la hora de la última consulta correcta. Esta hora no confirma la vigencia de los reportes. Si la consulta falla o envejece, se señala **Datos sin actualizar**; los errores de conexión abren la configuración del servidor.

1. La lista muestra las prioridades que calcula el **motor en Python** (AHP + Bayes) con los reportes que recibe la API, con el aporte de cada criterio. Se actualiza cada 5 s; cuando una zona cambia, parpadea y aparece un aviso.
2. En **Herramientas de prueba**, **Copiar minuto de la simulación al motor** modifica el reloj del servidor tras confirmar la acción.
   Debajo aparece la **asignación del motor** (programación lineal entera con PuLP): qué equipo va a cada zona, por qué ruta y en cuántos minutos. La lista de recomendaciones permanece separada del mapa simulado. No equivale a despachos confirmados.
3. **Herramientas de prueba**: tras confirmar, envía un reporte (zona, color, personas, heridos) como si llegara de una baliza, o marca una baliza como destruida.
4. Con el receptor LoRa conectado, `herramientas/puente_serial.py` envía los reportes reales a la misma API y aparecen aquí.

**Clave de la API.** Si el servidor tiene la variable `TRIA_CLAVE`, todo lo que cambia el estado (reportes, latidos, vías, intensidad, reloj) exige esa clave; consultar sigue abierto. En Render la clave se genera sola: se ve en el panel del servicio, en *Environment*. En el prototipo se escribe en **Herramientas de prueba → Clave de TRIA** (queda guardada solo en ese navegador), y en el puente LoRa con `--clave` o la variable `TRIA_CLAVE`:

```bash
python herramientas/puente_serial.py --puerto COM3 --api https://<servicio>.onrender.com --clave <clave>
```

En la red local del PMU, sin `TRIA_CLAVE`, la API sigue abierta como antes.

**Alcance:** este prototipo requiere validación técnica y operativa antes de utilizarse en emergencias reales. Estar conectado a la API no acredita que sus datos sean reales o actuales. El registro único de personas y los despachos confirmados no están implementados en esta interfaz.

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
