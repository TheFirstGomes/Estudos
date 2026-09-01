import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==============================================================================
# 0. CONFIGURAÇÃO DE CAMINHOS
# ==============================================================================
MODEL_PATH = 'modelos_treinados'
TEST_DATA_PATH = 'testes_streamlit'
# ==============================================================================
# 1. FUNÇÕES DE CARREGAMENTO E CACHE
# ==============================================================================

@st.cache_resource
def load_models():
    """Carrega os modelos treinados do disco."""
    model_files = {
        'umidade': os.path.join(MODEL_PATH, 'modelo_regressao_umidade.joblib'),
        'ph': os.path.join(MODEL_PATH, 'modelo_regressao_ph.joblib'),
        'rendimento': os.path.join(MODEL_PATH, 'modelo_regressao_rendimento_esperado.joblib')
    }
    
    models = {}
    for name, path in model_files.items():
        try:
            models[name] = joblib.load(path)
        except FileNotFoundError:
            st.error(f"Erro ao carregar modelo '{name}'. Arquivo não encontrado em: {path}")
            st.stop()
    return models

@st.cache_data 
def load_test_data():
    """Carrega os dados de teste para os gráficos e métricas."""
    try:
        # Carrega dados para o gráfico de correlação (Umidade vs Rendimento)
        X_test = pd.read_csv(os.path.join(TEST_DATA_PATH, 'X_teste_rendimento_esperado.csv'))
        y_test = pd.read_csv(os.path.join(TEST_DATA_PATH, 'y_teste_rendimento_esperado.csv'))
        
        # Combina X e y para facilitar o plot
        df_test = X_test.copy()
        df_test['rendimento_esperado'] = y_test['rendimento_esperado']
        
        return df_test
    except FileNotFoundError:
        st.warning(f"Arquivos de teste para o gráfico não encontrados em: {TEST_DATA_PATH}. O gráfico será desabilitado.")
        return pd.DataFrame()

MODELS = load_models()
TEST_DATA_DF = load_test_data()

# ==============================================================================
# 2. FUNÇÕES DE PREVISÃO E AÇÕES
# ==============================================================================

def generate_actions(umidade_pred, ph_pred, rendimento_pred):
    """Gera sugestões de manejo com base nas previsões."""
    actions = []
    
    # 1. Ação de Irrigação (Baseada na Umidade Prevista)
    if umidade_pred < 40: 
        actions.append("💧 **IRRIGUE AGORA!** Umidade do solo abaixo do ideal (<40%).")
    elif umidade_pred > 65: 
        actions.append("🛑 **EVITE IRRIGAR.** Umidade do solo alta demais (>65%), risco de encharcamento.")
    else:
        actions.append("✅ Umidade ideal. Monitoramento contínuo.")

    # 2. Ação de Fertilização/Correção (Baseada no pH Previsto)
    if ph_pred < 5.5: 
        actions.append("⚠️ **CORREÇÃO DE pH.** Adicionar calcário ou corretivo para aumentar o pH (muito ácido).")
    elif ph_pred > 7.5: 
        actions.append("⚠️ **CORREÇÃO DE pH.** Adicionar enxofre ou fertilizante ácido para diminuir o pH (muito alcalino).")
    else:
        actions.append("✅ pH ideal para a maioria das culturas. Fertilize conforme o cronograma.")
        
    # 3. Alerta de Produtividade (Baseado no Rendimento Previsto)
    if rendimento_pred < 20: # Limite de baixo rendimento simulado
        actions.append(f"📉 **ALERTA DE BAIXO RENDIMENTO.** O rendimento esperado ({rendimento_pred:.2f}) está abaixo da média. Reveja nutrientes e irrigação.")
    elif rendimento_pred > 60:
        actions.append(f"💰 **ALTO RENDIMENTO ESPERADO!** O rendimento previsto ({rendimento_pred:.2f}) indica condições ótimas.")

    return actions

