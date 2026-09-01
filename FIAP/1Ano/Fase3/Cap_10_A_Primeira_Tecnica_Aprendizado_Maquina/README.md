# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# AgroSense ML — Análise Agronômica e Processos de Machine Learning  
### Capítulo 10 – Processos de ML

## 👨‍🎓 Integrantes:
- <a href="https://www.linkedin.com/in/luan-g-432896b5/">Luan Gonçalves Gomes</a>

## 👩‍🏫 Professores:
### Tutor(a)
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b/">Sabrina Otoni</a>

### Coordenador(a)
- XXXX

---

# 📜 Descrição

Este projeto tem como objetivo aplicar **conceitos fundamentais de Machine Learning no contexto do agronegócio**, utilizando um conjunto de dados sintético contendo variáveis essenciais relacionadas ao solo, clima e tipos de cultura plantada.

O notebook **`luan_gomes_rm566806_fase3_cap10_processos_ml.ipynb`** implementa:

- Geração de base sintética com variáveis agronômicas (N, P, K, temperature, humidity, pH, rainfall, label);
- Análise exploratória detalhada (EDA) com mais de cinco gráficos;
- Construção do **perfil ideal de solo/clima por cultura**;
- Desenvolvimento de **5 modelos preditivos** diferentes;
- Avaliação comparativa dos modelos utilizando métricas adequadas;
- Interpretação dos resultados e identificação do modelo vencedor.

O trabalho atende integralmente aos requisitos do capítulo **Processos de ML** da Fase 3.

---

# 📁 Estrutura de Pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- **.github**: arquivos de configuração e workflows.
- **assets**: imagens institucionais, logos e elementos visuais.
- **config**: arquivos de parametrização (se aplicável).
- **document**: documentação complementar do projeto.
- **scripts**: scripts auxiliares (deploy, limpeza, automações).
- **src**: código-fonte das fases e notebooks desenvolvidos.
- **README.md**: documento principal de descrição técnica do projeto.

---

# 🔍 Análise Exploratória (EDA)

A base sintética gerada contém as seguintes variáveis:

| Variável | Descrição |
|---------|-----------|
| N | Nitrogênio no solo |
| P | Fósforo |
| K | Potássio |
| temperature | Temperatura média (°C) |
| humidity | Umidade do ar (%) |
| pH | Acidez do solo |
| rainfall | Precipitação (mm) |
| label | Cultura agrícola (soja, milho, café) |

Foram realizados 5+ gráficos obrigatórios:

1. **Histograma de Nitrogênio (N)**  
2. **Boxplot de pH por cultura**  
3. **Dispersão N × K colorida por cultura**  
4. **Temperatura × Umidade**  
5. **Matriz de correlação (heatmap)**  
6. (extra) *Distribuição das culturas*

Os gráficos estão disponíveis no notebook e podem ser exportados para a pasta `/imagens`.

---

# 🌿 Perfil Ideal de Solo/Clima

Para cada cultura (soja, milho e café), foi calculado o **top 10%** mais favorável, considerando nutrientes e clima.  
O resultado foi armazenado na tabela:

| Cultura | N ideal | P ideal | K ideal | pH ideal | Temp ideal | Umidade ideal | Chuva tolerada |
|--------|---------|---------|---------|----------|------------|----------------|-----------------|
| Soja | 77.605802 | 47.990992 | 61.255543 | 6.383920 | 26.222397 | 47.940441 | 3.393547 |
| Milho | 77.500641 | 48.275999 | 61.240766 | 6.382993 | 26.471274 | 49.596413 | 3.355627 |
| Café | 77.795647 | 48.276404 | 61.452591 | 6.381349 | 26.579301 | 48.407980 | 3.346697 |

# 🤖 Modelos Preditivos

Foram treinados **5 algoritmos de Machine Learning**:

- **LogisticRegression**
- **RandomForestClassifier**
- **GradientBoostingClassifier**
- **KNN**
- **SVC (RBF)**

Cada modelo foi avaliado utilizando:

- **Acurácia**
- **Precision**
- **Recall**
- **F1-score**

---

# 📊 Resultado Comparativo

| Modelo | Acurácia |
|--------|----------|
| RandomForestClassifier | **0.33304** |
| GradientBoostingClassifier | 0.32280 |
| LogisticRegression | 0.33312 |
| KNN | 0.33392 |
| SVC | 0.33448 |

---

# 🏆 Melhor Modelo

Após análise das métricas, o modelo vencedor foi: **SVC**

# 🔧 Como executar o código

### Pré-requisitos
- Python 3.10+  
- Jupyter Notebook  
- Bibliotecas:
pandas
numpy
seaborn
matplotlib
scikit-learn

# 🗃 Histórico de lançamentos

* 1.0.0 - 12/11/2025 — Entrega final  

---

# 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>