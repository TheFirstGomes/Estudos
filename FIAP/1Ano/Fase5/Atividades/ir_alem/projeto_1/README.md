# FarmTech Solutions — Classificação de Saúde de Plantações com ESP32 + ML
### FIAP · Fase 5 · Ir Além · Opção 2

---

## Visão Geral

Este projeto implementa um sistema de **Machine Learning embarcado** que classifica em tempo real se uma plantação de **alface** está **Saudável** ou **Não saudável**, utilizando dados coletados por sensores físicos conectados a um **ESP32**.

O sistema é composto por dois blocos:

| Bloco | Tecnologia | Responsabilidade |
|---|---|---|
| **Firmware** | C++ (Arduino) | Lê sensores, exibe no OLED, se comunica com Python via Serial |
| **ML / Backend** | Python + Scikit-learn | Treina modelo, classifica em tempo real, registra histórico |

---

## Por que Alface?

A **alface** (*Lactuca sativa*) foi escolhida por:

- Ser extremamente sensível a variações de temperatura e umidade — pequenas variações causam impacto visual rápido, facilitando validação
- Ter parâmetros ideais bem documentados na literatura agrícola
- Ser compatível com sensores de baixo custo (DHT11)
- Ciclo curto (~45 dias) → monitoramento contínuo é crítico para garantir produtividade

---

## Sensores Utilizados e Justificativa Técnica

| Sensor | Variável Medida | Pino ESP32 | Justificativa |
|---|---|---|---|
| **DHT11** | Temperatura (°C) + Umidade (%) | GPIO 4 | Variáveis com maior impacto na saúde da alface; sensor digital confiável para aplicações de campo |
| **Photosensitive Resistor** | Luminosidade (ADC 0–4095) | GPIO 34 | A luz é fator determinante na fotossíntese; valores extremos (baixo ou alto) indicam condições adversas |

### Condições Ideais — Alface

| Variável | Faixa Saudável | Faixa de Alerta |
|---|---|---|
| Temperatura | 15–25 °C | < 10 °C ou > 30 °C |
| Umidade relativa | 60–80 % | < 40 % ou > 90 % |
| Luminosidade (ADC) | 1000–3000 | < 500 ou > 3500 |

---

## Arquitetura do Sistema

```
┌──────────────────────────────────────────────────────────┐
│                   HARDWARE (ESP32)                       │
│                                                          │
│  ┌──────────┐   ┌──────────────────┐   ┌─────────────┐  │
│  │  DHT11   │   │  Photosensitive  │   │  OLED 0.96" │  │
│  │Temp+Umid │   │  Resistor (LDR)  │   │  SSD1306    │  │
│  └────┬─────┘   └────────┬─────────┘   └──────┬──────┘  │
│       │ GPIO4            │ GPIO34 (ADC)        │ I2C     │
│       └──────────────────┴─────────────────────┘         │
│                          │                               │
│               ┌──────────┴──────────┐                   │
│               │     ESP32 Dev Board  │                   │
│               │  JSON via Serial USB │                   │
│               └──────────┬──────────┘                   │
│                          │ USB                           │
└──────────────────────────┼───────────────────────────────┘
                           │ Serial 9600 baud
┌──────────────────────────┼───────────────────────────────┐
│                   SOFTWARE (Python)                      │
│                          │                               │
│               ┌──────────┴──────────┐                   │
│               │ inferencia_tempo_    │                   │
│               │ real.py             │                   │
│               │  • Lê JSON do ESP32  │                   │
│               │  • Carrega modelo   │                   │
│               │  • Classifica       │                   │
│               │  • Envia "1" ou "0" │                   │
│               │  • Salva histórico  │                   │
│               └──────────┬──────────┘                   │
│                          │                               │
│               ┌──────────┴──────────┐                   │
│               │  data/modelo.pkl    │                   │
│               │  (Random Forest /   │                   │
│               │   melhor modelo)    │                   │
│               └─────────────────────┘                   │
└──────────────────────────────────────────────────────────┘
```

**Fluxo de dados:**
```
Sensores → ESP32 → JSON Serial → Python ML → "1"/"0" → ESP32 → OLED + LED
```

---

## Estrutura do Repositório

```
ir_alem/
├── esp32/
│   └── esp32_sensor.ino           # Firmware ESP32 (C++ / Arduino)
├── python/
│   ├── gerar_dados_treino.py      # Gerador de dataset sintético rotulado
│   ├── treinar_modelo.py          # Treina e avalia 5 classificadores
│   ├── inferencia_tempo_real.py   # Inferência via Serial + log CSV
│   └── requirements.txt           # Dependências Python
├── data/
│   ├── sensor_data.csv            # Dataset gerado (criado automaticamente)
│   ├── modelo.pkl                 # Modelo salvo (criado automaticamente)
│   ├── historico_tempo_real.csv   # Log das inferências reais
│   ├── confusion_matrix.png       # Visualização — matriz de confusão
│   ├── roc_curves.png             # Visualização — curvas ROC
│   ├── comparativo_acuracia.png   # Visualização — comparativo de modelos
│   └── feature_importance.png     # Visualização — importância das features
└── README.md                      # Este arquivo
```