def make_predictions(input_data_df):
    """Executa a previsão nos 3 modelos com as features corretas."""
    
    # Lista completa de features, incluindo 'mes' e 'hora'
    all_features = [
        'umidade', 'ph', 'nitrogenio', 'fosforo', 'postassio', 
        'probabilidade_precipitacao', 'chuva_3h', 'bloqueio_meteorológico', 
        'estado_bomba', 'mes', 'hora'
    ]

    # Converte o input para o DataFrame que o modelo espera
    input_df = pd.DataFrame([input_data_df], columns=all_features)
    
    # 1. Previsão de Umidade 
    features_umidade = [c for c in all_features if c != 'umidade']
    umidade_pred = MODELS['umidade'].predict(input_df[features_umidade])[0]
    
    # 2. Previsão de pH
    features_ph = [c for c in all_features if c != 'ph']
    ph_pred = MODELS['ph'].predict(input_df[features_ph])[0]
    
    # 3. Previsão de Rendimento
    features_rendimento = [c for c in all_features if c != 'rendimento_esperado']
    rendimento_pred = MODELS['rendimento'].predict(input_df[features_rendimento])[0]

    return umidade_pred, ph_pred, rendimento_pred

# ==============================================================================
# 3. INTERFACE STREAMLIT
# ==============================================================================

# Configuração da Página
st.set_page_config(layout="wide", page_title="FarmTech Solutions | Assistente Agrícola Inteligente")
st.title("🌱 FarmTech Solutions: Assistente Agrícola Cognitivo")

st.markdown("---")

# Layout de Colunas para Inputs e Resultados
col_input, col_output = st.columns([1, 1])

# --- Coluna de Inputs (Simulação de Sensores) ---
with col_input:
    st.header("1. Simulação de Leitura de Sensores")
    st.markdown("Ajuste os parâmetros do campo e do clima para gerar a previsão:")
    
    # Variáveis do Solo
    st.subheader("Sensores de Campo e Sazonalidade")
    umidade = st.slider("Umidade Atual do Solo (%)", 10.0, 80.0, 45.0, 0.1)
    ph = st.slider("pH Atual do Solo", 4.0, 8.0, 6.5, 0.01)
    
    # Sazonalidade (Adicionado ao modelo)
    mes = st.slider("Mês Atual", 1, 12, 10)
    hora = st.slider("Hora do Dia (24h)", 0, 23, 15)
    
    # Variáveis Ambientais
    st.subheader("Condições Ambientais e Manejo")
    probabilidade_precipitacao = st.slider("Probabilidade de Precipitação (%)", 0.0, 1.0, 0.45, 0.01)
    chuva_3h = st.number_input("Chuva Prevista (mm/3h)", 0.0, 10.0, 1.5, 0.1)
    bloqueio_meteorológico = st.selectbox("Bloqueio Meteorológico (Nuvem, Neblina)", [0, 1], format_func=lambda x: "Sim" if x==1 else "Não")

    # Variáveis de Manejo (NPK são 0 ou 1 na amostra)
    st.subheader("Manejo e Nutrientes")
    nitrogenio = st.selectbox("Nitrogênio (N) - Presente/Ausente", [0, 1])
    fosforo = st.selectbox("Fósforo (P) - Presente/Ausente", [0, 1])
    postassio = st.selectbox("Potássio (K) - Presente/Ausente", [0, 1])
    
    estado_bomba = st.selectbox("Estado Atual da Bomba de Irrigação", [0, 1], format_func=lambda x: "Ligada" if x==1 else "Desligada")


    # Botão de Previsão
    if st.button("Gerar Previsões e Ações", type="primary"):
        
        # Coleta dos dados de input
        input_data = {
            'umidade': umidade, 'ph': ph, 'nitrogenio': nitrogenio, 'fosforo': fosforo, 
            'postassio': postassio, 'probabilidade_precipitacao': probabilidade_precipitacao, 
            'chuva_3h': chuva_3h, 'bloqueio_meteorológico': bloqueio_meteorológico, 
            'estado_bomba': estado_bomba, 'mes': mes, 'hora': hora
        }
        
        # Geração das Previsões
        umidade_pred, ph_pred, rendimento_pred = make_predictions(input_data)
        
        # Geração das Ações
        actions = generate_actions(umidade_pred, ph_pred, rendimento_pred)
        
        # Armazena os resultados na session state para exibir
        st.session_state['results'] = {
            'umidade': umidade_pred,
            'ph': ph_pred,
            'rendimento': rendimento_pred,
            'actions': actions,
            'current_umidade': umidade, # Guarda o input para o delta
            'current_ph': ph             # Guarda o input para o delta
        }

