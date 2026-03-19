/*
 * FarmTech Solutions — Sistema de Coleta e Comunicação via Wi-Fi
 * FIAP · Fase 5 · Ir Além · Opção 1
 *
 * Sensores utilizados:
 *   1. DHT11  — Temperatura (ºC) e Umidade relativa (%) → GPIO 4
 *   2. LDR    — Luminosidade (ADC 12-bit, 0–4095)       → GPIO 34
 *
 * O ESP32 conecta ao Wi-Fi e sobe um servidor HTTP na porta 80.
 * Dois endpoints disponíveis:
 *   GET /       → dashboard HTML com auto-atualização via JavaScript
 *   GET /data   → JSON com leitura atual dos sensores
 *
 * Feedback visual:
 *   LED Verde (GPIO 26) — condições dentro do ideal para alface
 *   LED Vermelho (GPIO 27) — alguma condição está fora do ideal
 *   OLED 0.96" (I2C) — exibe IP, temperatura, umidade e luz
 *
 * Bibliotecas necessárias (instale pelo Library Manager da Arduino IDE):
 *   - DHT sensor library (Adafruit)
 *   - Adafruit Unified Sensor
 *   - Adafruit SSD1306
 *   - Adafruit GFX Library
 *   - ArduinoJson
 *   (WiFi e WebServer são nativas do ESP32)
 */

#include <WiFi.h>
#include <WebServer.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoJson.h>

// ── Credenciais Wi-Fi ─────────────────────────────────────────────────────────
// Altere para o nome e senha da sua rede antes de gravar no ESP32
const char* WIFI_SSID     = "SEU_WIFI_AQUI";
const char* WIFI_PASSWORD = "SUA_SENHA_AQUI";

// ── Definição de pinos ────────────────────────────────────────────────────────
#define DHT_PIN      4      // Pino de dados do DHT11
#define DHT_TYPE     DHT11  // Modelo do sensor
#define LDR_PIN      34     // Pino analógico do fotorresistor (ADC1_CH6)
#define LED_VERDE    26     // LED verde: condição saudável
#define LED_VERMELHO 27     // LED vermelho: condição crítica

// ── OLED 0.96" (128x64, I2C) ─────────────────────────────────────────────────
#define OLED_WIDTH   128
#define OLED_HEIGHT  64
#define OLED_RESET   -1     // Sem pino de reset dedicado
#define OLED_ADDR    0x3C   // Endereço I2C padrão do SSD1306

// ── Limites de saúde para alface (Lactuca sativa) ────────────────────────────
// Baseados em literatura agrícola — usados para colorir o dashboard e LEDs
#define TEMP_MIN   15.0f
#define TEMP_MAX   25.0f
#define UMID_MIN   60.0f
#define UMID_MAX   80.0f
#define LUZ_MIN    1000
#define LUZ_MAX    3000

// ── Intervalo de leitura dos sensores (ms) ────────────────────────────────────
#define INTERVALO_LEITURA 3000

// ── Objetos globais ───────────────────────────────────────────────────────────
DHT             dht(DHT_PIN, DHT_TYPE);
WebServer       server(80);
Adafruit_SSD1306 oled(OLED_WIDTH, OLED_HEIGHT, &Wire, OLED_RESET);

// ── Variáveis compartilhadas (leitura dos sensores) ───────────────────────────
float  g_temp    = 0.0f;
float  g_umidade = 0.0f;
int    g_luz     = 0;
bool   g_saudavel = false;
unsigned long g_ultima_leitura = 0;

