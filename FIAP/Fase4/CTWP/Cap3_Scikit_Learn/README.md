# Classificação de Variedades de Grãos: Comparação e Otimização de Modelos de Machine Learning

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%"></a>
</p>

## 👨‍🎓 Integrantes
- <a href="https://www.linkedin.com/in/luan-g-432896b5/">Luan Gomes</a>

## 👩‍🏫 Professores
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Tutor</a>

### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Coordenador</a>

---

## 📜 Descrição do Projeto

Este projeto tem como objetivo analisar o conjunto de dados **seeds_dataset.txt** para classificar três variedades de grãos de trigo (Classe 1, 2 e 3), utilizando técnicas de EDA, pré-processamento, comparação entre modelos e otimização com Grid Search.

### 🎯 Objetivos

- Realizar uma Análise Exploratória de Dados (EDA) completa, incluindo visualização e escalonamento.
- Implementar e comparar o desempenho dos algoritmos **KNN**, **Random Forest** e **SVM**.
- Otimizar o modelo com melhor potencial (SVM) utilizando **GridSearchCV**.
- Interpretar resultados e extrair insights sobre as características geométricas dos grãos.

---

## 🛠️ Detalhes Técnicos

| Ferramenta / Técnica | Uso no Projeto |
|----------------------|----------------|
| **Linguagem** | Python 3 |
| **Bibliotecas** | Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn |
| **Pré-processamento** | StandardScaler |
| **Algoritmos** | KNN, SVM, Random Forest |
| **Otimização** | GridSearchCV |
| **Métricas Avaliadas** | Acurácia, Precisão, Recall, F1-Score, Matriz de Confusão |

---

## 1. Estrutura dos Dados e Pré-processamento

O dataset possui **210 amostras** e **8 atributos**, sendo 7 utilizados como features geométricas e 1 como variável alvo.

### 📌 Features

- Área  
- Perímetro  
- Compacidade  
- Comprimento do Núcleo  
- Largura do Núcleo  
- Coeficiente de Assimetria  
- Comprimento do Sulco do Núcleo  

**Target:** Classe do Grão (1, 2 ou 3)

### 🔧 Pré-processamento

- **Valores Ausentes:** Nenhum valor ausente encontrado.  
- **Escalonamento:** Aplicação do *StandardScaler*, essencial para modelos baseados em distância (KNN e SVM).

---

## 2. Resultados da Classificação e Comparação Inicial

Divisão dos dados: **70% treino / 30% teste**, `random_state=42`.

| Modelo          | Acurácia | Insight Principal |
|-----------------|----------|------------------|
| **Random Forest** | 0.9206 | Melhor acurácia inicial, robusto à multicolinearidade. |
| **KNN** | 0.8730 | Impactado pela correlação entre features. |
| **SVM (Inicial)** | 0.8730 | Parâmetros padrão não capturaram bem a fronteira de decisão. |

---

## 3. Otimização do Modelo (SVM com Grid Search)

O SVM foi escolhido para otimização visando superar o Random Forest.

### 🔍 Parâmetros Otimizados

| Parâmetro | Valor Inicial | Melhor Valor |
|-----------|----------------|--------------|
| **C** | 1.0 | 100 |
| **kernel** | 'rbf' | 'linear' |

### 📈 Desempenho Pós-Otimização

| Modelo | Acurácia Inicial | Acurácia Final |
|--------|------------------|----------------|
| **SVM** | 0.8730 | 0.8889 |

Melhora modesta, porém consistente.

---

## 4. Conclusões e Insights Finais

### 🏆 Modelo Vencedor

**Random Forest** com acurácia **0.9206**, mesmo sem otimização.

### 📊 Insights Relevantes

- **Geometria é altamente discriminante**, permitindo bom desempenho em todos os modelos.
- **Random Forest lida bem com multicolinearidade**, justificando sua superioridade.
- **Erros concentrados na Classe 1**, sugerindo fronteiras de decisão mais ambíguas.

### 🚀 Próximos Passos

- Criar novas features (ex.: razões geométricas).
- Explorar dados adicionais como cor e textura.
- Avaliar modelos mais complexos (XGBoost, LightGBM).

---

## 🔧 Como executar o código

Basta abrir e executar o notebook **.ipynb** incluído no repositório.

---

## 🗃 Histórico de Lançamentos
- **0.1.0 - 26/11/2025**

---

## 📋 Licença

Modelo baseado no template oficial da FIAP.
"""