# --- Coluna de Outputs (Resultados) ---
with col_output:
    st.header("2. Previsões de IA e Ações Sugeridas")
    
    if 'results' in st.session_state:
        results = st.session_state['results']
        
        # Apresentação dos Resultados
        st.subheader("Resultados da Regressão (Próxima Hora)")
        col_u, col_p, col_r = st.columns(3)
        
        with col_u:
            # Mostra a diferença da previsão em relação ao valor atual inserido pelo usuário
            delta_u = results['umidade'] - results['current_umidade']
            st.metric("Umidade Prevista (%)", f"{results['umidade']:.2f}", delta=f"{delta_u:.2f}") 
        
        with col_p:
            # Mostra a diferença da previsão em relação ao valor atual inserido pelo usuário
            delta_p = results['ph'] - results['current_ph']
            st.metric("pH Previsto", f"{results['ph']:.2f}", delta=f"{delta_p:.2f}")
            
        with col_r:
            st.metric("Rendimento Esperado (Simulado)", f"{results['rendimento']:.2f}")
            
        st.subheader("📋 Ações Sugeridas de Manejo (PARTE 2)")
        st.info("Estas sugestões otimizam o rendimento e corrigem o solo e a irrigação:")
        
        for action in results['actions']:
            st.markdown(f"- {action}")
            
        # ======================================================================
        # GRÁFICO DE CORRELAÇÃO (PARTE 1)
        # ======================================================================
        st.markdown("---")
        st.subheader("📊 Análise Gráfica: Umidade vs. Rendimento (PARTE 1)")
        
        if not TEST_DATA_DF.empty:
            # Cria a figura e os eixos do Matplotlib
            fig, ax = plt.subplots(figsize=(8, 4))
            
            # Gráfico de Dispersão (Scatter Plot)
            sns.scatterplot(
                x='umidade', 
                y='rendimento_esperado', 
                data=TEST_DATA_DF, 
                ax=ax, 
                alpha=0.2, # Transparência para dataset grande
                color='green'
            )
            
            # Destaca a previsão atual na cor vermelha
            ax.plot(
                results['umidade'], results['rendimento'], 
                'o', markersize=10, color='red', label='Previsão Atual'
            )
            
            ax.set_title("Correlação: Umidade do Solo vs. Rendimento Esperado", fontsize=12)
            ax.set_xlabel("Umidade do Solo (%)")
            ax.set_ylabel("Rendimento Esperado (Simulado)")
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)
            
            # Exibe o gráfico no Streamlit
            st.pyplot(fig)
        else:
            st.warning("Não foi possível carregar os dados de teste para o gráfico.")

# ==============================================================================
# 4. EXIBIÇÃO DE MÉTRICAS (PARTE 2)
# ==============================================================================
st.markdown("---")
st.header("📈 Métricas de Desempenho dos Modelos (PARTE 2)")
st.info("Apresentação dos resultados de MAE e R² obtidos no treinamento.")

# Dados das Métricas (Usando os valores que você gerou)
metric_data = {
    'Modelo': ['Umidade do Solo', 'pH', 'Rendimento Esperado'],
    'MAE (Erro Absoluto Médio)': [7.6031, 0.5571, 4.0035],
    'R² (Coeficiente de Determinação)': [0.0776, 0.0009, 0.7488]
}
metrics_df = pd.DataFrame(metric_data)

st.table(metrics_df.style.highlight_max(axis=0, subset=['R² (Coeficiente de Determinação)'], color='lightgreen'))

st.subheader("Conclusão Analítica(PARTE 2)")
st.markdown("""
* O **Modelo de Rendimento (R²: 0.7488)** demonstrou alta capacidade preditiva, indicando que o manejo de NPK e Umidade são os principais fatores de sucesso.
* Os **Modelos de Umidade e pH** tiveram **R² muito baixos** (0.0776 e 0.0009, respectivamente).
""")