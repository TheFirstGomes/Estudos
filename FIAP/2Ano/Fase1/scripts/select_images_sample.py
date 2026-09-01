"""
Seleciona uma amostra estratificada de 120 imagens (30 por classe) a partir do
dataset real "ECG Images dataset of Cardiac Patients" (Khan & Hussain, 2021,
Mendeley Data, DOI 10.17632/gwbz3fsgp8.2, CC BY 4.0) para a Parte 3 do
projeto (dados visuais).

O dataset completo tem ~929 imagens em 4 classes desbalanceadas (172 a 284
imagens por classe). Para reduzir o volume no repositorio e, ao mesmo tempo,
evitar reforcar o desbalanceamento original (um ponto de atencao de
Governanca de Dados / vies), a amostra usada aqui e balanceada: exatamente
30 imagens por classe, escolhidas aleatoriamente com semente fixa (seed=42)
para reprodutibilidade.

Para rodar este script: baixe o dataset completo em
https://data.mendeley.com/datasets/gwbz3fsgp8/2 ("Download All"), extraia o
zip e aponte SRC_ROOT abaixo para a pasta extraida (que contem as 4
subpastas de classe listadas em CLASS_MAP).
"""
import random
import shutil
from pathlib import Path

random.seed(42)

SRC_ROOT = Path("./ecg_extracted")  # pasta com o dataset Mendeley extraido
DST_ROOT = Path(__file__).resolve().parent.parent / "images"

CLASS_MAP = {
    "Normal Person ECG Images (284x12=3408)": "normal",
    "ECG Images of Myocardial Infarction Patients (240x12=2880)": "infarto_agudo_miocardio",
    "ECG Images of Patient that have History of MI (172x12=2064)": "historico_infarto",
    "ECG Images of Patient that have abnormal heartbeat (233x12=2796)": "arritmia",
}

N_PER_CLASS = 30


def main():
    for src_name, dst_name in CLASS_MAP.items():
        src_dir = SRC_ROOT / src_name
        dst_dir = DST_ROOT / dst_name
        dst_dir.mkdir(parents=True, exist_ok=True)

        files = sorted(src_dir.glob("*.jpg"))
        sample = random.sample(files, N_PER_CLASS)
        for f in sample:
            shutil.copy2(f, dst_dir / f.name)
        print(f"{dst_name}: {len(sample)} imagens copiadas de {len(files)} disponiveis")


if __name__ == "__main__":
    main()
