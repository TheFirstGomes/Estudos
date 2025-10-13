# 📊 Luan Gonçalves Gomes — RM566806  
## Fase 2 — Capítulo 07: Análise Exploratória de Dados em R  

### 🧠 Objetivo
Realizar uma **Análise Exploratória de Dados (AED)** utilizando R, com foco em compreender o comportamento de variáveis quantitativas e qualitativas relacionadas à **produção agrícola**.

---

## 1️⃣ Preparação do Ambiente

Antes de iniciar a análise, foi realizada a instalação e carregamento dos pacotes necessários:

```r
packages <- c('readxl', 'ggplot2', 'psych')
instalados <- packages %in% rownames(installed.packages())
if (any(!instalados)) install.packages(packages[!instalados])
lapply(packages, library, character.only=TRUE)
```

---

## 2️⃣ Carregamento dos Dados

A base de dados foi importada a partir de um arquivo Excel contendo informações sobre produção agrícola:

```r
dados <- read_excel('~/Estudos/FIAP/Fase2/Cap_07_Decolando_Ciencia_Dados/base_agronegocio.xlsx')
str(dados)
```

**Estrutura do dataset:**
- `num_trabalhadores` — número de trabalhadores (quantitativa)
- `producao_toneladas` — produção agrícola em toneladas (quantitativa)
- `cultura` — tipo de cultura produzida (qualitativa)
- `classificacao_produtividade` — nível de produtividade (qualitativa)

---

## 3️⃣ Variável Quantitativa: `producao_toneladas`

### 🔹 Medidas de Tendência Central
| Estatística | Valor |
|--------------|--------|
| Média        | 1614,20 |
| Mediana      | 1613,26 |
| Moda         | 480,16 |

---

### 🔹 Medidas de Dispersão
| Medida | Valor |
|--------|--------|
| Variância | 292.468,7 |
| Desvio Padrão | 540,8 |
| Amplitude | 2000,96 |
| Coeficiente de Variação (%) | 33,5 |

**Interpretação:**  
A produção apresenta **alta dispersão (CV = 33,5%)**, indicando heterogeneidade entre as fazendas analisadas.

---

### 🔹 Medidas Separatrizes
**Quartis**
| Q1 | Q2 (Mediana) | Q3 |
|----|---------------|----|
| 1209,66 | 1613,26 | 2054,69 |

**Decis (10% - 90%)**  
Valores variando entre **878,76** e **2335,61**, evidenciando amplitude produtiva elevada.

---

### 🔹 Análise Gráfica Quantitativa

#### Histograma com Curva de Densidade
![](8b7529d0-138f-42a6-b33e-b1b3907a7d60.png)

**Interpretação:**  
A distribuição é **ligeiramente assimétrica à esquerda**, com maior concentração em torno de 1600 toneladas.  
Há variabilidade considerável entre as observações, sem presença forte de outliers extremos.

---

## 4️⃣ Variável Qualitativa: `classificacao_produtividade`

### 🔹 Tabela de Frequências

| Classificação | Frequência | Percentual |
|----------------|-------------|-------------|
| Alta | 28 | 28% |
| Baixa | 28 | 28% |
| Média | 23 | 23% |
| Muito Alta | 21 | 21% |

**Interpretação:**  
Os grupos “Alta” e “Baixa” concentram as maiores frequências, com **distribuição relativamente equilibrada** entre as categorias.

---

### 🔹 Análise Gráfica Qualitativa

#### Gráfico de Barras
![](49c08e79-3c0d-4bf0-a78e-ebde5150c5ae.png)

#### Gráfico de Pizza
![](88ff43d2-53a5-4938-ba9b-867c203e402e.png)

**Interpretação:**  
Os dois gráficos demonstram que não há predominância absoluta de uma única categoria, indicando uma **distribuição diversificada da produtividade agrícola**.

---

## 5️⃣ Resumo Estatístico Global

```r
describe(dados$producao_toneladas)
```

| Estatística | Valor |
|--------------|--------|
| Média | 1614,2 |
| Desvio Padrão | 540,8 |
| Assimetria | -0,18 |
| Curtose | -0,97 |
| Amplitude | 2000,96 |

**Síntese:**  
A variável apresenta **leve assimetria negativa**, com concentração próxima à média e ausência de extremos relevantes.

---

## 🧩 Conclusão

A análise evidencia:
- Produção média próxima de 1600 toneladas;
- Ampla dispersão entre produtores;
- Classificação de produtividade equilibrada entre as categorias;
- Nenhuma anomalia grave nos dados.

Essa etapa de Análise Exploratória fornece uma **visão inicial robusta** para futuras etapas de modelagem estatística ou preditiva no contexto do agronegócio.

---

📁 **Arquivos gerados**
- `base_agronegocio.xlsx`
- `analise_exploratoria.R`
- `README.md` (este documento)
- Gráficos exportados:
  - `histograma_producao.png`
  - `barras_classificacao.png`
  - `pizza_classificacao.png`
