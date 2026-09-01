<div align="center">

# 📚 Luan Gonçalves Gomes

### Learning Journal · Diário de Estudos

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FIAP](https://img.shields.io/badge/FIAP-RM566806-ED1C24?style=flat)](https://fiap.com.br)
[![AWS](https://img.shields.io/badge/AWS-SNS%20%7C%20Rekognition-FF9900?style=flat&logo=amazonaws&logoColor=white)](https://aws.amazon.com)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey?style=flat)](http://creativecommons.org/licenses/by/4.0/)

<br/>

*🇧🇷 [Português](#português) · 🇺🇸 [English](#english)*

</div>

---

## Português

Repositório de estudos pessoais em **Python e Inteligência Artificial**, com foco especial no curso de IA da **FIAP**. Cada pasta documenta uma fase do aprendizado — desde algoritmos clássicos até integração com serviços em nuvem e técnicas avançadas de otimização.

### 🌾 FIAP — FarmTech Solutions (Fases 1–7)

Projeto principal do curso: um sistema completo de **agricultura de precisão** desenvolvido ao longo de 7 fases, integrando IoT, banco de dados, Machine Learning, cloud computing e visão computacional.

| Fase | Tema | Tecnologias |
|------|------|-------------|
| 1 | Base de dados e cálculo de insumos | Python, OpenWeatherMap API |
| 2 | Modelagem relacional e IoT | Oracle SQL, ESP32, C++ |
| 3 | Automação com ESP32 | C++, DHT22, LDR, MQTT |
| 4 | Dashboard e Data Science | Pandas, scikit-learn, Random Forest |
| 5 | Cloud Computing e alertas | AWS SNS, boto3 |
| 6 | Visão computacional | OpenCV, YOLO, MobileNetV2 |
| **7** | **Consolidação do sistema** | **Streamlit, SQLite, AWS, todos anteriores** |

📁 [`FIAP/Fase7/Cap_01_A_Consolidacao_De_Um_Sistema/`](FIAP/Fase7/Cap_01_A_Consolidacao_De_Um_Sistema/)

### 🧬 Ir Além — Tópicos Avançados

#### Opção 1 · AWS Rekognition
Integração do serviço de visão computacional da AWS para classificação de saúde da lavoura. Demonstração via console + código boto3 para pipeline completo com S3 e alertas SNS.

📁 [`FIAP/Fase7/ir_alem/opcao_1_rekognition/`](FIAP/Fase7/ir_alem/opcao_1_rekognition/)

#### Opção 2 · Algoritmos Genéticos com Meta-Otimização
Implementação de um **GA aninhado** para otimização de alocação de insumos agrícolas. O diferencial é o **Meta-GA**: um segundo algoritmo genético que evolui as *configurações* do GA interno — automatizando a busca pelos melhores hiperparâmetros sem intervenção manual.

A ideia surgiu da analogia com Random Forest: assim como a floresta executa muitas árvores com variações e agrega o melhor resultado, o Meta-GA executa muitas instâncias do GA com configurações distintas e evolui em direção à combinação ótima.

Esse conceito se conecta diretamente ao campo de **Neural Architecture Search (NAS)**, onde algoritmos evolutivos como NEAT/HyperNEAT buscam automaticamente a topologia ideal de redes neurais — indo além de hiperparâmetros e evoluindo a própria estrutura do modelo.

📓 [`FIAP/Fase7/ir_alem/opcao_2_algoritmo_genetico/`](FIAP/Fase7/ir_alem/opcao_2_algoritmo_genetico/)

### 🛠️ Tecnologias

<div align="center">

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/-scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![NumPy](https://img.shields.io/badge/-NumPy-013243?style=flat&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/-Pandas-150458?style=flat&logo=pandas&logoColor=white)
![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![AWS](https://img.shields.io/badge/-AWS-FF9900?style=flat&logo=amazonaws&logoColor=white)
![SQLite](https://img.shields.io/badge/-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Jupyter](https://img.shields.io/badge/-Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)
![Git](https://img.shields.io/badge/-Git-F05032?style=flat&logo=git&logoColor=white)

</div>

---

## English

Personal study repository in **Python and Artificial Intelligence**, with a primary focus on the **FIAP** AI program. Each folder documents a stage of the learning journey — from classical algorithms to cloud integration and advanced optimization techniques.

### 🌾 FIAP — FarmTech Solutions (Phases 1–7)

Main course project: a complete **precision agriculture system** developed across 7 phases, integrating IoT, databases, Machine Learning, cloud computing, and computer vision.

📁 [`FIAP/Fase7/Cap_01_A_Consolidacao_De_Um_Sistema/`](FIAP/Fase7/Cap_01_A_Consolidacao_De_Um_Sistema/)

### 🧬 Beyond the Curriculum — Advanced Topics

#### Option 1 · AWS Rekognition
Integration of AWS computer vision for crop health classification, with a full pipeline: S3 storage → Rekognition DetectLabels → SNS alerts.

#### Option 2 · Genetic Algorithms with Meta-Optimization
A **nested GA** for agricultural resource allocation optimization. The key contribution is the **Meta-GA**: a second genetic algorithm that evolves the *hyperparameter configurations* of the inner GA — removing the need for manual tuning.

This connects directly to **Neural Architecture Search (NAS)**, a research area where evolutionary methods like NEAT automatically search for optimal neural network topologies. The same principle applied here to GA hyperparameters can be extended to search over model architectures, operator types, and training strategies — a natural next step explored in the [referenced NAS survey](https://www.geeksforgeeks.org/deep-learning/neural-architecture-and-search-methods/).

| NAS Concept | This Project's Equivalent |
|---|---|
| Search space | GA hyperparameter combinations |
| Search strategy | Meta-GA (evolutionary) |
| Evaluation strategy | Run inner GA, measure solution quality |
| Architecture | GA configuration (pop size, mutation, crossover) |

---

<div align="center">

**Luan Gonçalves Gomes** · RM 566806 · FIAP

</div>
