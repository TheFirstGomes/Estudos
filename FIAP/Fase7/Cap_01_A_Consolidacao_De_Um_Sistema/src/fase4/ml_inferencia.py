"""
Fase 4 — Dashboard Interativo com Data Science
Carrega os modelos Random Forest da Fase 4 e expõe funções de inferência
e geração de ações corretivas para o dashboard integrado.
"""

from pathlib import Path
import sys
_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))
from src.config import FASE4_MODELS, FASE4_TESTS, MODELS_DIR, TEST_DIR

import joblib
import pandas as pd
import numpy as np


# ── Resolução dos caminhos dos modelos ────────────────────────────────────────

def _localizar(nome_arquivo: str) -> Path:
    """Procura o arquivo primeiro na cópia local, depois na Fase 4 original."""
    local = MODELS_DIR / nome_arquivo
    if local.exists():
        return local
    original = FASE4_MODELS / nome_arquivo
    if original.exists():
        return original
    raise FileNotFoundError(
        f"Modelo '{nome_arquivo}' não encontrado em {MODELS_DIR} nem em {FASE4_MODELS}"
    )


def _localizar_test(nome: str) -> Path:
    local = TEST_DIR / nome
    if local.exists():
        return local
    return FASE4_TESTS / nome


# ── Carregamento lazy dos modelos ─────────────────────────────────────────────

_modelos: dict = {}


def _carregar_modelos() -> dict:
    global _modelos
    if _modelos:
        return _modelos
    _modelos = {
        "umidade":    joblib.load(_localizar("modelo_regressao_umidade.joblib")),
        "ph":         joblib.load(_localizar("modelo_regressao_ph.joblib")),
        "rendimento": joblib.load(_localizar("modelo_regressao_rendimento_esperado.joblib")),
    }
    return _modelos


# ── Features (mesma ordem do treinamento na Fase 4) ───────────────────────────

TODAS_FEATURES = [
    "umidade", "ph", "nitrogenio", "fosforo", "postassio",
    "probabilidade_precipitacao", "chuva_3h",
    "bloqueio_meteorológico", "estado_bomba", "mes", "hora",
]


def fazer_previsoes(entrada: dict) -> dict:
    """
    Recebe um dicionário com as features e retorna as três previsões.
    """
    modelos = _carregar_modelos()
    df = pd.DataFrame([entrada], columns=TODAS_FEATURES)

    # Cada modelo foi treinado sem a sua própria variável-alvo como feature.
    # O modelo de rendimento usa todas as 11 features (inclusive umidade e ph).
    feat_umid = [c for c in TODAS_FEATURES if c != "umidade"]
    feat_ph   = [c for c in TODAS_FEATURES if c != "ph"]
    feat_rend = TODAS_FEATURES  # rendimento_esperado não está em TODAS_FEATURES

    umid_pred = float(modelos["umidade"].predict(df[feat_umid])[0])
    ph_pred   = float(modelos["ph"].predict(df[feat_ph])[0])
    rend_pred = float(modelos["rendimento"].predict(df[feat_rend])[0])

    return {
        "umidade_prevista":    round(umid_pred, 2),
        "ph_previsto":         round(ph_pred, 3),
        "rendimento_previsto": round(rend_pred, 2),
    }


# ── Geração de ações (mesma lógica do dashboard_db.py da Fase 4) ──────────────

def gerar_acoes(umid: float, ph: float, rendimento: float) -> list[dict]:
    """Retorna lista de dicts com {nivel, icone, mensagem}."""
    acoes = []

    # Irrigação
    if umid < 40:
        acoes.append({"nivel": "critico", "icone": "💧",
                      "mensagem": f"IRRIGUE AGORA — umidade prevista {umid:.1f}% abaixo de 40%."})
    elif umid > 65:
        acoes.append({"nivel": "alerta", "icone": "🛑",
                      "mensagem": f"EVITE IRRIGAR — umidade prevista {umid:.1f}% acima de 65%."})
    else:
        acoes.append({"nivel": "ok", "icone": "✅",
                      "mensagem": f"Umidade ideal ({umid:.1f}%). Monitoramento contínuo."})

    # pH
    if ph < 5.5:
        acoes.append({"nivel": "alerta", "icone": "⚠️",
                      "mensagem": f"CORREÇÃO DE pH — solo muito ácido (pH {ph:.2f}). Aplicar calcário."})
    elif ph > 7.5:
        acoes.append({"nivel": "alerta", "icone": "⚠️",
                      "mensagem": f"CORREÇÃO DE pH — solo muito alcalino (pH {ph:.2f}). Aplicar enxofre."})
    else:
        acoes.append({"nivel": "ok", "icone": "✅",
                      "mensagem": f"pH {ph:.2f} ideal para a maioria das culturas."})

    # Rendimento
    if rendimento < 20:
        acoes.append({"nivel": "critico", "icone": "📉",
                      "mensagem": f"BAIXO RENDIMENTO ({rendimento:.1f}). Revise nutrientes e irrigação."})
    elif rendimento > 60:
        acoes.append({"nivel": "ok", "icone": "💰",
                      "mensagem": f"ALTO RENDIMENTO esperado ({rendimento:.1f}). Condições ótimas!"})

    return acoes


def carregar_dados_teste_rendimento() -> pd.DataFrame | None:
    """Carrega o CSV de teste para o gráfico de correlação."""
    try:
        x = pd.read_csv(_localizar_test("X_teste_rendimento_esperado.csv"))
        y = pd.read_csv(_localizar_test("y_teste_rendimento_esperado.csv"))
        df = x.copy()
        df["rendimento_esperado"] = y["rendimento_esperado"]
        return df
    except Exception:
        return None


if __name__ == "__main__":
    entrada = {
        "umidade": 38.0, "ph": 6.2, "nitrogenio": 1, "fosforo": 1, "postassio": 1,
        "probabilidade_precipitacao": 0.2, "chuva_3h": 0.5,
        "bloqueio_meteorológico": 0, "estado_bomba": 0, "mes": 10, "hora": 14,
    }
    prev = fazer_previsoes(entrada)
    print("Previsões:", prev)
    for a in gerar_acoes(prev["umidade_prevista"], prev["ph_previsto"], prev["rendimento_previsto"]):
        print(f"  {a['icone']} [{a['nivel'].upper()}] {a['mensagem']}")
