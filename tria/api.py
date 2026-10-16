"""API local del Puesto de Mando (funciona sin internet, en la red del PMU).

Ejecutar:  uvicorn tria.api:app --reload
Documentación interactiva:  http://localhost:8000/docs
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .escenario import PuestoDeMando

app = FastAPI(title="TRIA – Triaje Territorial Inteligente", version="0.1.0")
pmu = PuestoDeMando()


class Reporte(BaseModel):
    zona: str
    color: str  # rojo | amarillo | verde
    personas: int = 0
    heridos: int = 0
    senales_vida: int = 0
    colapso: bool = False
    canal: str = "baliza"  # baliza | radio_kit | dron | lona | equipo | sms


class Latido(BaseModel):
    zona: str
    vivo: bool = True


@app.get("/version")
def version():
    """Versión desplegada. En Render, RENDER_GIT_COMMIT trae el commit de GitHub."""
    commit = os.getenv("RENDER_GIT_COMMIT", "local")
    return {"version": app.version, "commit": commit[:7]}


@app.get("/estado")
def estado():
    return {"minuto": pmu.t, "pesos_ahp": [round(w, 3) for w in pmu.pesos],
            "consistencia": round(pmu.consistencia, 3)}


@app.post("/reloj/{minuto}")
def fijar_minuto(minuto: float):
    pmu.t = minuto
    return {"minuto": pmu.t}


@app.post("/reportes")
def nuevo_reporte(r: Reporte):
    z = pmu.zonas.get(r.zona)
    if not z:
        raise HTTPException(404, f"Zona {r.zona} no existe")
    z.registrar_reporte(pmu.t, r.color, r.personas, r.heridos, r.senales_vida, r.colapso)
    return {"ok": True, "zona": z.id, "canal": r.canal}


@app.post("/latidos")
def latido(l: Latido):
    z = pmu.zonas.get(l.zona)
    if not z:
        raise HTTPException(404, f"Zona {l.zona} no existe")
    z.latido = l.vivo
    return {"ok": True}


@app.post("/vias/{a}/{b}")
def marcar_via(a: str, b: str, caida: bool = True):
    if not pmu.red.g.has_edge(a, b):
        raise HTTPException(404, "Vía no existe")
    pmu.red.marcar_caida(a, b, caida)
    return {"ok": True, "via": [a, b], "caida": caida}


@app.post("/intensidad/{zona}/{mmi}")
def intensidad(zona: str, mmi: int):
    pmu.zonas[zona].intensidad = mmi
    return {"ok": True}


@app.get("/prioridades")
def prioridades():
    return pmu.prioridades()


@app.get("/asignacion")
def asignacion():
    return pmu.asignacion()


@app.get("/hospital")
def hospital(origen: str, heridos: int = 1, zona: Optional[str] = None):
    from .asignacion import elegir_hospital
    h = elegir_hospital(origen, heridos, pmu.hospitales, pmu.red)
    if not h:
        raise HTTPException(409, "Ningún hospital con cupo y energía alcanzable")
    return h


# El prototipo (y futuras páginas) se sirven desde la raíz: https://<servicio>.onrender.com/
# Se monta al final para que no tape las rutas de la API.
_PROTOTIPO = Path(__file__).resolve().parent.parent / "prototipo"
if _PROTOTIPO.is_dir():
    app.mount("/", StaticFiles(directory=_PROTOTIPO, html=True), name="prototipo")
