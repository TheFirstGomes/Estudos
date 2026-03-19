# FarmTech Solutions — Monitor Wi-Fi de Plantação
### FIAP · Fase 5 · Ir Além · Opção 1 · Sistema de Coleta e Comunicação via ESP32

---

## Sobre o Projeto

Sistema embarcado que transforma o ESP32 em um **servidor HTTP** autônomo de monitoramento agrícola. Os sensores coletam temperatura, umidade e luminosidade em tempo real. Os dados são enviados via Wi-Fi e exibidos em um **dashboard HTML** acessível por qualquer dispositivo na mesma rede (celular, computador, tablet) — sem precisar de servidor externo.

**Cultura monitorada:** Alface (*Lactuca sativa*) — escolhida por ser altamente sensível a variações de temperatura e umidade, tornando o monitoramento contínuo crítico para a produção.

---

## Sensores Utilizados

| # | Sensor | Variável | Pino ESP32 | Justificativa |
|---|--------|----------|------------|---------------|
| 1 | **DHT11** | Temperatura (°C) e Umidade (%) | GPIO 4 | Captura diretamente as duas variáveis mais críticas para a saúde da alface. Simples, digital, incluso no kit. |
| 2 | **Fotorresistor (LDR)** | Luminosidade — ADC 12-bit (0–4095) | GPIO 34 | A luz é essencial para fotossíntese. Valores muito baixos indicam sombreamento excessivo; muito altos, estresse térmico por insolação. |

---

## Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────┐
│               Fazenda — Campo aberto                    │
│                                                         │
│  ┌──────────┐    ┌──────────┐                           │
│  │  DHT11   │    │   LDR    │                           │
│  │ Temp+Umid│    │   Luz    │                           │
│  └────┬─────┘    └────┬─────┘                           │
│       │               │                                 │
│       └──────┬────────┘                                 │
│              ▼                                          │
│     ┌─────────────────┐      ┌───────────────────┐     │
│     │     ESP32        │      │  OLED 0.96"       │     │
│     │  Servidor HTTP   │─────▶│  IP + leituras    │     │
│     │  porta 80        │      └───────────────────┘     │
│     │  GET /           │      ┌─────┐  ┌─────┐          │
│     │  GET /data (JSON)│─────▶│ LED │  │ LED │          │
│     └────────┬─────────┘      │Verde│  │Verm.│          │
│              │ Wi-Fi           └─────┘  └─────┘          │
└──────────────┼─────────────────────────────────────────-┘
               │
        Rede Wi-Fi local
               │
    ┌──────────▼──────────┐
    │  Navegador / Celular │
    │  http://IP_DO_ESP32  │
    │                      │
    │  ╔══════════════════╗│
    │  ║ FarmTech Monitor ║│
    │  ║  Temp:  22.5 °C  ║│
    │  ║  Umid:  68.0 %   ║│
    │  ║  Luz:   1840      ║│
    │  ║  ● SAUDAVEL       ║│
    │  ╚══════════════════╝│
    └──────────────────────┘
```

---

## Funcionalidades

- **Dashboard HTML auto-atualizado** — página servida pelo ESP32, atualiza os dados a cada 3 segundos via `fetch()` sem recarregar a página
- **Endpoint JSON** (`GET /data`) — retorna leituras no formato JSON, permitindo integração com outros sistemas
- **OLED 0.96"** — exibe IP da rede, temperatura, umidade, luz e status diretamente no circuito
- **LED Verde** (GPIO 26) — acende quando todas as condições estão dentro do ideal
- **LED Vermelho** (GPIO 27) — acende quando qualquer variável está fora da faixa saudável
- **Sem dependências externas** — 100% local, funciona sem internet, apenas Wi-Fi local

---

## Limiares de Saúde da Alface

| Variável | Faixa Saudável | Fora do Ideal |
|----------|---------------|---------------|
| Temperatura | 15–25 °C | < 15 °C (frio) ou > 25 °C (calor) |
| Umidade | 60–80 % | < 60 % (seca) ou > 80 % (fungo) |
| Luminosidade (ADC) | 1 000–3 000 | < 1 000 (sombra) ou > 3 000 (insolação) |

---

## Circuito — Pinagem

```
ESP32               Componente
─────────────────────────────────────────
GPIO 4          →   DHT11 (DATA)
GPIO 34         →   Fotorresistor (AO)
GPIO 26         →   LED Verde (anodo + resistor 220Ω)
GPIO 27         →   LED Vermelho (anodo + resistor 220Ω)
GPIO 21 (SDA)   →   OLED SDA
GPIO 22 (SCL)   →   OLED SCL
3.3V / GND      →   Alimentação dos componentes
```

> **Nota:** O GPIO 34 é somente entrada (input-only) e não tem resistor pull-up interno — ideal para leitura analógica do fotorresistor.

---

## Instalação e Uso

### 1. Bibliotecas necessárias (Arduino IDE)

Abra `Sketch > Include Library > Manage Libraries` e instale:

```
DHT sensor library        (Adafruit)
Adafruit Unified Sensor   (Adafruit)
Adafruit SSD1306          (Adafruit)
Adafruit GFX Library      (Adafruit)
ArduinoJson               (Benoit Blanchon)
```

A placa **ESP32** deve estar instalada via `File > Preferences > Additional Boards Manager URLs`:
```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

### 2. Configurar credenciais Wi-Fi

Abra `esp32/esp32_wifi_dashboard.ino` e edite as linhas:

```cpp
const char* WIFI_SSID     = "SEU_WIFI_AQUI";
const char* WIFI_PASSWORD = "SUA_SENHA_AQUI";
```

### 3. Gravar no ESP32

1. Conecte o ESP32 via USB
2. Selecione a placa: `Tools > Board > ESP32 Dev Module`
3. Selecione a porta: `Tools > Port > COMx`
4. Clique em **Upload**

### 4. Acessar o dashboard

Após o upload, abra o **Monitor Serial** (115200 baud). O ESP32 exibirá:

```
Wi-Fi conectado! IP: 192.168.1.XXX
Servidor HTTP iniciado na porta 80
Acesse: http://192.168.1.XXX
```

Abra o IP no navegador do celular ou computador (na mesma rede Wi-Fi) para ver o dashboard.

---

## Endpoint JSON

O endpoint `GET /data` retorna:

```json
{
  "temperatura": 22.5,
  "umidade": 68.0,
  "luz": 1840,
  "saudavel": true
}
```

Útil para integração com outros sistemas (Node-RED, Home Assistant, scripts Python etc.).

---

## Estrutura do Repositório

```
projeto_2/
├── esp32/
│   └── esp32_wifi_dashboard.ino   # Código-fonte do ESP32 (C++)
└── README.md                      # Esta documentação
```

---

## Grupo

> Projeto desenvolvido para a disciplina de Machine Learning — FIAP · Fase 5
> Luan Gonçalves Gomes - RM566806
