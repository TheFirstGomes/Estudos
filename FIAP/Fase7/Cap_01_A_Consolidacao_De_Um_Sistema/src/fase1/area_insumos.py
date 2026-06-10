"""
Fase 1 — Base de Dados Inicial
Cálculos de área de plantio, manejo de insumos e consulta à API meteorológica.
"""

import math
import requests
from datetime import datetime


# ── Cálculos de Área ─────────────────────────────────────────────────────────

def calcular_area_retangular(comprimento_m: float, largura_m: float) -> float:
    return comprimento_m * largura_m


def calcular_area_circular(raio_m: float) -> float:
    return math.pi * raio_m ** 2


def calcular_area_triangular(base_m: float, altura_m: float) -> float:
    return (base_m * altura_m) / 2


# ── Manejo de Insumos ────────────────────────────────────────────────────────

INSUMOS_POR_HECTARE = {
    "fertilizante_npk_kg": 300,
    "calcario_kg":         200,
    "herbicida_l":          3.5,
    "inseticida_l":         1.2,
    "agua_irrigacao_m3":  5000,
}


def calcular_insumos(area_m2: float) -> dict:
    """Retorna a quantidade de cada insumo necessária para a área informada."""
    area_ha = area_m2 / 10_000
    return {
        insumo: round(qtd_ha * area_ha, 2)
        for insumo, qtd_ha in INSUMOS_POR_HECTARE.items()
    }


def calcular_custo_estimado(insumos: dict) -> float:
    """Estimativa de custo em R$ com base nos insumos calculados."""
    precos = {
        "fertilizante_npk_kg": 3.50,
        "calcario_kg":          0.80,
        "herbicida_l":         45.00,
        "inseticida_l":        38.00,
        "agua_irrigacao_m3":    0.05,
    }
    return round(sum(insumos[k] * precos[k] for k in insumos), 2)


# ── API Meteorológica (OpenWeatherMap — mesma usada no ESP32) ─────────────────

OWM_BASE = "https://api.openweathermap.org/data/2.5/forecast"


def consultar_clima(lat: float, lon: float, api_key: str) -> dict:
    """
    Consulta o forecast de 3h da OpenWeatherMap (mesmo endpoint do sketch ESP32).
    Retorna dict com temperatura, umidade, precipitação e bloqueio de irrigação.
    """
    try:
        resp = requests.get(
            OWM_BASE,
            params={
                "lat": lat, "lon": lon,
                "appid": api_key,
                "units": "metric", "lang": "pt_br",
                "cnt": 1,
            },
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()
        item = data["list"][0]

        pop      = float(item.get("pop", 0))
        rain_3h  = float(item.get("rain", {}).get("3h", 0))
        temp     = float(item["main"]["temp"])
        umid_ar  = float(item["main"]["humidity"])
        descricao = item["weather"][0]["description"]

        # Mesma lógica de bloqueio do ESP32: pop >= 60% ou chuva >= 2 mm
        bloquear = pop >= 0.60 or rain_3h >= 2.0

        return {
            "temperatura_c":    round(temp, 1),
            "umidade_ar_pct":   umid_ar,
            "prob_chuva_pop":   round(pop, 2),
            "chuva_3h_mm":      round(rain_3h, 2),
            "descricao":        descricao,
            "bloquear_irrigacao": bloquear,
            "timestamp":        datetime.utcfromtimestamp(item["dt"]).strftime("%Y-%m-%d %H:%M"),
            "erro":             None,
        }

    except requests.exceptions.Timeout:
        return {"erro": "Timeout ao conectar com OpenWeatherMap."}
    except requests.exceptions.ConnectionError:
        return {"erro": "Sem conexão com a internet."}
    except Exception as exc:
        return {"erro": str(exc)}


def clima_simulado(lat: float = -23.55, lon: float = -46.63) -> dict:
    """Dados meteorológicos simulados (fallback sem chave de API)."""
    import random
    pop      = round(random.uniform(0, 1), 2)
    rain_3h  = round(random.uniform(0, 5), 2)
    return {
        "temperatura_c":    round(random.uniform(18, 35), 1),
        "umidade_ar_pct":   random.randint(40, 90),
        "prob_chuva_pop":   pop,
        "chuva_3h_mm":      rain_3h,
        "descricao":        "simulado",
        "bloquear_irrigacao": pop >= 0.60 or rain_3h >= 2.0,
        "timestamp":        datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        "erro":             None,
    }
