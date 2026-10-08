"""CardioIA - Fase 2, Parte 1: extração de sintomas e sugestão de diagnóstico.

Lê as frases de pacientes (data/frases_sintomas.txt), identifica sintomas com
base no mapa de conhecimento (data/mapa_conhecimento.csv) e sugere possíveis
diagnósticos ordenados por pontuação.

Como funciona (regras simples, sem ML):
  1. Normaliza o texto (minúsculas, sem acentos, sem pontuação).
  2. Procura cada expressão do mapa como palavra(s) inteira(s) na frase.
  3. Ignora expressões negadas ("sem febre", "não tenho dor no peito").
  4. Cada expressão vale 1 / (nº de doenças que a compartilham): sintomas
     genéricos (ex.: "dor no peito") pesam menos que os específicos
     (ex.: "boca torta"). A pontuação da doença é a soma dos sintomas
     encontrados que apontam para ela.

Uso:
    python extracao_diagnostico.py [frases.txt] [mapa.csv] [saida.csv]

AVISO: ferramenta didática. Não substitui avaliação médica.
"""
import csv
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NEGADORES = {"sem", "nao", "nunca", "nem", "nenhum", "nenhuma"}
JANELA_NEGACAO = 3  # palavras anteriores inspecionadas em busca de negação


def normalizar(texto: str) -> str:
    """Minúsculas, sem acentos, sem pontuação, espaços colapsados."""
    sem_acento = unicodedata.normalize("NFKD", texto.lower())
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9\s]", " ", sem_acento).split())


ROTULOS: dict[str, str] = {}  # expressão normalizada -> forma original (para exibição)


def carregar_mapa(caminho: Path) -> dict[str, set[str]]:
    """Retorna {expressão normalizada: {doenças associadas}}."""
    mapa: dict[str, set[str]] = defaultdict(set)
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        for linha in csv.DictReader(f):
            doenca = linha["Doença Associada"].strip()
            for coluna in ("Sintoma 1", "Sintoma 2"):
                expressao = normalizar(linha[coluna])
                if expressao:
                    mapa[expressao].add(doenca)
                    ROTULOS.setdefault(expressao, linha[coluna].strip())
    return mapa


def _negada(palavras: list[str], inicio: int) -> bool:
    return any(p in NEGADORES for p in palavras[max(0, inicio - JANELA_NEGACAO):inicio])


def extrair_sintomas(frase: str, mapa: dict[str, set[str]]) -> list[str]:
    """Expressões do mapa presentes (e não negadas) na frase."""
    texto = normalizar(frase)
    palavras = texto.split()
    encontrados = []
    for expressao in sorted(mapa, key=len, reverse=True):
        for m in re.finditer(rf"\b{re.escape(expressao)}\b", texto):
            inicio = len(texto[:m.start()].split())
            if not _negada(palavras, inicio):
                encontrados.append(expressao)
                break
    return encontrados


def sugerir_diagnosticos(sintomas: list[str], mapa: dict[str, set[str]]):
    """Lista [(doença, pontuação)] ordenada, da mais para a menos provável."""
    pontos: dict[str, float] = defaultdict(float)
    for s in sintomas:
        for doenca in mapa[s]:
            pontos[doenca] += 1 / len(mapa[s])
    return sorted(pontos.items(), key=lambda x: (-x[1], x[0]))


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # acentos no console do Windows
    frases_txt = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "data" / "frases_sintomas.txt"
    mapa_csv = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / "data" / "mapa_conhecimento.csv"
    saida = Path(sys.argv[3]) if len(sys.argv) > 3 else RAIZ / "data" / "resultados_diagnostico.csv"

    mapa = carregar_mapa(mapa_csv)
    frases = [l.strip() for l in frases_txt.read_text(encoding="utf-8").splitlines() if l.strip()]

    with open(saida, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["frase_id", "sintomas_identificados", "diagnostico_sugerido", "pontuacao", "alternativas"])
        for i, frase in enumerate(frases, 1):
            sintomas = extrair_sintomas(frase, mapa)
            ranking = sugerir_diagnosticos(sintomas, mapa)
            print(f"\nFrase {i}: {frase}")
            print(f"  Sintomas identificados: {', '.join(ROTULOS[s] for s in sintomas) or '(nenhum)'}")
            if ranking:
                print("  Possíveis diagnósticos:")
                for doenca, p in ranking[:3]:
                    print(f"    - {doenca} (pontuação {p:.2f})")
                top, alt = ranking[0], ranking[1:3]
            else:
                print("  Possíveis diagnósticos: nenhum encontrado no mapa de conhecimento")
                top, alt = ("", 0.0), []
            w.writerow([i, "; ".join(ROTULOS[s] for s in sintomas), top[0], f"{top[1]:.2f}" if top[0] else "",
                        "; ".join(f"{d} ({p:.2f})" for d, p in alt)])
    print(f"\nResultados salvos em {saida}")
    print("AVISO: apoio didático à triagem; não substitui avaliação médica.")


if __name__ == "__main__":
    main()