// ═══════════════════════════════════════════════════════════════════════════════
// Dashboard HTML (servido em GET /)
// Auto-atualiza via fetch() a cada 3 segundos sem recarregar a página.
// ═══════════════════════════════════════════════════════════════════════════════
const char HTML_DASHBOARD[] PROGMEM = R"rawhtml(
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FarmTech — Monitor de Plantacao</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', sans-serif;
    background: #0d1117;
    color: #c9d1d9;
    min-height: 100vh;
    padding: 20px;
  }
  h1 { color: #58a6ff; font-size: 1.4rem; margin-bottom: 4px; }
  .subtitle { color: #8b949e; font-size: 0.85rem; margin-bottom: 24px; }
  .cards { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }
  .card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 20px 24px;
    flex: 1;
    min-width: 160px;
    text-align: center;
  }
  .card-label { font-size: 0.78rem; color: #8b949e; text-transform: uppercase;
                letter-spacing: 0.08em; margin-bottom: 8px; }
  .card-value { font-size: 2.2rem; font-weight: 700; line-height: 1; }
  .card-unit  { font-size: 0.85rem; color: #8b949e; margin-top: 4px; }
  .ok   { color: #2ecc71; }
  .warn { color: #e74c3c; }
  .neutral { color: #58a6ff; }
  .status-bar {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
  }
  .dot { width: 14px; height: 14px; border-radius: 50%; flex-shrink: 0; }
  .dot-ok   { background: #2ecc71; box-shadow: 0 0 8px #2ecc71; }
  .dot-warn { background: #e74c3c; box-shadow: 0 0 8px #e74c3c; }
  .status-text { font-size: 1rem; font-weight: 600; }
  .footer { color: #484f58; font-size: 0.75rem; text-align: center; }
  #last-update { color: #58a6ff; }
</style>
</head>
<body>
<h1>FarmTech Solutions — Monitor de Plantacao</h1>
<p class="subtitle">Alface (Lactuca sativa) · ESP32 + DHT11 + Fotorresistor · Dados em tempo real</p>

<div class="status-bar">
  <div class="dot" id="status-dot"></div>
  <span class="status-text" id="status-text">Carregando...</span>
</div>

<div class="cards">
  <div class="card">
    <div class="card-label">Temperatura</div>
    <div class="card-value" id="temp">--</div>
    <div class="card-unit">graus Celsius</div>
  </div>
  <div class="card">
    <div class="card-label">Umidade</div>
    <div class="card-value" id="umid">--</div>
    <div class="card-unit">% relativa</div>
  </div>
  <div class="card">
    <div class="card-label">Luminosidade</div>
    <div class="card-value neutral" id="luz">--</div>
    <div class="card-unit">ADC (0 - 4095)</div>
  </div>
</div>

<p class="footer">Ultima atualizacao: <span id="last-update">--</span> &nbsp;|&nbsp; Atualiza automaticamente a cada 3 segundos</p>

<script>
async function atualizar() {
  try {
    const r = await fetch('/data');
    const d = await r.json();

    document.getElementById('temp').textContent = d.temperatura.toFixed(1);
    document.getElementById('umid').textContent = d.umidade.toFixed(1);
    document.getElementById('luz').textContent  = d.luz;

    const tempEl = document.getElementById('temp');
    const umidEl = document.getElementById('umid');
    tempEl.className = 'card-value ' + (d.temperatura >= 15 && d.temperatura <= 25 ? 'ok' : 'warn');
    umidEl.className = 'card-value ' + (d.umidade >= 60    && d.umidade <= 80    ? 'ok' : 'warn');

    const dot  = document.getElementById('status-dot');
    const txt  = document.getElementById('status-text');
    if (d.saudavel) {
      dot.className = 'dot dot-ok';
      txt.textContent = 'SAUDAVEL — Condicoes dentro do ideal para alface';
      txt.style.color = '#2ecc71';
    } else {
      dot.className = 'dot dot-warn';
      txt.textContent = 'ATENCAO — Uma ou mais condicoes estao fora do ideal';
      txt.style.color = '#e74c3c';
    }

    const now = new Date();
    document.getElementById('last-update').textContent =
      now.toLocaleTimeString('pt-BR');
  } catch(e) {
    document.getElementById('status-text').textContent = 'Erro ao conectar com o ESP32';
  }
}

atualizar();
setInterval(atualizar, 3000);
</script>
</body>
</html>
)rawhtml";

// ═══════════════════════════════════════════════════════════════════════════════
// Handlers HTTP
// ═══════════════════════════════════════════════════════════════════════════════

// GET / → retorna o dashboard HTML
void handleRoot() {
  server.send_P(200, "text/html", HTML_DASHBOARD);
}

// GET /data → retorna JSON com leitura atual
void handleData() {
  StaticJsonDocument<128> doc;
  doc["temperatura"] = g_temp;
  doc["umidade"]     = g_umidade;
  doc["luz"]         = g_luz;
  doc["saudavel"]    = g_saudavel;

  String json;
  serializeJson(doc, json);

  // Cabeçalho CORS permite acesso de outros hosts se necessário
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", json);
}

// ═══════════════════════════════════════════════════════════════════════════════
// Leitura dos sensores
// ═══════════════════════════════════════════════════════════════════════════════
void lerSensores() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  int   l = analogRead(LDR_PIN);

  // isnan() detecta falha de leitura do DHT11
  if (!isnan(t) && !isnan(h)) {
    g_temp    = t;
    g_umidade = h;
  }
  g_luz = l;

  // Classifica saúde: todas as variáveis devem estar dentro do intervalo ideal
  g_saudavel = (g_temp    >= TEMP_MIN && g_temp    <= TEMP_MAX) &&
               (g_umidade >= UMID_MIN && g_umidade <= UMID_MAX) &&
               (g_luz     >= LUZ_MIN  && g_luz     <= LUZ_MAX);

  // Atualiza LEDs
  digitalWrite(LED_VERDE,    g_saudavel ? HIGH : LOW);
  digitalWrite(LED_VERMELHO, g_saudavel ? LOW  : HIGH);
}

// ═══════════════════════════════════════════════════════════════════════════════
// Atualiza OLED
// ═══════════════════════════════════════════════════════════════════════════════
void atualizarOLED() {
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);

  // Linha 0: título
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  oled.println("FarmTech Monitor");

  // Linha 1: temperatura
  oled.setCursor(0, 14);
  oled.print("Temp:  ");
  oled.print(g_temp, 1);
  oled.println(" C");

  // Linha 2: umidade
  oled.setCursor(0, 26);
  oled.print("Umid:  ");
  oled.print(g_umidade, 1);
  oled.println(" %");

  // Linha 3: luminosidade
  oled.setCursor(0, 38);
  oled.print("Luz:   ");
  oled.println(g_luz);

  // Linha 4: status
  oled.setCursor(0, 52);
  oled.setTextSize(1);
  oled.print(g_saudavel ? ">> SAUDAVEL" : "!! ATENCAO");

  oled.display();
}

// ═══════════════════════════════════════════════════════════════════════════════
// setup()
// ═══════════════════════════════════════════════════════════════════════════════
void setup() {
  Serial.begin(115200);

  // Pinos de saída
  pinMode(LED_VERDE,    OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);

  // Inicializa DHT11
  dht.begin();

  // Inicializa OLED
  if (!oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("[ERRO] OLED nao inicializado");
    // Continua sem o OLED — não é fatal
  } else {
    oled.clearDisplay();
    oled.setTextSize(1);
    oled.setTextColor(SSD1306_WHITE);
    oled.setCursor(0, 0);
    oled.println("FarmTech Solutions");
    oled.println("Conectando Wi-Fi...");
    oled.display();
  }

  // Conexão Wi-Fi
  Serial.printf("\nConectando a '%s'", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\nWi-Fi conectado! IP: %s\n", WiFi.localIP().toString().c_str());

  // Exibe IP no OLED
  oled.clearDisplay();
  oled.setCursor(0, 0);
  oled.println("Wi-Fi OK!");
  oled.print("IP: ");
  oled.println(WiFi.localIP().toString());
  oled.println("");
  oled.println("Abra no navegador:");
  oled.print("http://");
  oled.print(WiFi.localIP().toString());
  oled.display();

  // Registra endpoints HTTP
  server.on("/",     handleRoot);
  server.on("/data", handleData);
  server.begin();
  Serial.println("Servidor HTTP iniciado na porta 80");
  Serial.printf("Acesse: http://%s\n", WiFi.localIP().toString().c_str());
}

// ═══════════════════════════════════════════════════════════════════════════════
// loop()
// ═══════════════════════════════════════════════════════════════════════════════
void loop() {
  // Atende requisições HTTP — deve ser chamado frequentemente
  server.handleClient();

  // Lê sensores a cada INTERVALO_LEITURA ms (sem usar delay())
  unsigned long agora = millis();
  if (agora - g_ultima_leitura >= INTERVALO_LEITURA) {
    g_ultima_leitura = agora;
    lerSensores();
    atualizarOLED();

    // Log serial para depuração
    Serial.printf("[%lu ms] Temp: %.1f C | Umid: %.1f %% | Luz: %d | Status: %s\n",
                  agora, g_temp, g_umidade, g_luz,
                  g_saudavel ? "SAUDAVEL" : "ATENCAO");
  }
}
