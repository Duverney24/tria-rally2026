/*
  TRIA – Baliza comunitaria LoRa
  Placa de referencia: ESP32 con radio SX1276 (por ejemplo TTGO LoRa32). Ajuste los pines a su placa.
  Librería: "LoRa" de Sandeep Mistry (Gestor de librerías de Arduino).

  Funcionamiento:
    - Botón PERSONAS: suma 5 personas por pulsación (el LED parpadea para confirmar).
    - Botones ROJO / AMARILLO / VERDE: envían el reporte con el conteo actual.
    - Latido automático cada LATIDO_MS: si el PMU deja de recibirlo, TRIA asume que la baliza
      fue destruida y eleva la urgencia de la zona.

  Formato del mensaje (texto corto para ahorrar aire):
    Reporte:  R,<zona>,<color>,<personas>,<bateria_mV>,<contador>
    Latido:   L,<zona>,<bateria_mV>,<contador>

  Frecuencia: banda ISM de 915 MHz. Verifique la regulación vigente de la ANE antes de desplegar.
*/
#include <SPI.h>
#include <LoRa.h>

// ---- Configuración de la baliza ----
const char* ZONA = "BRU";            // código de la vereda
const long FRECUENCIA = 915E6;
const unsigned long LATIDO_MS = 5UL * 60UL * 1000UL;  // 5 minutos

// ---- Pines (TTGO LoRa32 v1; cambie según su placa) ----
#define LORA_SCK 5
#define LORA_MISO 19
#define LORA_MOSI 27
#define LORA_SS 18
#define LORA_RST 14
#define LORA_DIO0 26
#define BTN_ROJO 13
#define BTN_AMARILLO 12
#define BTN_VERDE 15
#define BTN_PERSONAS 2
#define LED 25
#define PIN_BATERIA 35

int personas = 0;
unsigned long contador = 0;
unsigned long ultimoLatido = 0;

int bateria_mV() {
  return analogReadMilliVolts(PIN_BATERIA) * 2;  // divisor 1:2 típico
}

void parpadear(int veces) {
  for (int i = 0; i < veces; i++) {
    digitalWrite(LED, HIGH); delay(120);
    digitalWrite(LED, LOW); delay(120);
  }
}

void enviar(const String& msg) {
  LoRa.beginPacket();
  LoRa.print(msg);
  LoRa.endPacket();
  contador++;
}

void reportar(const char* color) {
  // Se envía 3 veces con pausa aleatoria para aumentar la probabilidad de recepción.
  String msg = String("R,") + ZONA + "," + color + "," + personas + "," + bateria_mV() + "," + contador;
  for (int i = 0; i < 3; i++) {
    enviar(msg);
    delay(random(800, 2500));
  }
  parpadear(3);
}

bool pulsado(int pin) {
  if (digitalRead(pin) == LOW) {
    delay(40);
    if (digitalRead(pin) == LOW) {
      while (digitalRead(pin) == LOW) delay(10);
      return true;
    }
  }
  return false;
}

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  int botones[] = {BTN_ROJO, BTN_AMARILLO, BTN_VERDE, BTN_PERSONAS};
  for (int b : botones) pinMode(b, INPUT_PULLUP);

  SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, LORA_SS);
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(FRECUENCIA)) {
    Serial.println("Error iniciando LoRa");
    while (true) parpadear(1);
  }
  LoRa.setSpreadingFactor(10);   // más alcance a cambio de menos velocidad
  LoRa.setSignalBandwidth(125E3);
  LoRa.enableCrc();
  randomSeed(esp_random());
  parpadear(2);
}

void loop() {
  if (pulsado(BTN_PERSONAS)) { personas += 5; parpadear(1); }
  if (pulsado(BTN_ROJO)) reportar("rojo");
  if (pulsado(BTN_AMARILLO)) reportar("amarillo");
  if (pulsado(BTN_VERDE)) reportar("verde");

  if (millis() - ultimoLatido > LATIDO_MS) {
    enviar(String("L,") + ZONA + "," + bateria_mV() + "," + contador);
    ultimoLatido = millis();
  }
}
