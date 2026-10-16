"""Grafo vial: rutas más cortas evitando las vías caídas."""
from __future__ import annotations

import networkx as nx


class RedVial:
    def __init__(self, vias: list[dict]):
        """vias: [{"a": "PMU", "b": "CEN", "minutos": 4, "nombre": "..."}, ...]"""
        self.g = nx.Graph()
        for v in vias:
            self.g.add_edge(v["a"], v["b"], minutos=v["minutos"], nombre=v.get("nombre", ""), caida=False)

    def marcar_caida(self, a: str, b: str, caida: bool = True) -> None:
        self.g[a][b]["caida"] = caida

    def _transitable(self) -> nx.Graph:
        return nx.subgraph_view(self.g, filter_edge=lambda a, b: not self.g[a][b]["caida"])

    def ruta(self, origen: str, destino: str) -> tuple[list[str], float] | None:
        """Devuelve (camino, minutos) o None si no hay ruta terrestre."""
        try:
            g = self._transitable()
            camino = nx.shortest_path(g, origen, destino, weight="minutos")
            minutos = nx.path_weight(g, camino, weight="minutos")
            return camino, minutos
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def tiempos_desde(self, origen: str) -> dict[str, float]:
        return nx.single_source_dijkstra_path_length(self._transitable(), origen, weight="minutos")
