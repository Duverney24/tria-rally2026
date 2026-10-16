"""Pruebas de punta a punta de la API con el cliente de pruebas de FastAPI."""
import pytest
from fastapi.testclient import TestClient

from tria import api


@pytest.fixture()
def cliente(monkeypatch):
    monkeypatch.delenv("TRIA_CLAVE", raising=False)
    api.pmu = api.PuestoDeMando()  # estado limpio en cada prueba
    return TestClient(api.app)


def test_salud_y_estado(cliente):
    assert cliente.get("/salud").json()["ok"] is True
    est = cliente.get("/estado").json()
    assert est["requiere_clave"] is False and est["consistencia"] < 0.1


def test_reporte_cambia_las_prioridades(cliente):
    zona = cliente.get("/prioridades").json()[-1]["zona"]
    r = cliente.post("/reportes", json={"zona": zona, "color": "rojo", "personas": 80, "heridos": 9})
    assert r.status_code == 200
    fila = next(f for f in cliente.get("/prioridades").json() if f["zona"] == zona)
    assert fila["color"] == "rojo" and fila["personas"] == 80 and not fila["en_silencio"]


def test_validaciones(cliente):
    assert cliente.post("/reportes", json={"zona": "NOEXISTE", "color": "rojo"}).status_code == 404
    assert cliente.post("/reportes", json={"zona": "BRU", "color": "morado"}).status_code == 422


def test_clave_en_rutas_que_cambian_estado(cliente, monkeypatch):
    monkeypatch.setenv("TRIA_CLAVE", "abc")
    assert cliente.post("/reloj/30").status_code == 401
    assert cliente.post("/reloj/30", headers={"X-TRIA-Clave": "abc"}).status_code == 200
    assert cliente.get("/estado").json()["minuto"] == 30  # consultar sigue abierto


@pytest.mark.parametrize("origen,permitido", [
    ("https://tria-rally2026.vercel.app", True),
    ("https://tria-rally2026-git-main-riassds-projects.vercel.app", True),
    ("https://duverney24.github.io", True),
    ("http://localhost:5173", True),
    ("https://sitio-ajeno.com", False),
    ("https://vercel.app.sitio-ajeno.com", False),
])
def test_cors(cliente, origen, permitido):
    r = cliente.options("/reportes", headers={"Origin": origen, "Access-Control-Request-Method": "POST",
                                             "Access-Control-Request-Headers": "content-type,x-tria-clave"})
    assert (r.headers.get("access-control-allow-origin") == origen) is permitido


def test_config_entrega_la_clave_de_carto(cliente, monkeypatch):
    assert cliente.get("/config").json() == {"carto_key": ""}
    monkeypatch.setenv("TRIA_CARTO_KEY", "clave-de-prueba-123")
    assert cliente.get("/config").json()["carto_key"] == "clave-de-prueba-123"
