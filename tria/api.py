"""API local del Puesto de Mando (funciona sin internet, en la red del PMU).

Ejecutar:  uvicorn tria.api:app --reload
Documentación interactiva:  http://localhost:8000/docs
"""
from __future__ import annotations

import os
import secrets
from pathlib import Path
from typing import Literal, Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .escenario import PuestoDeMando

app = FastAPI(title="TRIA – Triaje Territorial Inteligente", version="0.1.0")

# CORS: permite que el prototipo publicado en otro dominio (Vercel, GitHub Pages) consulte esta API.
# TRIA_ORIGENES es una expresión regular de orígenes; por defecto Vercel, GitHub Pages y localhost.
# No reemplaza la clave: las rutas que cambian el estado siguen exigiendo X-TRIA-Clave si está definida.
ORIGENES_DEFECTO = (r"https://([a-z0-9-]+\.)*vercel\.app|https://[a-z0-9-]+\.github\.io"
                    r"|http://(localhost|127\.0\.0\.1)(:\d+)?")
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=os.getenv("TRIA_ORIGENES", ORIGENES_DEFECTO),
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-TRIA-Clave"],
)


def exigir_clave(x_tria_clave: Optional[str] = Header(default=None)) -> None:
    """Si TRIA_CLAVE está definida, las rutas que cambian el estado exigen la cabecera X-TRIA-Clave.

    Sin TRIA_CLAVE (red local del PMU) todo queda abierto, como antes. Se lee en cada llamada para
    poder cambiarla sin reiniciar y para las pruebas.
    """
    clave = os.getenv("TRIA_CLAVE")
    if clave and not secrets.compare_digest((x_tria_clave or "").encode(), clave.encode()):
        raise HTTPException(401, "Falta la clave de TRIA o no es correcta (cabecera X-TRIA-Clave)")


CON_CLAVE = [Depends(exigir_clave)]
pmu = PuestoDeMando()


class Reporte(BaseModel):
    zona: str
    color: Literal["rojo", "amarillo", "verde"]
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


@app.get("/salud")
def salud():
    """Comprobación de vida para Docker, Render y monitores externos."""
    return {"ok": True, "zonas": len(pmu.zonas), "minuto": pmu.t}


@app.get("/estado")
def estado():
    return {"minuto": pmu.t, "pesos_ahp": [round(w, 3) for w in pmu.pesos],
            "consistencia": round(pmu.consistencia, 3), "requiere_clave": bool(os.getenv("TRIA_CLAVE"))}


@app.post("/reloj/{minuto}", dependencies=CON_CLAVE)
def fijar_minuto(minuto: float):
    pmu.t = minuto
    return {"minuto": pmu.t}


@app.post("/reportes", dependencies=CON_CLAVE)
def nuevo_reporte(r: Reporte):
    z = pmu.zonas.get(r.zona)
    if not z:
        raise HTTPException(404, f"Zona {r.zona} no existe")
    z.registrar_reporte(pmu.t, r.color, r.personas, r.heridos, r.senales_vida, r.colapso)
    return {"ok": True, "zona": z.id, "canal": r.canal}


@app.post("/latidos", dependencies=CON_CLAVE)
def latido(l: Latido):
    z = pmu.zonas.get(l.zona)
    if not z:
        raise HTTPException(404, f"Zona {l.zona} no existe")
    z.latido = l.vivo
    return {"ok": True}


@app.post("/vias/{a}/{b}", dependencies=CON_CLAVE)
def marcar_via(a: str, b: str, caida: bool = True):
    if not pmu.red.g.has_edge(a, b):
        raise HTTPException(404, "Vía no existe")
    pmu.red.marcar_caida(a, b, caida)
    return {"ok": True, "via": [a, b], "caida": caida}


@app.post("/intensidad/{zona}/{mmi}", dependencies=CON_CLAVE)
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
