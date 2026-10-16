# TRIA – Triaje Territorial Inteligente

**Equipo CHIVAS DE RESCATE** · Rally Latinoamericano de Innovación 2026 · Reto 9: *Optimización y priorización de recursos y esfuerzos en la post-emergencia*

TRIA es un sistema de apoyo a la decisión para el **Puesto de Mando Unificado (PMU)**. Dice **a quién atender primero, por qué ruta y con qué recurso** después de un sismo, una avalancha o una inundación, **incluso cuando la red celular, internet y la energía están caídas**.

> TRIA recomienda; la autoridad decide. Cada recomendación muestra sus criterios.

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
prototipo/        Demo interactiva (un solo HTML, funciona sin internet)
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

**Prototipo:** abrir `prototipo/index.html` con doble clic en cualquier navegador.

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
pmu.red.marcar_caida("J3", "BRU")      # cae la vía Pitalito–Mocoa
print(pmu.prioridades()[:3])
print(pmu.asignacion())                # envía rescate a Bruselas rodeando por Chillurco
```

**En línea (Render):** el archivo `render.yaml` despliega la API y el prototipo en un solo servicio. Cada push a `main` publica una versión nueva automáticamente; el pie del prototipo muestra el commit desplegado. Rutas: `/` prototipo · `/docs` API · `/version` versión desplegada.

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
