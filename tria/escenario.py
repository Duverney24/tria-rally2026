"""Carga del escenario y estado en memoria del Puesto de Mando."""
from __future__ import annotations

import json
from pathlib import Path

from .asignacion import Equipo, Necesidad, asignar
from .modelo import MATRIZ_AHP_EJEMPLO, Zona, indice_urgencia, necesidades, pesos_ahp
from .rutas import RedVial

RUTA_DEFECTO = Path(__file__).resolve().parent.parent / "datos" / "escenario_pitalito.json"


class PuestoDeMando:
    def __init__(self, archivo: Path = RUTA_DEFECTO, matriz_ahp=MATRIZ_AHP_EJEMPLO):
        datos = json.loads(Path(archivo).read_text(encoding="utf-8"))
        self.zonas = {z["id"]: Zona(**z) for z in datos["zonas"]}
        self.hospitales = datos["hospitales"]
        self.equipos = {e["id"]: Equipo(**e) for e in datos["equipos"]}
        self.red = RedVial(datos["vias"])
        self.pesos, self.consistencia = pesos_ahp(matriz_ahp)
        self.t = 0.0  # minutos desde el evento

    def prioridades(self) -> list[dict]:
        filas = []
        for z in self.zonas.values():
            u, aportes = indice_urgencia(z, self.t, self.pesos)
            filas.append({"zona": z.id, "nombre": z.nombre, "en_silencio": z.en_silencio,
                          "indice": round(u, 3), "aportes": {k: round(v, 3) for k, v in aportes.items()},
                          "necesidades": necesidades(z, self.t)})
        return sorted(filas, key=lambda f: -f["indice"])

    def asignacion(self) -> list[dict]:
        nec = [Necesidad(f["zona"], tipo, f["indice"]) for f in self.prioridades() for tipo in f["necesidades"]]
        return asignar(list(self.equipos.values()), nec, self.red)
