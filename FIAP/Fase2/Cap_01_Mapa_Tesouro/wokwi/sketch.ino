#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// =================== DEBUG ===================
#define DEBUG_WEATHER 1  // 0=desliga logs extras, 1=liga

// ====== Wi-Fi (Wokwi) ======
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";

// ====== OpenWeather (5 day / 3 hour forecast - grátis) ======
const char* OWM_API_KEY = "9097d4adc560cc1bd95f14584949b647";
const char* OWM_BASE    = "https://api.openweathermap.org/data/2.5/forecast";
const float LAT = -23.55;  // ajuste para sua região
const float LON = -46.63;  // ajuste para sua região
const char* OWM_PARAMS = "&units=metric&lang=pt_br";

// Frequência de busca e validade dos dados
const unsigned long WX_PERIOD_MS = 15UL * 60UL * 1000UL; // 15 min
const unsigned long WX_TTL_MS    = 3UL  * 60UL * 60UL * 1000UL; // 3h

// Limiares meteo p/ bloquear irrigação
const float WX_POP_BLOCK  = 0.60f; // prob. de precipitação (>= 60%)
const float WX_RAIN_BLOCK = 2.0f;  // chuva prevista nas próximas 3h (mm/3h)

// ====== Pinos ======
#define PIN_DHT      4
#define DHT_TYPE     DHT22
#define PIN_LDR_AO   34
#define PIN_RELAY    25
#define PIN_N        14
#define PIN_P        27
#define PIN_K        26
const bool RELAY_ACTIVE_HIGH = true;

DHT dht(PIN_DHT, DHT_TYPE);
bool pumpOn = false;

// ====== Estado meteorológico ======
float wx_pop = 0.0f;       // 0..1
float wx_rain_mm = 0.0f;   // mm acumulados nas próximas 3h
unsigned long wx_last_update = 0;

// ====== Cultura (ex.: tomate) ======
const float PH_MIN  = 6.0f;
const float PH_MAX  = 6.8f;
const float HUM_ON  = 35.0f; // liga abaixo
const float HUM_OFF = 45.0f; // desliga acima (histerese)

// ====== Utilitários ======
float mapADCToPH(int adc) {
  if (adc < 0) adc = 0;
  if (adc > 4095) adc = 4095;
  return (adc / 4095.0f) * 14.0f;
  // Se quiser inverter a relação com luz:
  // return 14.0f - (adc / 4095.0f) * 14.0f;
}

void setPump(bool on) {
  pumpOn = on;
  if (RELAY_ACTIVE_HIGH) digitalWrite(PIN_RELAY, on ? HIGH : LOW);
  else                   digitalWrite(PIN_RELAY, on ? LOW  : HIGH);
}

bool weatherBlocksIrrigation() {
  // Sem dado recente -> não bloqueia
  if (millis() - wx_last_update > WX_TTL_MS) return false;
  if (wx_pop     >= WX_POP_BLOCK)  return true;
  if (wx_rain_mm >= WX_RAIN_BLOCK) return true;
  return false;
}

bool ensureWifi() {
  if (WiFi.status() == WL_CONNECTED) return true;
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  unsigned long t0 = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - t0 < 8000) {
    delay(250);
  }
  return WiFi.status() == WL_CONNECTED;
}

