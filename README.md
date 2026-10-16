# TRIA – Triaje Territorial Inteligente

**Equipo CHIVAS DE RESCATE** · Rally Latinoamericano de Innovación 2026 · Reto 9: *Optimización y priorización de recursos y esfuerzos en la post-emergencia*

TRIA es un sistema de apoyo a la decisión para el **Puesto de Mando Unificado (PMU)**. Dice **a quién atender primero, por qué ruta y con qué recurso** después de un sismo, una avalancha o una inundación, **incluso cuando la red celular, internet y la energía están caídas**.

> TRIA recomienda; la autoridad decide. Cada recomendación muestra sus criterios.

**📖 [Manual de uso del prototipo](docs/manual_de_uso.md)** · **🏗️ [Arquitectura](docs/arquitectura.md)** · **🌋 [Escenarios](docs/escenarios.md)** · **🎤 [Preguntas del jurado](docs/temas_por_integrante.md)**

---

## Funcionalidades

### Para el Puesto de Mando (quien coordina la emergencia)

| Funcionalidad | Qué hace |
|---|---|
| **Cola de prioridades** | Ordena todas las zonas por un índice de urgencia (0 a 1) y se recalcula cada 15 minutos o ante cualquier evento. |
| **Explicación de cada prioridad** | Al elegir una zona muestra cuánto aporta cada criterio: severidad, personas afectadas, vulnerabilidad y tiempo sin atención. |
| **Estimación de zonas en silencio** | Calcula la probabilidad de afectación grave de las zonas que no reportan, con el mapa de amenaza, la intensidad sísmica y el tipo de silencio. |
| **Detección de balizas destruidas** | Si una baliza deja de enviar su latido automático, eleva la urgencia de esa zona. |
| **Asignación de equipos** | Asigna a cada necesidad (rescate, atención y traslado, reconocimiento) un solo equipo del tipo correcto, sin duplicar esfuerzos. |
| **Rutas con vías caídas** | Calcula la ruta más rápida evitando las vías bloqueadas y re-enruta a los equipos que van en camino. |
| **Elección de hospital** | Envía a los heridos al hospital alcanzable con cupo y energía, no al más cercano si está saturado. |
| **Mapa operativo real** | Pitalito con zoom; capas oscura, satelital, de calles y de relieve; áreas probables de afectación; equipos en movimiento. |
| **Bitácora** | Registro con hora de cada reporte, asignación, re-enrutamiento y entrega de heridos. |
| **Comparación con "quien reporta primero"** | Muestra que atender por orden de llegada deja por fuera a las zonas incomunicadas. |
| **Escenarios multiamenaza** | Sismo (apagón total o red parcial), avenida torrencial, alud o deslizamiento, inundación lenta y tormenta con vendaval, cada uno con su mapa de amenaza y su fuente oficial (SGC, IDEAM). Ver [escenarios](docs/escenarios.md). |

### Para la comunidad (quien reporta)

| Medio | Cómo se usa | ¿Necesita app o internet? |
|---|---|---|
| **Baliza comunitaria** | Botones rojo, amarillo y verde, y "+5 personas". | No |
| **WiFi TRIA-EMERGENCIA** *(en desarrollo)* | El celular se conecta a la baliza y abre una página de reporte sola. | No |
| **SMS** | Mensaje corto a un número fijo cuando hay algo de señal. | No |
| **Kit comunitario** | Radio LoRa de bolsillo conectado al celular por Bluetooth. | App del radio, sin internet |
| **Lona y señales tierra-aire** | Lona de color o una "V" o "X" visible para el dron. | No |
| **A pie** | Llevar el reporte al punto de encuentro o a un equipo en terreno. | No |

---

## Idea central

La mayoría de los sistemas atiende a quien logra reportar. TRIA también **prioriza el silencio**:

- Si una zona **tiene baliza activa pero nadie reporta**, su urgencia sube con el tiempo, porque una zona sin daños suele avisar pronto.
- Si **la baliza deja de emitir su latido automático**, probablemente fue destruida, y esa es la señal más fuerte de afectación grave.
- Si la zona **no tiene ningún medio de reporte**, su silencio no informa nada, y TRIA prioriza con el mapa de amenaza, el censo del DANE y la intensidad sísmica del SGC.

## Capas de comunicación (sin un único punto de falla)

| Capa | Medio | Funciona si… |
|---|---|---|
| 1 | Baliza solar LoRa con botones rojo, amarillo y verde, latido automático y malla | cae la red celular |
| 2 | Kit comunitario en un punto seguro: radios LoRa portátiles conectables al celular por Bluetooth | se destruye la baliza |
| 3 | Dron con receptor LoRa que recoge los mensajes al sobrevolar | no hay ninguna red en tierra |
| 4 | Lonas de colores y señales tierra-aire OACI (V, X, Y, N, flecha) que ve el dron o una aeronave | no funciona ningún aparato |
| 5 | Personas como mensajeros: vecinos y equipos en terreno que reportan cada zona por donde pasan | no hay nada más |
| Final | TRIA prioriza con amenaza, censo e intensidad y **sale a buscar** la información | llegan cero reportes |

## Estructura del repositorio

