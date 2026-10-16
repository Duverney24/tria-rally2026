"""Asignación óptima de equipos a necesidades con programación lineal entera (PuLP).

Variables: x[e, n] = 1 si el equipo e atiende la necesidad n.
Objetivo:  maximizar  suma( x[e,n] * (U_n - lambda * t_en / T_max) )
Restricciones:
  - cada equipo atiende como máximo una necesidad;
  - cada necesidad recibe como máximo un equipo (sin duplicar esfuerzos);
  - solo equipos del tipo correcto y con ruta transitable.
"""
from __future__ import annotations

from dataclasses import dataclass

import pulp

from .rutas import RedVial


@dataclass
class Equipo:
    id: str
    nombre: str
    tipo: str  # "rescate", "aph" o "edan"
    ubicacion: str
    libre: bool = True


@dataclass
class Necesidad:
    zona: str
    tipo: str
    urgencia: float


def asignar(equipos: list[Equipo], necesidades: list[Necesidad], red: RedVial,
            lam: float = 0.3) -> list[dict]:
    libres = [e for e in equipos if e.libre]
    opciones = {}
    for e in libres:
        tiempos = red.tiempos_desde(e.ubicacion)
        for i, n in enumerate(necesidades):
            if e.tipo == n.tipo and n.zona in tiempos:
                opciones[(e.id, i)] = tiempos[n.zona]
    if not opciones:
        return []

    t_max = max(opciones.values()) or 1.0
    prob = pulp.LpProblem("asignacion_TRIA", pulp.LpMaximize)
    x = {k: pulp.LpVariable(f"x_{k[0]}_{k[1]}", cat="Binary") for k in opciones}
    prob += pulp.lpSum(x[k] * (necesidades[k[1]].urgencia - lam * opciones[k] / t_max) for k in x)
    for e in libres:
        prob += pulp.lpSum(x[k] for k in x if k[0] == e.id) <= 1
    for i in range(len(necesidades)):
        prob += pulp.lpSum(x[k] for k in x if k[1] == i) <= 1
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    resultado = []
    for k, var in x.items():
        if var.value() and var.value() > 0.5:
            n = necesidades[k[1]]
            camino, minutos = red.ruta(next(e.ubicacion for e in libres if e.id == k[0]), n.zona)
            resultado.append({"equipo": k[0], "zona": n.zona, "tipo": n.tipo,
                              "urgencia": round(n.urgencia, 3), "minutos": minutos, "ruta": camino})
    return sorted(resultado, key=lambda r: -r["urgencia"])


def elegir_hospital(origen: str, heridos: int, hospitales: dict[str, dict], red: RedVial) -> dict | None:
    """El hospital alcanzable más cercano con cupo y energía (no el más cercano saturado)."""
    tiempos = red.tiempos_desde(origen)
    candidatos = [
        (tiempos[h], h) for h, d in hospitales.items()
        if d["energia"] and d["capacidad"] - d["ocupacion"] >= heridos and h in tiempos
    ]
    if not candidatos:
        return None
    minutos, h = min(candidatos)
    return {"hospital": h, "minutos": minutos}
