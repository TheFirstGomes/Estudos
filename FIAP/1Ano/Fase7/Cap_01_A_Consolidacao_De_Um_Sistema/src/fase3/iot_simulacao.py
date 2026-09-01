"""
Fase 3 — IoT e Automação Inteligente
Simulação do ESP32 com sensores DHT22 (umidade), LDR (pH) e botões N/P/K.
Lógica de irrigação idêntica ao sketch.ino da Fase 2/Cap_01_Mapa_Tesouro.
"""

import random
import time
from datetime import datetime
from pathlib import Path

import sys
_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))
from src.config import (ALERT_UMIDADE_MIN, ALERT_UMIDADE_MAX,
                        ALERT_PH_MIN, ALERT_PH_MAX)


# ── Constantes do ESP32 (espelhadas do .ino) ─────────────────────────────────

PH_MIN   = 6.0   # ligar a bomba só se pH >= PH_MIN
PH_MAX   = 6.8   # ligar a bomba só se pH <= PH_MAX
HUM_ON   = 35.0  # liga a bomba abaixo deste valor
HUM_OFF  = 45.0  # desliga a bomba acima deste valor (histerese)

WX_POP_BLOCK  = 0.60   # prob. de chuva que bloqueia irrigação
WX_RAIN_BLOCK = 2.0    # mm/3h que bloqueia irrigação


# ── Simulação de sensores ─────────────────────────────────────────────────────

def _adc_to_ph(adc: int) -> float:
    """Converte leitura ADC 12-bit em pH (mesma fórmula do .ino)."""
    adc = max(0, min(4095, adc))
    return (adc / 4095.0) * 14.0


def ler_sensores(
    umidade_override: float = None,
    ph_override: float = None,
    n_ok: bool = None,
    p_ok: bool = None,
    k_ok: bool = None,
    prob_chuva: float = None,
    chuva_3h: float = None,
) -> dict:
    """
    Simula uma leitura do ESP32.
    Se os parâmetros forem None, gera valores aleatórios realistas.
    """
    umidade = umidade_override if umidade_override is not None \
        else round(random.uniform(20, 75), 1)

    adc = random.randint(1500, 2500)
    ph = ph_override if ph_override is not None else round(_adc_to_ph(adc), 2)

    n = n_ok if n_ok is not None else random.choice([True, False])
    p = p_ok if p_ok is not None else random.choice([True, False])
    k = k_ok if k_ok is not None else random.choice([True, False])

    pop     = prob_chuva if prob_chuva is not None else round(random.uniform(0, 1), 2)
    rain    = chuva_3h   if chuva_3h   is not None else round(random.uniform(0, 4), 2)
    temp    = round(random.uniform(18, 34), 1)

    return {
        "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "umidade_pct": umidade,
        "ph":          ph,
        "N_ok":        n,
        "P_ok":        p,
        "K_ok":        k,
        "npk_ok":      n and p and k,
        "temperatura": temp,
        "prob_chuva":  pop,
        "chuva_3h_mm": rain,
        "wx_block":    pop >= WX_POP_BLOCK or rain >= WX_RAIN_BLOCK,
    }


def decidir_bomba(leitura: dict, bomba_ligada: bool = False) -> tuple[bool, str]:
    """
    Implementa a lógica de decisão do .ino:
    - Ligar:   !wx_block AND umidade < HUM_ON AND pH ok AND NPK ok
    - Desligar: wx_block OR umidade > HUM_OFF OR !pH ok OR !NPK ok
    Retorna (novo_estado, motivo).
    """
    ph_ok   = PH_MIN <= leitura["ph"] <= PH_MAX
    wx_block = leitura["wx_block"]
    umid     = leitura["umidade_pct"]
    npk_ok   = leitura["npk_ok"]

    if not bomba_ligada:
        if not wx_block and umid < HUM_ON and ph_ok and npk_ok:
            return True, f"Umidade {umid}% < {HUM_ON}% | pH {leitura['ph']:.2f} ok | NPK ok"
        motivos = []
        if wx_block:        motivos.append("chuva prevista")
        if umid >= HUM_ON:  motivos.append(f"umidade {umid}% >= {HUM_ON}%")
        if not ph_ok:       motivos.append(f"pH {leitura['ph']:.2f} fora de [{PH_MIN},{PH_MAX}]")
        if not npk_ok:      motivos.append("NPK insuficiente")
        return False, "OFF — " + "; ".join(motivos)
    else:
        if wx_block or umid > HUM_OFF or not ph_ok or not npk_ok:
            motivos = []
            if wx_block:         motivos.append("chuva prevista")
            if umid > HUM_OFF:   motivos.append(f"umidade {umid}% > {HUM_OFF}%")
            if not ph_ok:        motivos.append(f"pH {leitura['ph']:.2f} fora de range")
            if not npk_ok:       motivos.append("NPK insuficiente")
            return False, "Desligada — " + "; ".join(motivos)
        return True, f"Mantendo ON — umidade {umid}%"


def simular_ciclo(n_leituras: int = 5, intervalo_s: float = 0.0,
                  id_cultura: int = 1) -> list[dict]:
    """
    Executa N leituras consecutivas simulando o loop() do ESP32,
    persiste no banco e retorna a lista de eventos.
    """
    from src.fase2.database import inserir_leitura, registrar_irrigacao, inicializar_db

    inicializar_db()

    bomba = False
    eventos = []

    for i in range(n_leituras):
        leit = ler_sensores()
        nova_bomba, motivo = decidir_bomba(leit, bomba)

        id_leit = inserir_leitura(
            id_cultura=id_cultura,
            umidade=leit["umidade_pct"],
            ph=leit["ph"],
            n=int(leit["N_ok"]),
            p=int(leit["P_ok"]),
            k=int(leit["K_ok"]),
            temp=leit["temperatura"],
            prob_chuva=leit["prob_chuva"],
            chuva_3h=leit["chuva_3h_mm"],
            bloquear=leit["wx_block"],
        )

        if nova_bomba and not bomba:
            registrar_irrigacao(
                id_cultura=id_cultura,
                duracao_min=round(random.uniform(5, 30), 1),
                volume_litros=round(random.uniform(50, 300), 1),
                motivo=motivo,
            )

        bomba = nova_bomba
        leit["bomba_on"] = bomba
        leit["motivo"]   = motivo
        leit["id_leitura"] = id_leit
        eventos.append(leit)

        if intervalo_s > 0:
            time.sleep(intervalo_s)

    return eventos


if __name__ == "__main__":
    print("=== Simulação IoT ESP32 (5 leituras) ===")
    for ev in simular_ciclo(5):
        status = "LIGADA" if ev["bomba_on"] else "DESLIGADA"
        print(f"[{ev['timestamp']}] Umid={ev['umidade_pct']}%  pH={ev['ph']:.2f}  "
              f"Bomba={status}  | {ev['motivo']}")
