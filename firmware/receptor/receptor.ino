/*
  TRIA – Receptor del Puesto de Mando (o repetidor en un punto alto)
  Recibe los mensajes LoRa de las balizas y los imprime por puerto serie como una línea JSON.
  El script herramientas/puente_serial.py los lee y los envía a la API local de TRIA.

  Modo repetidor: con REPETIDOR = true, retransmite cada mensaje una vez (malla simple
  de un salto). Use un repetidor en lomas o torres para rodear montañas.
*/
#include <SPI.h>
#include <LoRa.h>

const long FRECUENCIA = 915E6;
const bool REPETIDOR = false;

#define LORA_SCK 5
#define LORA_MISO 19
#define LORA_MOSI 27
#define LORA_SS 18
#define LORA_RST 14
#define LORA_DIO0 26

String ultimo = "";

void setup() {
  Serial.begin(115200);
  SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, LORA_SS);
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(FRECUENCIA)) {
    Serial.println("{\"error\":\"LoRa\"}");
    while (true) delay(1000);
  }
  LoRa.setSpreadingFactor(10);
  LoRa.setSignalBandwidth(125E3);
  LoRa.enableCrc();
}

void loop() {
  int tam = LoRa.parsePacket();
  if (!tam) return;
  String msg = "";
  while (LoRa.available()) msg += (char)LoRa.read();
  if (msg == ultimo) return;  // descarta duplicados (la baliza repite 3 veces)
  ultimo = msg;

  Serial.print("{\"msg\":\"");
  Serial.print(msg);
  Serial.print("\",\"rssi\":");
  Serial.print(LoRa.packetRssi());
  Serial.print(",\"snr\":");
  Serial.print(LoRa.packetSnr());
  Serial.println("}");

  if (REPETIDOR && !msg.endsWith(",rep")) {
    delay(random(200, 900));
    LoRa.beginPacket();
    LoRa.print(msg + ",rep");
    LoRa.endPacket();
  }
}
