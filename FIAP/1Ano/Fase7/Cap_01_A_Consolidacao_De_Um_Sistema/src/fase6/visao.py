"""
Fase 6 — Visão Computacional com Redes Neurais
Interface de inferência para o dashboard integrado.
Suporta dois modos:
  - 'simulado': gera resultado fictício para demonstração (sem modelo carregado)
  - 'opencv':   processa imagem real via OpenCV (análise de cor/textura)
O YOLO/MobileNetV2 treinados nos notebooks da Fase 6 podem ser plugados aqui
adicionando um loader na função _inferir_modelo().
"""

import random
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# ── Classes e classes de ameaças definidas no contexto FarmTech ──────────────

CLASSES_SAUDE = [
    "Saudável",
    "Praga detectada",
    "Doença foliar",
    "Deficiência nutricional",
    "Crescimento irregular",
]

# Mapeamento da Fase 6 (dataset com tratores/carros/motos como proxy de veículos agrícolas)
CLASSES_VEICULO = ["Trator", "Carro", "Moto"]

ACOES_CORRETIVAS = {
    "Saudável":                "Nenhuma ação necessária. Continue o monitoramento.",
    "Praga detectada":         "Aplicar defensivo agrícola. Isolar o talhão afetado.",
    "Doença foliar":           "Aplicar fungicida preventivo. Retirar folhas afetadas.",
    "Deficiência nutricional": "Revisar adubação. Coletar amostra de solo para análise.",
    "Crescimento irregular":   "Verificar irrigação e espaçamento. Consultar agrônomo.",
}


# ── Modo simulado ────────────────────────────────────────────────────────────

def _resultado_simulado(nome_arquivo: str = "imagem.jpg") -> dict:
    classe = random.choice(CLASSES_SAUDE)
    confianca = round(random.uniform(0.60, 0.97), 3)
    bboxes = []
    if classe != "Saudável":
        for _ in range(random.randint(1, 3)):
            x = random.randint(50, 300)
            y = random.randint(50, 300)
            bboxes.append({
                "x": x, "y": y,
                "w": random.randint(40, 120),
                "h": random.randint(40, 100),
                "conf": round(random.uniform(0.55, 0.95), 2),
            })
    return {
        "arquivo":    nome_arquivo,
        "modo":       "simulado",
        "classe":     classe,
        "confianca":  confianca,
        "deteccoes":  len(bboxes),
        "bboxes":     bboxes,
        "acao":       ACOES_CORRETIVAS[classe],
        "erro":       None,
    }


# ── Modo OpenCV (análise de cor como proxy da saúde da planta) ───────────────

def _inferir_opencv(caminho: Path) -> dict:
    """
    Análise básica de cor HSV para estimar saúde da planta.
    Verde intenso → Saudável; amarelo/marrom → possível doença/praga.
    """
    try:
        import cv2
        import numpy as np

        img = cv2.imread(str(caminho))
        if img is None:
            return {"erro": f"Não foi possível abrir a imagem: {caminho}"}

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Faixa de verde saudável no espaço HSV
        verde_low  = np.array([35, 40, 40])
        verde_high = np.array([85, 255, 255])
        mask_verde = cv2.inRange(hsv, verde_low, verde_high)

        # Faixa de amarelo/marrom (sintoma de doença)
        amarelo_low  = np.array([15, 40, 40])
        amarelo_high = np.array([34, 255, 255])
        mask_amarelo = cv2.inRange(hsv, amarelo_low, amarelo_high)

        total_px  = img.shape[0] * img.shape[1]
        pct_verde   = float(np.sum(mask_verde > 0)) / total_px
        pct_amarelo = float(np.sum(mask_amarelo > 0)) / total_px

        if pct_verde > 0.40:
            classe, confianca = "Saudável", round(pct_verde, 3)
        elif pct_amarelo > 0.20:
            classe, confianca = "Doença foliar", round(pct_amarelo, 3)
        elif pct_verde < 0.10:
            classe, confianca = "Deficiência nutricional", round(1 - pct_verde, 3)
        else:
            classe, confianca = "Crescimento irregular", 0.55

        return {
            "arquivo":   caminho.name,
            "modo":      "opencv",
            "classe":    classe,
            "confianca": confianca,
            "deteccoes": 1 if classe != "Saudável" else 0,
            "bboxes":    [],
            "acao":      ACOES_CORRETIVAS[classe],
            "pct_verde":   round(pct_verde * 100, 1),
            "pct_amarelo": round(pct_amarelo * 100, 1),
            "erro":      None,
        }

    except ImportError:
        return {"erro": "opencv-python não instalado. Use o modo simulado."}
    except Exception as exc:
        return {"erro": str(exc)}


# ── API pública ───────────────────────────────────────────────────────────────

def analisar_imagem(caminho_ou_bytes, modo: str = "auto") -> dict:
    """
    Analisa uma imagem e retorna o resultado de classificação.

    Parâmetros
    ----------
    caminho_ou_bytes : str | Path | bytes
        Caminho do arquivo ou bytes lidos (ex: st.file_uploader).
    modo : 'auto' | 'simulado' | 'opencv'
        'auto' tenta opencv, cai em simulado se não disponível.
    """
    if isinstance(caminho_ou_bytes, bytes):
        # Salva temporariamente para o OpenCV conseguir abrir
        tmp = Path("/tmp/farmtech_upload.jpg")
        tmp.write_bytes(caminho_ou_bytes)
        caminho = tmp
        nome = "upload.jpg"
    else:
        caminho = Path(caminho_ou_bytes)
        nome = caminho.name

    if modo == "simulado":
        return _resultado_simulado(nome)

    resultado = _inferir_opencv(caminho)
    if resultado.get("erro") and modo == "auto":
        resultado = _resultado_simulado(nome)

    return resultado


def sumarizar_batch(resultados: list[dict]) -> dict:
    """Resume uma lista de resultados de análise de imagens."""
    if not resultados:
        return {}
    classes = [r["classe"] for r in resultados if not r.get("erro")]
    total = len(classes)
    return {
        "total_imagens":  total,
        "saudaveis":      classes.count("Saudável"),
        "com_problema":   total - classes.count("Saudável"),
        "distribuicao":   {c: classes.count(c) for c in set(classes)},
        "conf_media":     round(sum(r["confianca"] for r in resultados if not r.get("erro")) / max(total, 1), 3),
    }
