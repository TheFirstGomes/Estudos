"""
Fase 5 — Cloud Computing & Segurança
Serviço de alertas via AWS SNS.
Modo real:  usa boto3 + credenciais da AWS (env vars ou ~/.aws/credentials).
Modo simulado: imprime o alerta sem enviar, útil para demonstração local.
"""

import os
import json
from datetime import datetime
from pathlib import Path
import sys
_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))
from src.config import (ALERT_UMIDADE_MIN, ALERT_UMIDADE_MAX,
                        ALERT_PH_MIN, ALERT_PH_MAX, ALERT_RENDIMENTO_BAIXO)


# ── Estrutura de alerta ───────────────────────────────────────────────────────

def montar_alerta(tipo: str, valor: float, limite: float,
                  acao: str, cultura: str = "Geral") -> dict:
    return {
        "timestamp":  datetime.now().isoformat(),
        "cultura":    cultura,
        "tipo":       tipo,
        "valor":      round(valor, 2),
        "limite":     round(limite, 2),
        "acao":       acao,
        "severidade": "CRITICO" if tipo.endswith("_min") else "ALERTA",
    }


def verificar_thresholds(umidade: float, ph: float,
                         rendimento: float = None,
                         cultura: str = "Geral") -> list[dict]:
    """
    Avalia os valores dos sensores/modelos contra os thresholds da Fase 5.
    Retorna lista de alertas (pode ser vazia se tudo estiver dentro do range).
    """
    alertas = []

    if umidade < ALERT_UMIDADE_MIN:
        alertas.append(montar_alerta(
            "umidade_min", umidade, ALERT_UMIDADE_MIN,
            f"IRRIGAR IMEDIATAMENTE — umidade {umidade:.1f}% abaixo de {ALERT_UMIDADE_MIN}%.",
            cultura,
        ))
    elif umidade > ALERT_UMIDADE_MAX:
        alertas.append(montar_alerta(
            "umidade_max", umidade, ALERT_UMIDADE_MAX,
            f"SUSPENDER IRRIGAÇÃO — umidade {umidade:.1f}% acima de {ALERT_UMIDADE_MAX}%.",
            cultura,
        ))

    if ph < ALERT_PH_MIN:
        alertas.append(montar_alerta(
            "ph_min", ph, ALERT_PH_MIN,
            f"APLICAR CALCÁRIO — pH {ph:.2f} muito ácido (mínimo {ALERT_PH_MIN}).",
            cultura,
        ))
    elif ph > ALERT_PH_MAX:
        alertas.append(montar_alerta(
            "ph_max", ph, ALERT_PH_MAX,
            f"APLICAR ENXOFRE — pH {ph:.2f} muito alcalino (máximo {ALERT_PH_MAX}).",
            cultura,
        ))

    if rendimento is not None and rendimento < ALERT_RENDIMENTO_BAIXO:
        alertas.append(montar_alerta(
            "rendimento_baixo", rendimento, ALERT_RENDIMENTO_BAIXO,
            f"REVISAR MANEJO — rendimento previsto {rendimento:.1f} ton/ha abaixo do mínimo.",
            cultura,
        ))

    return alertas


# ── Envio via AWS SNS ─────────────────────────────────────────────────────────

def _boto_disponivel() -> bool:
    try:
        import boto3  # noqa: F401
        return True
    except ImportError:
        return False


def enviar_alerta_sns(alerta: dict, topic_arn: str, regiao: str = "us-east-1") -> dict:
    """
    Publica o alerta num tópico SNS.
    Retorna {'enviado': True/False, 'modo': 'real'/'simulado', 'detalhe': ...}
    """
    subject = f"[FarmTech] {alerta['severidade']} — {alerta['tipo']} | {alerta['cultura']}"
    body = (
        f"FarmTech Solutions — Sistema de Alertas Automaticos\n"
        f"{'='*55}\n"
        f"Timestamp : {alerta['timestamp']}\n"
        f"Cultura   : {alerta['cultura']}\n"
        f"Tipo      : {alerta['tipo']}\n"
        f"Valor     : {alerta['valor']}\n"
        f"Limite    : {alerta['limite']}\n"
        f"Severidade: {alerta['severidade']}\n"
        f"\nACAO SUGERIDA:\n{alerta['acao']}\n"
        f"{'='*55}\n"
        f"Este e-mail foi gerado automaticamente pelo sistema FarmTech (Fase 5 - AWS SNS)."
    )

    if not topic_arn or not _boto_disponivel():
        print(f"[SNS SIMULADO]\n{body}")
        return {"enviado": False, "modo": "simulado", "detalhe": body}

    try:
        import boto3
        cliente = boto3.client("sns", region_name=regiao)
        resp = cliente.publish(TopicArn=topic_arn, Message=body, Subject=subject)
        return {"enviado": True, "modo": "real", "detalhe": resp.get("MessageId", "")}
    except Exception as exc:
        print(f"[SNS ERRO] {exc}\n[Fallback simulado]\n{body}")
        return {"enviado": False, "modo": "simulado_por_erro", "detalhe": str(exc)}


def processar_e_enviar(umidade: float, ph: float,
                       rendimento: float = None,
                       cultura: str = "Geral",
                       topic_arn: str = "",
                       regiao: str = "us-east-1") -> list[dict]:
    """
    Ponto de entrada principal: verifica thresholds e envia os alertas necessários.
    Retorna lista de resultados de envio.
    """
    alertas = verificar_thresholds(umidade, ph, rendimento, cultura)
    resultados = []
    for alerta in alertas:
        res = enviar_alerta_sns(alerta, topic_arn, regiao)
        res["alerta"] = alerta
        resultados.append(res)
    return resultados


if __name__ == "__main__":
    resultados = processar_e_enviar(
        umidade=28.0, ph=4.9, rendimento=15.0,
        cultura="Soja — Talhão A",
        topic_arn="",   # vazio → modo simulado
    )
    for r in resultados:
        print(f"[{r['modo']}] Alerta enviado: {r['enviado']}")
