"""Lee el receptor LoRa por puerto serie y envía reportes y latidos a la API local de TRIA.

Uso:
    pip install pyserial requests
    python herramientas/puente_serial.py --puerto COM3          (Windows)
    python herramientas/puente_serial.py --puerto /dev/ttyUSB0  (Linux)

Sin hardware se puede probar con --simular, que escribe mensajes de ejemplo.
"""
import argparse
import json
import time

import requests

API = "http://localhost:8000"


def procesar(linea: str) -> None:
    dato = json.loads(linea)
    partes = dato["msg"].split(",")
    if partes[0] == "R":
        _, zona, color, personas, *_ = partes
        r = requests.post(f"{API}/reportes", json={"zona": zona, "color": color,
                                                  "personas": int(personas), "canal": "baliza"})
        print("Reporte", zona, color, personas, "->", r.status_code)
    elif partes[0] == "L":
        requests.post(f"{API}/latidos", json={"zona": partes[1], "vivo": True})
        print("Latido", partes[1])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--puerto")
    ap.add_argument("--simular", action="store_true")
    args = ap.parse_args()

    if args.simular:
        for linea in ['{"msg":"L,CRI,3900,1","rssi":-98,"snr":7}',
                      '{"msg":"R,REG,rojo,40,3850,2","rssi":-112,"snr":-3}']:
            procesar(linea)
            time.sleep(1)
        return

    import serial  # pyserial
    with serial.Serial(args.puerto, 115200, timeout=1) as s:
        while True:
            linea = s.readline().decode(errors="ignore").strip()
            if linea.startswith("{"):
                try:
                    procesar(linea)
                except Exception as e:  # noqa: BLE001
                    print("Error:", e, linea)


if __name__ == "__main__":
    main()
