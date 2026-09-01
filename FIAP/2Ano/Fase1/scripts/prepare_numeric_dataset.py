"""
Prepara o dataset numerico (Parte 1) a partir dos dados brutos oficiais do
UCI Machine Learning Repository - Heart Disease Data Set (subconjunto Cleveland).

Fonte oficial:
https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data

Doadores originais: Andras Janosi (Hungarian Institute of Cardiology, Budapest),
William Steinbrunn (University Hospital, Zurich), Matthias Pfisterer (University
Hospital, Basel) e Robert Detrano (V.A. Medical Center, Long Beach & Cleveland
Clinic Foundation). Doado ao UCI ML Repository por David W. Aha.

O arquivo original nao possui cabecalho e usa "?" para valores ausentes.
Este script apenas: (1) adiciona nomes de coluna legiveis, (2) converte "?"
em campo vazio (ausencia explicita, sem inventar valores), (3) converte
colunas que sao categoricas-inteiras para int quando possivel, e (4) salva
como CSV em data/cardio_dataset.csv. Nenhum valor numerico original e alterado.
"""
import csv

SRC = "cleveland.data"  # baixado de archive.ics.uci.edu
DST = "../data/cardio_dataset.csv"

COLUMNS = [
    "age",              # idade em anos
    "sex",              # 1 = masculino, 0 = feminino
    "chest_pain_type",  # 1-4: tipo de dor no peito (1=angina tipica ... 4=assintomatico)
    "resting_bp",       # pressao arterial em repouso (mm Hg)
    "cholesterol",      # colesterol serico (mg/dl)
    "fasting_blood_sugar_gt120",  # 1 = glicemia jejum > 120 mg/dl, 0 = nao
    "resting_ecg",      # 0=normal,1=alteracao onda ST-T,2=hipertrofia ventricular esq.
    "max_heart_rate",   # frequencia cardiaca maxima atingida
    "exercise_angina",  # 1 = angina induzida por exercicio, 0 = nao
    "st_depression",    # depressao do segmento ST induzida por exercicio
    "st_slope",         # 1=ascendente,2=plano,3=descendente
    "n_major_vessels",  # numero de vasos principais (0-3) visiveis em fluoroscopia
    "thalassemia",      # 3=normal,6=defeito fixo,7=defeito reversivel
    "diagnosis",        # 0 = sem doenca; 1-4 = presenca/gravidade de doenca cardiaca
]


def convert(value: str):
    value = value.strip()
    if value == "?":
        return ""
    f = float(value)
    if f.is_integer():
        return int(f)
    return f


def main():
    with open(SRC, encoding="utf-8") as f_in, open(DST, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(COLUMNS)
        n_rows = 0
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            fields = line.split(",")
            writer.writerow([convert(v) for v in fields])
            n_rows += 1
    print(f"{n_rows} linhas escritas em {DST}")


if __name__ == "__main__":
    main()
