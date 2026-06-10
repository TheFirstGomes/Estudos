"""
Fase 7 — IA Como Fertilizante Digital
Cap. 1 — A Consolidação de um Sistema

Orquestrador FarmTech — menu interativo no terminal.
Execução:
    cd FIAP/Fase7/FarmTech
    python run.py
"""

import sys
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

PYTHON = sys.executable


def banner() -> None:
    print("\n" + "=" * 60)
    print("   FARMTECH SOLUTIONS — Fase 7 | A Consolidação de um Sistema")
    print("=" * 60)


def menu() -> str:
    print("""
1. Dashboard completo (Streamlit — todas as fases)
2. Fase 1/2 — Inicializar banco de dados
3. Fase 3 — Simular ciclo IoT (5 leituras)
4. Fase 4 — Testar inferência ML
5. Fase 5 — Testar alertas AWS (modo simulado)
6. Fase 6 — Testar visão computacional (modo simulado)
0. Sair
""")
    try:
        return input("Escolha (0-6) [padrão: 1]: ").strip() or "1"
    except (EOFError, KeyboardInterrupt):
        return "1"


def rodar(modulo: str, descricao: str, opcional: bool = False) -> bool:
    print(f"\n>> {descricao}")
    try:
        res = subprocess.run(
            [PYTHON, modulo],
            check=True, capture_output=True, text=True, cwd=str(ROOT),
        )
        if res.stdout:
            print(res.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        if opcional:
            print(f"   Aviso (opcional): {e.stderr.strip()[:200]}")
            return False
        print(f"   ERRO: {e.stderr.strip()[:400]}")
        if e.stdout:
            print(f"   Stdout: {e.stdout.strip()[:200]}")
        sys.exit(1)


def abrir_dashboard() -> None:
    app = ROOT / "dashboard" / "app.py"
    print(f"\nIniciando dashboard: {app}")
    print("Acesse: http://localhost:8501")
    print("Pressione Ctrl+C para encerrar.\n")
    try:
        subprocess.run(
            [PYTHON, "-m", "streamlit", "run", str(app)],
            check=True, cwd=str(ROOT),
        )
    except (subprocess.CalledProcessError, KeyboardInterrupt):
        print("\nDashboard encerrado.")


def main() -> None:
    os.chdir(ROOT)
    banner()
    opcao = menu()

    if opcao == "0":
        print("Saindo.")
        return

    if opcao == "1":
        abrir_dashboard()

    elif opcao == "2":
        rodar("src/fase2/database.py", "Inicializando banco de dados FarmTech")

    elif opcao == "3":
        rodar("src/fase3/iot_simulacao.py", "Simulação IoT — 5 leituras ESP32")

    elif opcao == "4":
        rodar("src/fase4/ml_inferencia.py", "Teste de inferência ML (Random Forest)")

    elif opcao == "5":
        rodar("src/fase5/aws_alertas.py", "Teste de alertas AWS SNS (simulado)")

    elif opcao == "6":
        # Pequeno script inline para testar o módulo de visão
        script = (
            "import sys; sys.path.insert(0, '.');"
            "from src.fase6.visao import analisar_imagem, sumarizar_batch;"
            "res = [analisar_imagem(b'', modo='simulado') for _ in range(5)];"
            "[print(f\"  {r['arquivo']} -> {r['classe']} ({r['confianca']*100:.1f}%)\") for r in res];"
            "print('Sumário:', sumarizar_batch(res))"
        )
        subprocess.run([PYTHON, "-c", script], cwd=str(ROOT))

    else:
        print("Opção inválida.")

    print("\n" + "=" * 60)
    print("   FARMTECH — Execução concluída.")
    print("=" * 60)


if __name__ == "__main__":
    main()