---

## Modelos de Machine Learning

Foram treinados e comparados **5 classificadores** usando Scikit-learn:

| # | Modelo | Tipo | Motivo da escolha |
|---|---|---|---|
| 1 | Regressão Logística | Linear | Baseline interpretável |
| 2 | K-Nearest Neighbors | Instance-based | Sem pressupostos sobre distribuição |
| 3 | SVM (kernel RBF) | Kernel | Boa separação em espaços não-lineares |
| 4 | Random Forest | Ensemble (Bagging) | Robusto, resistente a overfitting |
| 5 | Gradient Boosting | Ensemble (Boosting) | Alta performance preditiva |

Todos os modelos são encapsulados em `Pipeline` com `StandardScaler` para normalização.

### Métricas Avaliadas

- **Acurácia** — proporção de classificações corretas
- **AUC-ROC** — capacidade discriminativa (1.0 = perfeito)
- **Cross-Validation 5-fold** — estimativa de generalização
- **Precision / Recall / F1** por classe
- **Matriz de Confusão**

O modelo com maior **AUC-ROC** é salvo automaticamente como `data/modelo.pkl`.

---

## Como Executar

### 1. Instalar dependências Python

```bash
pip install -r python/requirements.txt
```

### 2. Gravar o firmware no ESP32

1. Abra o Arduino IDE
2. Instale as bibliotecas (via Library Manager):
   - `DHT sensor library` (Adafruit)
   - `Adafruit SSD1306`
   - `Adafruit GFX Library`
   - `ArduinoJson`
3. Abra `esp32/esp32_sensor.ino`
4. Selecione a placa: **ESP32 Dev Module**
5. Grave no ESP32

### 3. Montar o circuito

```
DHT11
  VCC → 3.3V
  GND → GND
  DATA → GPIO 4

Photosensitive Resistor Module
  VCC → 3.3V
  GND → GND
  AO (analog out) → GPIO 34

OLED SSD1306 (I2C)
  VCC → 3.3V
  GND → GND
  SDA → GPIO 21
  SCL → GPIO 22

LED Verde  → GPIO 26 → Resistor 220Ω → GND
LED Vermelho → GPIO 27 → Resistor 220Ω → GND
```

### 4. Treinar o modelo

```bash
# Gera o dataset sintético (1200 amostras, balanceado)
python python/gerar_dados_treino.py

# Treina os 5 modelos, avalia e salva o melhor em data/modelo.pkl
python python/treinar_modelo.py
```

### 5. Executar inferência em tempo real

```bash
# Detecta a porta automaticamente
python python/inferencia_tempo_real.py

# Ou especifica a porta manualmente
python python/inferencia_tempo_real.py --porta COM3       # Windows
python python/inferencia_tempo_real.py --porta /dev/ttyUSB0  # Linux

# Listar portas disponíveis
python python/inferencia_tempo_real.py --listar
```

O terminal exibirá as leituras em tempo real:

```
Horário              Temp (°C)    Umid (%)     Luz (ADC)    Classificação
---------------------------------------------------------------------------
2025-10-01 14:23:01  21.5         68.0         1850         SAUDÁVEL ✓
2025-10-01 14:23:06  34.2         45.0         3100         NÃO SAUDÁVEL ✗
```

---

## Dataset Sintético — Metodologia

Por não ser possível coletar meses de dados rotulados antes da entrega, o dataset de treino foi **gerado sinteticamente** com base em parâmetros agrícolas documentados para alface, com ruído gaussiano para simular variações reais.

| Classe | Cenário | Temperatura | Umidade | Luz (ADC) |
|---|---|---|---|---|
| Saudável | Condição ideal | 15–25 °C | 60–80 % | 1000–3000 |
| Não saudável | Calor excessivo | > 30 °C | variável | variável |
| Não saudável | Frio excessivo | < 10 °C | variável | variável |
| Não saudável | Seca | variável | < 40 % | variável |
| Não saudável | Excesso de umidade | variável | > 90 % | variável |

O modelo é **validado com dados reais** coletados pelo ESP32 durante a inferência em tempo real, confirmando ou rejeitando as hipóteses aprendidas.

---

## Saída do Sistema

### No OLED do ESP32

```
  FarmTech ML
─────────────────
Temp : 21.5 C
Umid : 68.0 %
Luz  : 1850
─────────────────
SAUDAVEL
```

### LEDs
- **Verde aceso** → Plantação Saudável
- **Vermelho aceso** → Plantação Não Saudável

---

## Grupo

> Projeto desenvolvido para a disciplina de Machine Learning — FIAP · Fase 5
