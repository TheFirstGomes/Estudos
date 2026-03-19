/*
 * FarmTech Solutions — Classificação de Saúde de Plantações
 * FIAP · Fase 5 · Ir Além
 *
 * Hardware:
 *   - ESP32 Development Board
 *   - DHT11 (Temperatura e Umidade) → GPIO 4
 *   - Photosensitive Resistor Module (LDR) → GPIO 34 (ADC)
 *   - OLED 0.96" SSD1306 I2C → SDA=GPIO21, SCL=GPIO22
 *   - LED Verde (Saudável)   → GPIO 26
 *   - LED Vermelho (N. Saudável) → GPIO 27
 *
 * Comunicação: Serial USB 9600 baud — JSON enviado ao Python,
 *              resultado recebido como "1" (saudável) ou "0" (não saudável)
 *
 * Bibliotecas necessárias (instalar via Arduino Library Manager):
 *   - DHT sensor library (Adafruit)
 *   - Adafruit SSD1306
 *   - Adafruit GFX Library
 *   - ArduinoJson
 */

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include <ArduinoJson.h>

// ─── Pinos ────────────────────────────────────────────────
#define DHT_PIN      4       // Pino digital do DHT11
#define DHT_TYPE     DHT11   // Modelo do sensor
#define LDR_PIN      34      // Pino analógico do fotorresistor (ADC1)
#define LED_VERDE    26      // LED verde → plantação saudável
#define LED_VERMELHO 27      // LED vermelho → plantação não saudável

// ─── OLED ─────────────────────────────────────────────────
#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1     // Reset não utilizado (pino -1)
#define OLED_ADDRESS  0x3C   // Endereço I2C padrão do SSD1306

// ─── Instâncias ───────────────────────────────────────────
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
DHT dht(DHT_PIN, DHT_TYPE);

// ─── Intervalo de leitura ─────────────────────────────────
const unsigned long INTERVALO_MS   = 5000;  // Leitura a cada 5 segundos
const unsigned long TIMEOUT_MS     = 6000;  // Aguarda resposta Python por 6s

unsigned long ultimaLeitura = 0;

// ─────────────────────────────────────────────────────────
void setup() {
  Serial.begin(9600);

  // Configuração dos LEDs
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_VERMELHO, LOW);

  // Inicialização do DHT11
  dht.begin();

  // Inicialização do OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
    // Se falhar, pisca o LED vermelho indefinidamente como alerta
    while (true) {
      digitalWrite(LED_VERMELHO, HIGH);
      delay(300);
      digitalWrite(LED_VERMELHO, LOW);
      delay(300);
    }
  }

  // Tela de boas-vindas
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("  FarmTech ML");
  display.println("  FIAP - Fase 5");
  display.println();
  display.println("Cultura: Alface");
  display.println("Aguardando dados...");
  display.display();

  delay(2000);
}

// ─────────────────────────────────────────────────────────
void loop() {
  unsigned long agora = millis();

  // Respeita o intervalo entre leituras
  if (agora - ultimaLeitura < INTERVALO_MS) return;
  ultimaLeitura = agora;

  // ── Leitura do DHT11 ────────────────────────────────────
  float temperatura = dht.readTemperature();  // ºC
  float umidade     = dht.readHumidity();     // %

  if (isnan(temperatura) || isnan(umidade)) {
    exibirErro("Erro no DHT11");
    return;
  }

  // ── Leitura do LDR ──────────────────────────────────────
  // ADC de 12 bits: 0 (escuro) → 4095 (muito iluminado)
  int luz = analogRead(LDR_PIN);

  // ── Envia JSON ao Python via Serial ─────────────────────
  // Formato: {"temp":23.5,"humidity":65.0,"light":1800}
  StaticJsonDocument<128> docEnvio;
  docEnvio["temp"]     = temperatura;
  docEnvio["humidity"] = umidade;
  docEnvio["light"]    = luz;
  serializeJson(docEnvio, Serial);
  Serial.println();  // Finaliza linha para o Python detectar

  // ── Aguarda resposta do modelo Python ───────────────────
  unsigned long inicio = millis();
  String resultado = "";

  while (resultado.length() == 0) {
    if (millis() - inicio > TIMEOUT_MS) {
      exibirErro("Timeout Python");
      return;
    }
    if (Serial.available()) {
      resultado = Serial.readStringUntil('\n');
      resultado.trim();
    }
  }

  // ── Exibe resultado no OLED e acende LED ────────────────
  bool saudavel = (resultado == "1");
  exibirResultado(temperatura, umidade, luz, saudavel);
}

// ─── Exibe leitura + classificação no OLED ────────────────
void exibirResultado(float temp, float umid, int luz, bool saudavel) {
  display.clearDisplay();

  // Cabeçalho
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("  FarmTech ML");
  display.drawLine(0, 9, 127, 9, SSD1306_WHITE);

  // Dados do sensor
  display.setCursor(0, 12);
  display.print("Temp : ");
  display.print(temp, 1);
  display.println(" C");

  display.print("Umid : ");
  display.print(umid, 1);
  display.println(" %");

  display.print("Luz  : ");
  display.println(luz);

  display.drawLine(0, 42, 127, 42, SSD1306_WHITE);

  // Classificação em destaque
  display.setTextSize(2);
  display.setCursor(0, 48);

  if (saudavel) {
    display.println("SAUDAVEL");
    digitalWrite(LED_VERDE, HIGH);
    digitalWrite(LED_VERMELHO, LOW);
  } else {
    display.println("N.SAUDAVEL");
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_VERMELHO, HIGH);
  }

  display.display();
}

// ─── Exibe mensagem de erro no OLED ───────────────────────
void exibirErro(const char* msg) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("  FarmTech ML");
  display.println();
  display.println("ERRO:");
  display.println(msg);
  display.display();

  // Pisca ambos os LEDs como alerta de erro
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_VERDE, HIGH);
    digitalWrite(LED_VERMELHO, HIGH);
    delay(200);
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_VERMELHO, LOW);
    delay(200);
  }
}
