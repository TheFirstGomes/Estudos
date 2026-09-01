"""
FarmTech Solutions — Gerador de Dados de Treino Sintéticos
FIAP · Fase 5 · Ir Além

Cultura avaliada: Alface (Lactuca sativa)

Por que Alface?
  - Cultura muito sensível a variações de temperatura e umidade
  - Parâmetros ideais bem documentados na literatura agrícola
  - Ciclo curto (~45 dias) → monitoramento contínuo é crítico
  - Compatível com a escala da fazenda descrita no projeto principal

Condições ideais para Alface (baseado em literatura agrícola):
  Temperatura : 15–25 °C  (ótimo: 18–22 °C)
  Umidade     : 60–80 %   (ótimo: 65–75 %)
  Luz (ADC)   : 1000–3000 (luz moderada; ADC 12-bit do ESP32: 0-4095)

Este script gera um dataset sintético rotulado para treinar o modelo,
simulando leituras reais do DHT11 e do fotorresistor no ESP32.
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ── Configuração do gerador ───────────────────────────────────────────────────
SEED         = 42
N_SAUDAVEL   = 600   # amostras da classe "saudável"
N_N_SAUDAVEL = 600   # amostras da classe "não saudável"

rng = np.random.default_rng(SEED)

# ─────────────────────────────────────────────────────────────────────────────
def gerar_saudavel(n: int) -> pd.DataFrame:
    """
    Gera amostras dentro das condições ideais da alface, com ruído
    gaussiano para simular variações naturais do ambiente.
    """
    temp     = rng.normal(loc=20.0, scale=2.5, size=n).clip(15, 25)
    umidade  = rng.normal(loc=70.0, scale=5.0, size=n).clip(60, 80)
    luz      = rng.normal(loc=2000, scale=400,  size=n).clip(1000, 3000).astype(int)
    rotulo   = np.ones(n, dtype=int)  # 1 = saudável

    return pd.DataFrame({
        "temperatura_c": np.round(temp, 1),
        "umidade_pct":   np.round(umidade, 1),
        "luz_adc":       luz,
        "saudavel":      rotulo,
    })


def gerar_n_saudavel(n: int) -> pd.DataFrame:
    """
    Gera amostras fora das condições ideais, cobrindo quatro cenários
    de estresse:
      1. Calor excessivo (> 30 °C) — queima foliar
      2. Frio excessivo (< 10 °C) — retardo de crescimento
      3. Seca      (< 40 % umid.) — murcha e queima de bordas
      4. Excesso de umidade (> 90 %) — doenças fúngicas
    """
    n_por_cenario = n // 4
    dfs = []

    # Cenário 1: calor
    t = rng.normal(loc=33.0, scale=2.0, size=n_por_cenario).clip(30, 42)
    h = rng.normal(loc=55.0, scale=8.0, size=n_por_cenario).clip(20, 80)
    l = rng.integers(500, 4095, size=n_por_cenario)
    dfs.append(pd.DataFrame({"temperatura_c": np.round(t, 1),
                              "umidade_pct": np.round(h, 1),
                              "luz_adc": l, "saudavel": 0}))

    # Cenário 2: frio
    t = rng.normal(loc=7.0, scale=2.0, size=n_por_cenario).clip(0, 10)
    h = rng.normal(loc=65.0, scale=8.0, size=n_por_cenario).clip(40, 90)
    l = rng.integers(200, 2500, size=n_por_cenario)
    dfs.append(pd.DataFrame({"temperatura_c": np.round(t, 1),
                              "umidade_pct": np.round(h, 1),
                              "luz_adc": l, "saudavel": 0}))

    # Cenário 3: seca
    t = rng.normal(loc=22.0, scale=3.0, size=n_por_cenario).clip(12, 32)
    h = rng.normal(loc=30.0, scale=5.0, size=n_por_cenario).clip(10, 40)
    l = rng.integers(800, 3500, size=n_por_cenario)
    dfs.append(pd.DataFrame({"temperatura_c": np.round(t, 1),
                              "umidade_pct": np.round(h, 1),
                              "luz_adc": l, "saudavel": 0}))

    # Cenário 4: excesso de umidade
    t = rng.normal(loc=20.0, scale=3.0, size=n_por_cenario).clip(10, 30)
    h = rng.normal(loc=93.0, scale=3.0, size=n_por_cenario).clip(90, 100)
    l = rng.integers(300, 2000, size=n_por_cenario)
    dfs.append(pd.DataFrame({"temperatura_c": np.round(t, 1),
                              "umidade_pct": np.round(h, 1),
                              "luz_adc": l, "saudavel": 0}))

    return pd.concat(dfs, ignore_index=True)


# ── Geração e exportação ──────────────────────────────────────────────────────
df_saudavel   = gerar_saudavel(N_SAUDAVEL)
df_n_saudavel = gerar_n_saudavel(N_N_SAUDAVEL)

df = pd.concat([df_saudavel, df_n_saudavel], ignore_index=True)
df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)  # embaralha

# Salva na pasta data/
saida = Path(__file__).parent.parent / "data" / "sensor_data.csv"
saida.parent.mkdir(exist_ok=True)
df.to_csv(saida, index=False)

print(f"Dataset gerado: {len(df)} amostras → {saida}")
print(f"\nDistribuição das classes:")
print(df["saudavel"].value_counts().rename({1: "Saudável (1)", 0: "Não saudável (0)"}))
print(f"\nEstatísticas:\n{df.describe().round(2)}")