bool fetchWeather() {
  if (!ensureWifi()) {
    Serial.println("[WX] Wi-Fi indisponível");
    return false;
  }

  String url = String(OWM_BASE) + "?lat=" + String(LAT, 6) + "&lon=" + String(LON, 6)
             + OWM_PARAMS + "&appid=" + OWM_API_KEY;

  HTTPClient http;
  http.begin(url);
  http.setTimeout(8000);
  int code = http.GET();

  Serial.print("[WX] HTTP status: "); Serial.println(code);

  if (code != HTTP_CODE_OK) {
    #if DEBUG_WEATHER
      // Mascarar a API key na URL ao logar
      String urlMask = url;
      int i = urlMask.indexOf("appid=");
      if (i >= 0) { int j = urlMask.indexOf('&', i); if (j < 0) j = urlMask.length();
        urlMask.replace(urlMask.substring(i+6, j), "****");
      }
      Serial.print("[WX] URL="); Serial.println(urlMask);
    #endif
    http.end();
    return false;
  }

  #if DEBUG_WEATHER
    Serial.print("[WX] Content-Type: "); Serial.println(http.header("Content-Type"));
    Serial.print("[WX] Content-Length: "); Serial.println(http.getSize());
  #endif

  DynamicJsonDocument doc(24 * 1024);
  DeserializationError err = deserializeJson(doc, http.getStream());
  http.end();
  if (err) {
    Serial.print("[WX] JSON erro: "); Serial.println(err.c_str());
    return false;
  }

  // Forecast 3h: usar list[0]
  float pop  = 0.0f;
  float rain = 0.0f;
  long  dt0  = 0;

  if (doc.containsKey("list") && doc["list"].size() > 0) {
    JsonObject f0 = doc["list"][0];
    if (f0.containsKey("pop")) pop = f0["pop"].as<float>();
    if (f0.containsKey("rain") && f0["rain"].containsKey("3h"))
      rain = f0["rain"]["3h"].as<float>();
    dt0 = f0["dt"] | 0;
  }

  wx_pop = pop;          // 0..1
  wx_rain_mm = rain;     // mm/3h
  wx_last_update = millis();

  Serial.print("[WX] OK (3h): pop=");  Serial.print(wx_pop, 2);
  Serial.print("  rain3h=");           Serial.print(wx_rain_mm, 2);
  Serial.print("  dt=");               Serial.println(dt0);

  return true;
}

// ====== Agendamento simples ======
unsigned long last_fetch = 0;

void setup() {
  Serial.begin(115200);
  dht.begin();
  analogReadResolution(12);

  pinMode(PIN_RELAY, OUTPUT);
  setPump(false);

  pinMode(PIN_N, INPUT_PULLUP);
  pinMode(PIN_P, INPUT_PULLUP);
  pinMode(PIN_K, INPUT_PULLUP);

  WiFi.mode(WIFI_STA);

  Serial.println("=== Irrigacao + OpenWeather (forecast 3h) ===");
  Serial.println("Bloqueia irrigacao se pop>=0.60 ou chuva3h>=2.0 mm\n");
}

void loop() {
  // 1) Atualiza meteo periodicamente
  if (millis() - last_fetch > WX_PERIOD_MS || wx_last_update == 0) {
    if (fetchWeather()) last_fetch = millis();
    else                last_fetch = millis() + 5000; // retry curto
  }

  // 2) Leituras locais
  const int   adc = analogRead(PIN_LDR_AO);
  const float ph  = mapADCToPH(adc);
  const float hum = dht.readHumidity();

  const bool N_ok = (digitalRead(PIN_N) == LOW);
  const bool P_ok = (digitalRead(PIN_P) == LOW);
  const bool K_ok = (digitalRead(PIN_K) == LOW);
  const bool npk_ok = N_ok && P_ok && K_ok;

  // 3) Decisão determinística (como combinado)
  const bool wx_block = weatherBlocksIrrigation();

  if (!isnan(hum)) {
    const bool ph_ok = (ph >= PH_MIN && ph <= PH_MAX);

    if (!pumpOn) {
      if (!wx_block && (hum < HUM_ON) && ph_ok && npk_ok) setPump(true);
    } else {
      if (wx_block || (hum > HUM_OFF) || !ph_ok || !npk_ok) setPump(false);
    }
  } else {
    Serial.println("[WARN] DHT22 NaN. Mantendo estado.");
  }

  // 4) Logs (inclui idade do dado meteo)
  unsigned long age = (wx_last_update == 0) ? 0 : (millis() - wx_last_update);

  Serial.print("Umid="); Serial.print(isnan(hum) ? -1 : hum); Serial.print("%  ");
  Serial.print("pH~=");  Serial.print(ph, 2); Serial.print("  ");
  Serial.print("N="); Serial.print(N_ok); Serial.print(" P="); Serial.print(P_ok); Serial.print(" K="); Serial.print(K_ok);
  Serial.print("  WX(pop="); Serial.print(wx_pop,2);
  Serial.print(", rain3h="); Serial.print(wx_rain_mm,2);
  Serial.print(", block=");  Serial.print(wx_block ? "1" : "0");
  Serial.print(", age_ms="); Serial.print(age);
  Serial.print(")  Pump="); Serial.println(pumpOn ? "ON" : "OFF");

  delay(800);
}
