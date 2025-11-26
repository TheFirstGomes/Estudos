🌾 FarmTech Solutions: Assistente Agrícola Cognitivo

Este repositório contém o projeto de finalização do curso, demonstrando a integração de sensores IoT (simulados), banco de dados SQL, Machine Learning (Regressão) e um Dashboard Analítico online (Streamlit) para otimizar a tomada de decisão na agricultura de precisão.

🎯 Objetivos do Projeto

O objetivo principal é transformar dados de campo em conhecimento preditivo, permitindo sugestões automáticas de irrigação e manejo agrícola.

Fases Entregues

Pipeline de Machine Learning (Básico): Treinamento de modelos de Regressão para previsão de Umidade, pH e Rendimento Esperado.

IR ALÉM 1 (Integração IoT e DB): Modelagem e Ingestão de dados IoT (simulados) em tempo real para uma base de dados SQLite.

IR ALÉM 2 (Dashboard Analítico Online): Criação de um dashboard interativo (Streamlit) que lê os dados em tempo real da base SQL e exibe previsões e tendências.

🛠️ Arquitetura e Componentes

A solução é dividida em três componentes principais, que se comunicam para formar o Assistente Cognitivo.

Componente

Função

Arquivos

Ingestor/DB (IoT)

Simula a coleta de dados dos sensores a cada 0.05s e os armazena no banco de dados SQLite.

ingestor_iot.py

Modelos de ML

Modelos de Regressão (Random Forest) treinados para prever variáveis críticas.

modelos_treinados/*.joblib

Dashboard Analítico

Interface Streamlit que acessa o DB em tempo real, carrega os modelos e exibe previsões e tendências.

ir_alem/dashboard_db.py

⚙️ Configuração e Execução

Para rodar o projeto, você deve ter Python 3.10, 3.11 ou 3.12 instalado.

1. Pré-requisitos (Instalação)

Crie e ative um ambiente virtual e instale todas as dependências necessárias:

# 1. Cria e ativa o ambiente virtual (opcional, mas recomendado)
python -m venv .venv
.\.venv\Scripts\activate

# 2. Instalação de todas as bibliotecas necessárias
pip install streamlit pandas scikit-learn matplotlib seaborn joblib


2. Estrutura de Pastas

Seus arquivos devem estar organizados conforme a estrutura abaixo para que o projeto funcione (os caminhos relativos foram corrigidos no código para esta estrutura):

Cap1_Memorizando_Aprendendo_Dados/
├── .venv/
├── raw/
│   └── dados_irrigacao.csv     # (Seu arquivo CSV original)
├── modelos_treinados/
│   ├── modelo_regressao_umidade.joblib
│   └── ...
├── testes_streamlit/
│   └── X_teste_rendimento_esperado.csv
│   └── ...
├── ir_alem/
│   ├── ingestor_iot.py         # (Simulador de Sensores e Ingestão DB)
│   └── dashboard_db.py         # (Dashboard Streamlit)
└── farmtech_database.db        # (O arquivo DB será criado aqui)


3. Ordem de Execução (Modo Online)

Para demonstrar a solução de IR ALÉM 2 (Online), você deve rodar dois scripts simultaneamente em dois terminais separados.

🏃 Passo A: Ingestão de Dados (Terminal 1)

Este script cria a tabela SQL e simula a inserção de novos dados continuamente. Mantenha-o rodando.

# Navegue até a pasta 'ir_alem' ou execute a partir da raiz
python ir_alem/ingestor_iot.py


Resultado Esperado: O terminal começará a mostrar mensagens de "X linhas ingeridas no DB." e o arquivo farmtech_database.db será criado na raiz.

🏃 Passo B: Dashboard Analítico (Terminal 2)

Este script inicia o dashboard Streamlit, que se conecta ao farmtech_database.db criado no Passo A.

# Navegue até a pasta 'ir_alem' ou execute a partir da raiz
streamlit run ir_alem/dashboard_db.py


Resultado Esperado: O dashboard abrirá no seu navegador. O Gráfico de Tendências se atualizará a cada 5 segundos, lendo os novos dados inseridos pelo script do Terminal 1.

📊 Análise de Resultados (IR ALÉM 2)

O dashboard é dividido em áreas chave para análise:

1. Previsões e Ações Sugeridas

O painel permite simular inputs futuros e usa os modelos de ML treinados para gerar três previsões:

Umidade Prevista: Baseia a Ação de Irrigação.

pH Previsto: Baseia a Ação de Correção/Fertilização.

Rendimento Esperado: Previsão de Produtividade, usada para alertas de manejo.

2. Gráfico de Tendências (Monitoramento Online)

Lê os últimos 500 pontos da base de dados (atualizada pelo ingestor) para mostrar a evolução da Umidade e do pH ao longo do tempo. Essencial para demonstrar a funcionalidade online.

3. Métricas de Desempenho

As métricas do conjunto de teste são exibidas, com destaque para a precisão:

Alvo

R² (Coeficiente de Determinação)

Interpretação

Rendimento Esperado

0.7488

Forte capacidade preditiva.

Umidade e pH

Muito Baixo

Modelo fraco, indica a necessidade de técnicas de Séries Temporais (como LSTM) para prever estas variáveis com precisão.