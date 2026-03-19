"""
FarmTech Solutions — Treinamento do Modelo de Classificação
FIAP · Fase 5 · Ir Além

Objetivo: treinar e avaliar 5 classificadores para prever se a plantação
de alface está "Saudável" (1) ou "Não saudável" (0) com base em:
  - temperatura_c  : temperatura em ºC (DHT11)
  - umidade_pct    : umidade relativa em % (DHT11)
  - luz_adc        : valor ADC 0–4095 do fotorresistor

Execução:
  python gerar_dados_treino.py   # gera data/sensor_data.csv se ainda não existir
  python treinar_modelo.py       # treina e salva o modelo em data/modelo.pkl
"""

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    ConfusionMatrixDisplay, roc_auc_score, roc_curve
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# ── Caminhos ─────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent.parent
DATA_PATH   = BASE_DIR / "data" / "sensor_data.csv"
MODELO_PATH = BASE_DIR / "data" / "modelo.pkl"
IMG_DIR     = BASE_DIR / "data"

# ── Carregamento dos dados ────────────────────────────────────────────────────
if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset não encontrado em {DATA_PATH}.\n"
        "Execute primeiro: python gerar_dados_treino.py"
    )

df = pd.read_csv(DATA_PATH)
print(f"Dataset carregado: {len(df)} amostras")
print(f"Classes: {df['saudavel'].value_counts().to_dict()}\n")

# ── Features e alvo ──────────────────────────────────────────────────────────
FEATURES = ["temperatura_c", "umidade_pct", "luz_adc"]
TARGET   = "saudavel"

X = df[FEATURES].values
y = df[TARGET].values

# ── Divisão treino/teste (80/20, estratificada) ───────────────────────────────
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Definição dos 5 modelos ───────────────────────────────────────────────────
# Cada modelo é encapsulado em um Pipeline com StandardScaler para garantir
# que features numéricas estejam na mesma escala (essencial para KNN, SVM e LR)
modelos = {
    "Regressão Logística": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, random_state=42)),
    ]),
    "K-Nearest Neighbors": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", KNeighborsClassifier(n_neighbors=5)),
    ]),
    "SVM (RBF)": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", SVC(kernel="rbf", probability=True, random_state=42)),
    ]),
    "Random Forest": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42)),
    ]),
    "Gradient Boosting": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", GradientBoostingClassifier(n_estimators=100, random_state=42)),
    ]),
}

# ── Treinamento e avaliação ───────────────────────────────────────────────────
resultados = []

print("=" * 60)
print("AVALIAÇÃO DOS MODELOS")
print("=" * 60)

for nome, modelo in modelos.items():
    # Treina
    modelo.fit(X_treino, y_treino)
    y_pred     = modelo.predict(X_teste)
    y_prob     = modelo.predict_proba(X_teste)[:, 1]

    # Métricas
    acuracia   = accuracy_score(y_teste, y_pred)
    auc        = roc_auc_score(y_teste, y_prob)
    cv_scores  = cross_val_score(modelo, X, y, cv=5, scoring="accuracy")

    resultados.append({
        "Modelo":         nome,
        "Acurácia (%)":   round(acuracia * 100, 2),
        "AUC-ROC":        round(auc, 4),
        "CV Acurácia":    round(cv_scores.mean() * 100, 2),
        "CV Std (%)":     round(cv_scores.std() * 100, 2),
    })

    print(f"\n{nome}")
    print(f"  Acurácia  : {acuracia:.4f}")
    print(f"  AUC-ROC   : {auc:.4f}")
    print(f"  CV 5-fold : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(classification_report(y_teste, y_pred,
                                target_names=["Não saudável", "Saudável"]))

# ── Tabela comparativa ────────────────────────────────────────────────────────
df_res = pd.DataFrame(resultados).sort_values("AUC-ROC", ascending=False)
print("\n" + "=" * 60)
print("RANKING FINAL")
print("=" * 60)
print(df_res.to_string(index=False))

# ── Seleção do melhor modelo ──────────────────────────────────────────────────
melhor_nome  = df_res.iloc[0]["Modelo"]
melhor_modelo = modelos[melhor_nome]
print(f"\nMelhor modelo: {melhor_nome}")

# ── Salva o melhor modelo ─────────────────────────────────────────────────────
joblib.dump(melhor_modelo, MODELO_PATH)
print(f"Modelo salvo em: {MODELO_PATH}")

# ── Visualizações ─────────────────────────────────────────────────────────────

# 1. Matriz de confusão do melhor modelo
y_pred_melhor = melhor_modelo.predict(X_teste)
cm = confusion_matrix(y_teste, y_pred_melhor)
fig, ax = plt.subplots(figsize=(5, 4))
ConfusionMatrixDisplay(cm, display_labels=["Não Saudável", "Saudável"]).plot(ax=ax, cmap="Blues")
ax.set_title(f"Matriz de Confusão — {melhor_nome}")
plt.tight_layout()
plt.savefig(IMG_DIR / "confusion_matrix.png", dpi=150)
plt.close()

# 2. Curvas ROC de todos os modelos
fig, ax = plt.subplots(figsize=(7, 5))
for nome, modelo in modelos.items():
    y_prob = modelo.predict_proba(X_teste)[:, 1]
    fpr, tpr, _ = roc_curve(y_teste, y_prob)
    auc = roc_auc_score(y_teste, y_prob)
    ax.plot(fpr, tpr, label=f"{nome} (AUC={auc:.3f})")
ax.plot([0, 1], [0, 1], "k--", label="Aleatório")
ax.set_xlabel("Taxa de Falsos Positivos")
ax.set_ylabel("Taxa de Verdadeiros Positivos")
ax.set_title("Curvas ROC — Comparação de Modelos")
ax.legend(loc="lower right", fontsize=8)
plt.tight_layout()
plt.savefig(IMG_DIR / "roc_curves.png", dpi=150)
plt.close()

# 3. Comparativo de acurácia
fig, ax = plt.subplots(figsize=(8, 4))
cores = ["#2ecc71" if n == melhor_nome else "#3498db" for n in df_res["Modelo"]]
bars = ax.barh(df_res["Modelo"], df_res["Acurácia (%)"], color=cores)
ax.set_xlabel("Acurácia (%)")
ax.set_title("Comparação de Acurácia por Modelo")
ax.set_xlim(50, 105)
for bar, val in zip(bars, df_res["Acurácia (%)"]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(IMG_DIR / "comparativo_acuracia.png", dpi=150)
plt.close()

# 4. Importância das features (somente para modelos baseados em árvores)
if hasattr(melhor_modelo["clf"], "feature_importances_"):
    importancias = melhor_modelo["clf"].feature_importances_
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.barplot(x=importancias, y=FEATURES, palette="viridis", ax=ax)
    ax.set_title(f"Importância das Features — {melhor_nome}")
    ax.set_xlabel("Importância")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "feature_importance.png", dpi=150)
    plt.close()

print("\nVisualizações salvas em data/")
print("\nPróximo passo: execute inferencia_tempo_real.py com o ESP32 conectado.")
