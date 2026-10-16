from tria.modelo import MATRIZ_AHP_EJEMPLO, Zona, indice_urgencia, pesos_ahp, probabilidad_grave
from tria.escenario import PuestoDeMando


def test_ahp_consistente():
    w, cr = pesos_ahp(MATRIZ_AHP_EJEMPLO)
    assert abs(sum(w) - 1) < 1e-9
    assert w[0] > w[1] > w[2] > w[3]
    assert cr < 0.10


def test_silencio_con_baliza_sube_con_el_tiempo():
    p0 = probabilidad_grave(0.4, 0)
    p60 = probabilidad_grave(0.4, 60)
    assert p60 > p0


def test_sin_medio_el_silencio_no_informa():
    assert abs(probabilidad_grave(0.4, 120, medio="ninguno") - 0.4) < 1e-9


def test_latido_perdido_eleva_mucho():
    assert probabilidad_grave(0.4, 0, latido=False) > 0.75


def test_zona_poblada_va_primero():
    w, _ = pesos_ahp(MATRIZ_AHP_EJEMPLO)
    grande = Zona("A", "A", 4800, 0.8, 0.55)
    chica = Zona("B", "B", 1100, 0.75, 0.2)
    assert indice_urgencia(grande, 60, w)[0] > indice_urgencia(chica, 60, w)[0]


def test_asignacion_sin_duplicar_y_con_vias_caidas():
    pmu = PuestoDeMando()
    pmu.zonas["BRU"].latido = False
    pmu.red.marcar_caida("CRI", "BRU")
    asig = pmu.asignacion()
    zonas_tipo = [(a["zona"], a["tipo"]) for a in asig]
    assert len(zonas_tipo) == len(set(zonas_tipo))
    equipos = [a["equipo"] for a in asig]
    assert len(equipos) == len(set(equipos))
    bru = [a for a in asig if a["zona"] == "BRU"]
    assert bru and "PAL" in bru[0]["ruta"]  # rodea por Palmarito


def test_prioridades_incluyen_estado_de_la_zona():
    pmu = PuestoDeMando()
    pmu.zonas["REG"].registrar_reporte(10, "rojo", 40, heridos=6)
    pmu.zonas["BRU"].latido = False
    filas = {f["zona"]: f for f in pmu.prioridades()}
    assert filas["REG"]["color"] == "rojo" and filas["REG"]["personas"] == 40 and filas["REG"]["heridos"] == 6
    assert not filas["REG"]["en_silencio"]
    assert filas["BRU"]["latido"] is False and filas["BRU"]["en_silencio"]
