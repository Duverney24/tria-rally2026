"""Modelo de urgencia de TRIA.

Tres piezas, todas explicables:
1. Pesos de los criterios con AHP (Proceso Analítico Jerárquico).
2. Probabilidad de afectación grave de una zona en silencio (Bayes en forma de chances).
3. Índice de urgencia = suma ponderada de criterios normalizados entre 0 y 1.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

CRITERIOS = ["severidad", "personas", "vulnerabilidad", "tiempo"]

# Matriz de comparación por pares (escala de Saaty). La define el Consejo
# Municipal de Gestión del Riesgo; estos valores son un ejemplo.
MATRIZ_AHP_EJEMPLO = [
    [1, 2, 3, 4],
    [1 / 2, 1, 2, 3],
    [1 / 3, 1 / 2, 1, 2],
    [1 / 4, 1 / 3, 1 / 2, 1],
]

# Índice aleatorio de Saaty según el tamaño de la matriz.
_RI = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}


def pesos_ahp(matriz: list[list[float]]) -> tuple[list[float], float]:
    """Devuelve (pesos, razón de consistencia). CR < 0,10 se considera coherente."""
    n = len(matriz)
    medias = [math.prod(fila) ** (1 / n) for fila in matriz]
    total = sum(medias)
    w = [m / total for m in medias]
    aw = [sum(matriz[i][j] * w[j] for j in range(n)) for i in range(n)]
    lambda_max = sum(aw[i] / w[i] for i in range(n)) / n
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    cr = ci / _RI[n] if _RI.get(n) else 0.0
    return w, cr


# --- Bayes para zonas en silencio -------------------------------------------

# Razón de verosimilitud según la intensidad sísmica (MMI) reportada por el SGC.
LR_INTENSIDAD = {5: 0.5, 6: 0.7, 7: 1.5, 8: 2.5, 9: 4.0}
LR_LATIDO_PERDIDO = 5.0  # la baliza dejó de emitir su latido: probable destrucción
P_SILENCIO_SI_GRAVE = 0.9


def p_silencio_si_no_grave(minutos: float, tau: float = 40.0) -> float:
    """Una zona sin daños suele reportar pronto: esta probabilidad cae con el tiempo."""
    return 0.9 * math.exp(-minutos / tau) + 0.05


def probabilidad_grave(
    previa: float,
    minutos_silencio: float,
    medio: str = "baliza",
    latido: bool = True,
    intensidad: Optional[int] = None,
) -> float:
    """P(afectación grave | evidencia).

    medio: "baliza", "celular" o "ninguno".
      - "ninguno": callar no aporta información (razón 1); manda la amenaza.
      - latido=False: la baliza fue probablemente destruida (razón 5).
      - en otro caso: silencio con medio disponible (razón a / b(t)).
    """
    chances = previa / (1 - previa)
    if intensidad is not None:
        chances *= LR_INTENSIDAD.get(intensidad, 1.0)
    if medio == "ninguno":
        lr = 1.0
    elif not latido:
        lr = LR_LATIDO_PERDIDO
    else:
        lr = P_SILENCIO_SI_GRAVE / p_silencio_si_no_grave(minutos_silencio)
    chances *= lr
    return chances / (1 + chances)


# --- Zonas e índice ----------------------------------------------------------

SEVERIDAD_COLOR = {"rojo": 1.0, "amarillo": 0.6, "verde": 0.15}


@dataclass
class Zona:
    id: str
    nombre: str
    poblacion: int
    vulnerabilidad: float  # 0-1, a partir de indicadores del DANE
    previa: float  # probabilidad previa de afectación grave (mapa de amenaza)
    medio: str = "baliza"
    latido: bool = True
    intensidad: Optional[int] = None
    # estado
    en_silencio: bool = True
    silencio_desde: float = 0.0
    color: Optional[str] = None
    personas: int = 0
    heridos: int = 0
    senales_vida: int = 0
    colapso: bool = False
    primer_reporte: Optional[float] = None
    rescate_hecho: bool = False
    extra: dict = field(default_factory=dict)

    def registrar_reporte(self, t: float, color: str, personas: int, heridos: int = 0,
                          senales_vida: int = 0, colapso: bool = False) -> None:
        self.en_silencio = False
        self.color, self.personas, self.heridos = color, personas, heridos
        self.senales_vida, self.colapso = senales_vida, colapso
        if self.primer_reporte is None:
            self.primer_reporte = t


def criterios(z: Zona, t: float) -> dict[str, float]:
    """Valores normalizados (0-1) de cada criterio para la zona en el minuto t."""
    if z.en_silencio:
        p = probabilidad_grave(z.previa, t - z.silencio_desde, z.medio, z.latido, z.intensidad)
        afectados = z.poblacion * p * 0.05
        return {
            "severidad": p,
            "personas": min(1.0, afectados / 200),
            "vulnerabilidad": z.vulnerabilidad,
            "tiempo": min(1.0, (t - z.silencio_desde) / 180),
        }
    sev = 1.0 if (z.colapso or z.senales_vida > 0) else SEVERIDAD_COLOR.get(z.color or "verde", 0.15)
    return {
        "severidad": sev,
        "personas": min(1.0, z.personas / 200),
        "vulnerabilidad": z.vulnerabilidad,
        "tiempo": min(1.0, (t - (z.primer_reporte or t)) / 180),
    }


def indice_urgencia(z: Zona, t: float, pesos: list[float]) -> tuple[float, dict[str, float]]:
    """Devuelve (índice, aporte de cada criterio) para poder explicar la recomendación."""
    c = criterios(z, t)
    aportes = {k: c[k] * pesos[i] for i, k in enumerate(CRITERIOS)}
    return sum(aportes.values()), aportes


def necesidades(z: Zona, t: float) -> list[str]:
    """Qué tipo de equipo necesita la zona: rescate, aph (atención y traslado) o edan."""
    if z.en_silencio:
        p = probabilidad_grave(z.previa, t - z.silencio_desde, z.medio, z.latido, z.intensidad)
        if p >= 0.65:
            return ["rescate"]  # despliegue preventivo
        return ["edan"] if p >= 0.35 else []
    n = []
    if not z.rescate_hecho and (z.colapso or z.senales_vida > 0):
        n.append("rescate")
    if z.heridos > 0:
        n.append("aph")
    return n
