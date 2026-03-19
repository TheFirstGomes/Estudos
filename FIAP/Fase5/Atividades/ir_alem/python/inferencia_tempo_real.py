"""
FarmTech Solutions — Inferência em Tempo Real via Serial (ESP32)
FIAP · Fase 5 · Ir Além

Este script:
  1. Conecta ao ESP32 pela porta Serial USB
  2. Recebe JSON com leituras do DHT11 e fotorresistor
  3. Classifica usando o modelo treinado (modelo.pkl)
  4. Envia o resultado de volta ao ESP32 ("1" ou "0")
  5. Registra todas as leituras em data/historico_tempo_real.csv

Requisitos:
  - ESP32 conectado via USB com o sketch esp32_sensor.ino gravado
  - Modelo treinado em data/modelo.pkl (execute treinar_modelo.py antes)

Uso:
  python inferencia_tempo_real.py                  # detecta a porta automaticamente
  python inferencia_tempo_real.py --porta COM3     # porta manual (Windows)
  python inferencia_tempo_real.py --porta /dev/ttyUSB0  # Linux/Mac
  python inferencia_tempo_real.py --listar         # lista portas disponíveis
"""

import argparse
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import joblib
import serial
import serial.tools.list_ports

# ── Caminhos ─────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent.parent
MODELO_PATH  = BASE_DIR / "data" / "modelo.pkl"
HISTORICO    = BASE_DIR / "data" / "historico_tempo_real.csv"

BAUD_RATE    = 9600
TIMEOUT_S    = 8       # segundos de espera por mensagem Serial

ROTULO_MAP   = {1: "SAUDÁVEL ✓", 0: "NÃO SAUDÁVEL ✗"}
CABECALHO_CSV = ["timestamp", "temperatura_c", "umidade_pct",
                 "luz_adc", "predicao", "classe"]


# ── Utilitários ───────────────────────────────────────────────────────────────
def listar_portas() -> list[str]:
    """Retorna lista de portas Serial disponíveis."""
    return [p.device for p in serial.tools.list_ports.comports()]


def detectar_porta_esp32() -> str | None:
    """
    Tenta detectar automaticamente a porta do ESP32.
    Procura por dispositivos com 'CP210' ou 'CH340' no nome
    (chips USB-Serial mais comuns nos ESP32 dev boards).
    """
    for port in serial.tools.list_ports.comports():
        desc = (port.description or "").upper()
        if any(chip in desc for chip in ["CP210", "CH340", "FTDI", "USB"]):
            return port.device
    # Fallback: retorna a primeira disponível, se houver
    portas = listar_portas()
    return portas[0] if portas else None


def carregar_modelo():
    """Carrega o modelo salvo pelo treinar_modelo.py."""
    if not MODELO_PATH.exists():
        sys.exit(
            f"Modelo não encontrado em {MODELO_PATH}.\n"
            "Execute primeiro: python treinar_modelo.py"
        )
    modelo = joblib.load(MODELO_PATH)
    print(f"Modelo carregado: {MODELO_PATH}")
    return modelo


def inicializar_csv():
    """Cria o CSV de histórico se ainda não existir."""
    if not HISTORICO.exists():
        with open(HISTORICO, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CABECALHO_CSV)


def registrar_csv(row: dict):
    """Acrescenta uma linha ao CSV de histórico."""
    with open(HISTORICO, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO_CSV)
        writer.writerow(row)


def classificar(modelo, temp: float, umidade: float, luz: int) -> int:
    """Retorna 1 (saudável) ou 0 (não saudável)."""
    X = [[temp, umidade, luz]]
    return int(modelo.predict(X)[0])


# ── Loop principal de inferência ─────────────────────────────────────────────
def executar(porta: str, modelo):
    print(f"\nConectando ao ESP32 na porta {porta} @ {BAUD_RATE} baud...")

    try:
        ser = serial.Serial(porta, BAUD_RATE, timeout=TIMEOUT_S)
    except serial.SerialException as e:
        sys.exit(f"Erro ao abrir porta {porta}: {e}")

    # Aguarda o ESP32 inicializar (o boot do ESP32 demora ~2s)
    time.sleep(2)
    ser.reset_input_buffer()

    print("Conexão estabelecida. Aguardando dados do ESP32...")
    print("Pressione Ctrl+C para encerrar.\n")
    print(f"{'Horário':<20} {'Temp (°C)':<12} {'Umid (%)':<12} {'Luz (ADC)':<12} {'Classificação'}")
    print("-" * 75)

    inicializar_csv()

    total       = 0
    saudaveis   = 0

    try:
        while True:
            # ── Lê linha do Serial ───────────────────────────────────────────
            linha_raw = ser.readline().decode("utf-8", errors="ignore").strip()

            if not linha_raw:
                continue  # linha vazia ou timeout → aguarda próxima

            # ── Tenta interpretar como JSON ──────────────────────────────────
            try:
                dados = json.loads(linha_raw)
                temp    = float(dados["temp"])
                umidade = float(dados["humidity"])
                luz     = int(dados["light"])
            except (json.JSONDecodeError, KeyError, ValueError):
                # Ignora linhas de debug/erro do ESP32
                print(f"  [debug ESP32] {linha_raw}")
                continue

            # ── Classificação ────────────────────────────────────────────────
            predicao = classificar(modelo, temp, umidade, luz)
            classe   = ROTULO_MAP[predicao]

            # ── Envia resultado de volta ao ESP32 ────────────────────────────
            ser.write(f"{predicao}\n".encode())

            # ── Log no terminal ──────────────────────────────────────────────
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{ts:<20} {temp:<12.1f} {umidade:<12.1f} {luz:<12} {classe}")

            # ── Registra no CSV ──────────────────────────────────────────────
            registrar_csv({
                "timestamp":    ts,
                "temperatura_c": temp,
                "umidade_pct":   umidade,
                "luz_adc":       luz,
                "predicao":      predicao,
                "classe":        ROTULO_MAP[predicao].replace(" ✓", "").replace(" ✗", ""),
            })

            # ── Estatísticas acumuladas ──────────────────────────────────────
            total += 1
            saudaveis += predicao

    except KeyboardInterrupt:
        print("\n\nEncerrando...")
    finally:
        ser.close()
        print(f"\nResumo da sessão:")
        print(f"  Total de leituras : {total}")
        if total > 0:
            print(f"  Saudável          : {saudaveis} ({saudaveis/total*100:.1f}%)")
            print(f"  Não saudável      : {total-saudaveis} ({(total-saudaveis)/total*100:.1f}%)")
        print(f"  Histórico salvo   : {HISTORICO}")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inferência em tempo real — ESP32 + ML")
    parser.add_argument("--porta",   type=str, help="Porta Serial (ex: COM3 ou /dev/ttyUSB0)")
    parser.add_argument("--listar",  action="store_true", help="Lista portas disponíveis e sai")
    args = parser.parse_args()

    if args.listar:
        portas = listar_portas()
        print("Portas disponíveis:" if portas else "Nenhuma porta encontrada.")
        for p in portas:
            print(f"  {p}")
        sys.exit(0)

    modelo = carregar_modelo()

    porta = args.porta or detectar_porta_esp32()
    if not porta:
        sys.exit(
            "Nenhuma porta Serial detectada.\n"
            "Use --listar para ver as portas disponíveis e passe com --porta."
        )

    executar(porta, modelo)