```
prototipo/        Demo interactiva (un HTML + Leaflet y fuentes locales en vendor/; sw.js la deja disponible sin internet)
tria/             Motor en Python
  modelo.py         AHP, Bayes para zonas en silencio, índice de urgencia
  rutas.py          Grafo vial con NetworkX; evita vías caídas
  asignacion.py     Asignación óptima con programación lineal entera (PuLP) y elección de hospital
  escenario.py      Estado del Puesto de Mando
  api.py            API local con FastAPI
datos/            Escenario ilustrativo de Pitalito (Huila)
firmware/         Baliza y receptor/repetidor LoRa (ESP32 + SX1276)
herramientas/     Puente serie: receptor LoRa → API
tests/            Pruebas del modelo
docs/             Arquitectura y reparto de temas del equipo
```

## Cómo ejecutarlo

**Prototipo:** abrir `prototipo/index.html` en el navegador. El mapa usa Leaflet (incluido en `prototipo/vendor/`) con capas de OpenStreetMap, Esri (satélite) y OpenTopoMap, que necesitan internet la primera vez. Servido por la API o en Render, un service worker (`prototipo/sw.js`) guarda la app y las teselas que se van viendo, así que el prototipo abre y muestra el mapa ya recorrido aunque se caiga la red; en campo se complementa con teselas descargadas previamente. La alcaldía, los hospitales y los centros poblados de los corregimientos están en su **ubicación real**; las riberas urbanas son aproximadas. Se pueden corregir con el botón "Ajustar ubicaciones" y pegar el resultado en `GEO_FIJO`.

**Motor y API:**

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
pytest -q                        # pruebas
uvicorn tria.api:app --reload    # API en http://localhost:8000/docs
```

Ejemplo rápido en Python:

```python
from tria.escenario import PuestoDeMando
pmu = PuestoDeMando()
pmu.zonas["BRU"].latido = False        # la baliza de Bruselas dejó de latir
pmu.red.marcar_caida("CRI", "BRU")     # cae la vía a Bruselas
print(pmu.prioridades()[:3])
print(pmu.asignacion())                # envía rescate a Bruselas rodeando por Palmarito
```

**En línea (Render):** el archivo `render.yaml` despliega la API y el prototipo en un solo servicio. Cada push a `main` publica una versión nueva automáticamente; el pie del prototipo muestra el commit desplegado. Rutas: `/` prototipo · `/docs` API · `/version` versión desplegada.

**Con Docker (PMU en una laptop o mini-PC, sin internet):**

```bash
docker compose up -d            # http://localhost:8000  (o http://<ip-del-equipo>:8000 en la red local)
TRIA_CLAVE=... docker compose up -d   # exige clave en las rutas que cambian el estado
```

La imagen trae la API y el prototipo, corre con un usuario sin privilegios y Docker comprueba su salud con `/version`.

**Prototipo en Vercel:** `vercel.json` publica `prototipo/` como sitio estático, sin build. Basta importar el repositorio en https://vercel.com/new y pulsar *Deploy* (sin cambiar ajustes); cada push a `main` se despliega solo. La API sigue en Render.

**Prototipo en GitHub Pages:** cada push a `main` que toque `prototipo/` lo publica en https://duverney24.github.io/tria-rally2026/ (flujo `.github/workflows/pages.yml`, rama `gh-pages`). Es el mismo prototipo, servido como sitio estático: la simulación, el modo sin conexión y la instalación como app funcionan; la pestaña *En vivo* necesita la API, que sigue en Render.

**Hardware:** ver `firmware/baliza/baliza.ino` y `firmware/receptor/receptor.ino` (Arduino IDE, librería *LoRa* de Sandeep Mistry, banda de 915 MHz; verificar la regulación vigente de la ANE).

## Estado

| Componente | Estado |
|---|---|
| Prototipo visual con escenario de peor caso | ✅ |
| Modelo AHP + Bayes + índice | ✅ con pruebas |
| Asignación con programación lineal entera | ✅ en el motor; el prototipo HTML usa asignación voraz para la demo |
| API local | ✅ básica |
| Firmware de baliza y receptor | 🟡 borrador, sin probar en hardware |
| Registro único de heridos y desaparecidos | ⏳ pendiente |
| Integración dron y lonas | ⏳ pendiente (entrada manual vía `/reportes` con `canal`) |

## Datos

El escenario de Pitalito es **ilustrativo**: las poblaciones, probabilidades previas, intensidades y tiempos de viaje deben reemplazarse por el censo del DANE, el mapa de amenaza municipal y la cartografía real. Los datos personales de heridos y desaparecidos se tratarían según la Ley 1581 de 2012 (habeas data).

## Equipo

Santiago Bernal Pertuz (líder) · Sharon Bolaños · Tania González · Jaime Johan Rosas Guzmán · Duverney Torres Figueroa · Jhunier Libardo Hernández Calderón · Lizley Reyes Álvarez (docente)

## Declaración de uso de IA

Claude (Anthropic) · apoyo en la búsqueda de fuentes, en la estructura del código base y del prototipo y en la corrección de redacción. El equipo definió la idea, eligió el enfoque, revisó y adaptó el código y verificó los datos.

## Licencia

MIT. Según las bases del Rally, el material entregado pasa a dominio público.
