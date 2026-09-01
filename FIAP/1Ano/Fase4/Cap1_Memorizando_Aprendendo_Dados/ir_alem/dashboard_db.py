import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sqlite3
from sklearn.metrics import mean_absolute_error, r2_score

# ==============================================================================
# 0. CONFIGURAÇÃO DE CAMINHOS
# ==============================================================================
# Ajuste estes caminhos se o seu app.py não estiver na pasta 'Cap1_Memorizando_Aprendendo_Dados'.
MODEL_PATH = 'modelos_treinados'
TEST_DATA_PATH = 'testes_streamlit'
DB_NAME = 'farmtech_database.db' 

# Dados das Métricas (Hardcoded dos seus resultados para a PARTE 2)
METRIC_DATA = {
    'Modelo': ['Umidade do Solo', 'pH', 'Rendimento Esperado'],
    'MAE (Erro Absoluto Médio)': [7.6031, 0.5571, 4.0035],
    'R² (Coeficiente de Determinação)': [0.0776, 0.0009, 0.7488]
}

# =TECNICA DE PLOTAGEM MATPLOTLIB/SEABORN (Para evitar erros de thread no Streamlit)=
# Configura o Matplotlib para ser seguro em ambientes web
plt.style.use('ggplot') 

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

@st.cache_data(ttl=5) # Cache de 5 segundos: força a atualização do gráfico de tendências
def fetch_data_from_db():
    """Lê os últimos 500 registros da tabela sensor_data do SQLite para gráficos de tendência."""
    try:
        conn = sqlite3.connect(DB_NAME)
        # Limita a 500 linhas para melhor performance no Streamlit
        df = pd.read_sql_query("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 500", conn)
        conn.close()
        
        if df.empty:
            return pd.DataFrame()

        # Prepara o DataFrame (Cria features 'mes' e 'hora' para consistência)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['mes'] = df['timestamp'].dt.month
        df['hora'] = df['timestamp'].dt.hour
        
        # Inverte a ordem para o gráfico de linha mostrar o tempo crescendo (mais antigo para mais novo)
        df = df.sort_values(by='timestamp').reset_index(drop=True) 
        
        return df
    except sqlite3.OperationalError as e:
        st.error(f"Erro ao conectar ou ler o DB: {e}. Execute o 'ingestor_iot.py' primeiro.")
        return pd.DataFrame()

@st.cache_data 
def load_test_data_for_plot():
    """Carrega dados de teste (estáticos) para o gráfico de correlação inicial."""
    try:
        X_test = pd.read_csv(os.path.join(TEST_DATA_PATH, 'X_teste_rendimento_esperado.csv'))
        y_test = pd.read_csv(os.path.join(TEST_DATA_PATH, 'y_teste_rendimento_esperado.csv'))
        df_test = X_test.copy()
        # Adiciona a coluna alvo para plotagem
        df_test['rendimento_esperado'] = y_test['rendimento_esperado'] 
        return df_test
    except FileNotFoundError:
        return pd.DataFrame()

MODELS = load_models()
TEST_DATA_DF = load_test_data_for_plot()

# ==============================================================================
# 2. FUNÇÕES DE PREVISÃO E AÇÕES (Lógica principal de IA)
# ==============================================================================

def generate_actions(umidade_pred, ph_pred, rendimento_pred):
    """Gera sugestões de manejo com base nas previsões."""
    actions = []
    
    # 1. Ação de Irrigação
    if umidade_pred < 40: 
        actions.append("💧 **IRRIGUE AGORA!** Umidade do solo abaixo do ideal (<40%).")
    elif umidade_pred > 65: 
        actions.append("🛑 **EVITE IRRIGAR.** Umidade do solo alta demais (>65%).")
    else: actions.append("✅ Umidade ideal. Monitoramento contínuo.")

    # 2. Ação de Fertilização/Correção
    if ph_pred < 5.5: actions.append("⚠️ **CORREÇÃO DE pH.** Adicionar calcário ou corretivo (muito ácido).")
    elif ph_pred > 7.5: actions.append("⚠️ **CORREÇÃO DE pH.** Adicionar enxofre ou fertilizante ácido (muito alcalino).")
    else: actions.append("✅ pH ideal para a maioria das culturas.")
        
    # 3. Alerta de Produtividade
    if rendimento_pred < 20: 
        actions.append(f"📉 **ALERTA DE BAIXO RENDIMENTO.** Revise nutrientes e irrigação.")
    elif rendimento_pred > 60: 
        actions.append(f"💰 **ALTO RENDIMENTO ESPERADO!** Condições ótimas.")

    return actions

def make_predictions(input_data_df):
    """Executa a previsão nos 3 modelos com as features corretas."""
    all_features = [
        'umidade', 'ph', 'nitrogenio', 'fosforo', 'postassio', 
        'probabilidade_precipitacao', 'chuva_3h', 'bloqueio_meteorológico', 
        'estado_bomba', 'mes', 'hora'
    ]
    input_df = pd.DataFrame([input_data_df], columns=all_features)
    
    # 1. Previsão de Umidade 
    features_umidade = [c for c in all_features if c != 'umidade']
    umidade_pred = MODELS['umidade'].predict(input_df[features_umidade])[0]
    
    # 2. Previsão de pH
    features_ph = [c for c in all_features if c != 'ph']
    ph_pred = MODELS['ph'].predict(input_df[features_ph])[0]
    
    # 3. Previsão de Rendimento
    # Remove a coluna target do modelo de rendimento (que não é uma feature de input)
    features_rendimento = [c for c in all_features if c != 'rendimento_esperado'] 
    rendimento_pred = MODELS['rendimento'].predict(input_df[features_rendimento])[0]

    return umidade_pred, ph_pred, rendimento_pred

# ==============================================================================
# 3. INTERFACE STREAMLIT
# ==============================================================================

st.set_page_config(layout="wide", page_title="FarmTech Solutions | Assistente Agrícola Cognitivo")
st.title("🌱 FarmTech Solutions: Dashboard de Agricultura Cognitiva")

st.markdown("Este dashboard lê dados **em tempo real** (simulado) da base de dados SQL (`farmtech_database.db`).")
st.markdown("---")

# Coluna 1: Inputs, Coluna 2: Resultados
col_input, col_output = st.columns([1, 1])

# --- Coluna de Inputs (Simulação de Sensores) ---
with col_input:
    st.header("1. Simulação para Previsão Futura (Online)")
    st.markdown("Ajuste os parâmetros para prever as condições de campo (próxima hora).")
    
    # Campos de Input
    with st.expander("Sensores de Campo e Sazonalidade", expanded=True):
        umidade = st.slider("Umidade Atual do Solo (%)", 10.0, 80.0, 45.0, 0.1)
        ph = st.slider("pH Atual do Solo", 4.0, 8.0, 6.5, 0.01)
        mes = st.slider("Mês Atual", 1, 12, 10)
        hora = st.slider("Hora do Dia (24h)", 0, 23, 15)
        
    with st.expander("Condições Ambientais e Manejo"):
        probabilidade_precipitacao = st.slider("Probabilidade de Precipitação (%)", 0.0, 1.0, 0.45, 0.01)
        chuva_3h = st.number_input("Chuva Prevista (mm/3h)", 0.0, 10.0, 1.5, 0.1)
        bloqueio_meteorológico = st.selectbox("Bloqueio Meteorológico (Nuvem, Neblina)", [0, 1], format_func=lambda x: "Sim" if x==1 else "Não")

        nitrogenio = st.selectbox("Nitrogênio (N)", [0, 1])
        fosforo = st.selectbox("Fósforo (P)", [0, 1])
        postassio = st.selectbox("Potássio (K)", [0, 1])
        estado_bomba = st.selectbox("Estado Atual da Bomba de Irrigação", [0, 1], format_func=lambda x: "Ligada" if x==1 else "Desligada")


    if st.button("Gerar Previsões e Ações", type="primary"):
        input_data = {
            'umidade': umidade, 'ph': ph, 'nitrogenio': nitrogenio, 'fosforo': fosforo, 
            'postassio': postassio, 'probabilidade_precipitacao': probabilidade_precipitacao, 
            'chuva_3h': chuva_3h, 'bloqueio_meteorológico': bloqueio_meteorológico, 
            'estado_bomba': estado_bomba, 'mes': mes, 'hora': hora
        }
        umidade_pred, ph_pred, rendimento_pred = make_predictions(input_data)
        actions = generate_actions(umidade_pred, ph_pred, rendimento_pred)
        
        st.session_state['results'] = {
            'umidade': umidade_pred, 'ph': ph_pred, 'rendimento': rendimento_pred,
            'actions': actions, 'current_umidade': umidade, 'current_ph': ph
        }

# --- Coluna de Outputs (Resultados) ---
with col_output:
    st.header("2. Resultados Preditivos e Ações Sugeridas")
    
    if 'results' in st.session_state:
        results = st.session_state['results']
        st.subheader("Resultados da Regressão (Próxima Hora)")
        col_u, col_p, col_r = st.columns(3)
        
        with col_u:
            delta_u = results['umidade'] - results['current_umidade']
            st.metric("Umidade Prevista (%)", f"{results['umidade']:.2f}", delta=f"{delta_u:.2f}") 
        with col_p:
            delta_p = results['ph'] - results['current_ph']
            st.metric("pH Previsto", f"{results['ph']:.2f}", delta=f"{delta_p:.2f}")
        with col_r:
            st.metric("Rendimento Esperado (Simulado)", f"{results['rendimento']:.2f}")
            
        st.subheader("📋 Ações Sugeridas de Manejo (Online)")
        for action in results['actions']:
            st.markdown(f"- {action}")
    
    else:
        st.info("Ajuste os inputs e clique em 'Gerar Previsões e Ações' para ver os resultados.")

# ==============================================================================
# 4. GRÁFICOS ANALÍTICOS (IR ALÉM 2)
# ==============================================================================
st.markdown("---")
st.header("📊 Análise e Tendências em Tempo Real")

col_trends, col_corr = st.columns(2)

# --- 4.1 Gráfico de Tendências (Lê o DB a cada 5 segundos) ---
with col_trends:
    st.subheader("Tendência da Umidade e pH (Dados IoT Atuais)")
    
    # Atualização forçada a cada 5 segundos
    current_data_df = fetch_data_from_db() 
    
    if not current_data_df.empty:
        fig_trend, ax_trend = plt.subplots(figsize=(10, 5))
        
        # Plot Umidade
        ax_trend.plot(current_data_df['timestamp'], current_data_df['umidade'], label='Umidade', color='#007BFF', alpha=0.9)
        ax_trend.set_ylabel('Umidade (%)', color='#007BFF')
        ax_trend.tick_params(axis='y', labelcolor='#007BFF')
        
        # Cria um segundo eixo para o pH
        ax2_trend = ax_trend.twinx() 
        ax2_trend.plot(current_data_df['timestamp'], current_data_df['ph'], label='pH', color='#28A745', linestyle='--', alpha=0.9)
        ax2_trend.set_ylabel('pH', color='#28A745')
        ax2_trend.tick_params(axis='y', labelcolor='#28A745')

        ax_trend.set_title("Monitoramento de Campo em Tempo Real")
        ax_trend.set_xlabel("Timestamp")
        ax_trend.tick_params(axis='x', rotation=45)
        fig_trend.tight_layout()
        st.pyplot(fig_trend)
    else:
        st.info("Aguardando que o 'ingestor_iot.py' comece a popular a base de dados...")
        
# --- 4.2 Gráfico de Correlação (Estatístico/Previsão) ---
with col_corr:
    st.subheader("Correlação: Umidade vs. Rendimento (Estabilidade do Modelo)")

    if not TEST_DATA_DF.empty:
        fig_corr, ax_corr = plt.subplots(figsize=(10, 5))
        sns.scatterplot(
            x='umidade', 
            y='rendimento_esperado', 
            data=TEST_DATA_DF, 
            ax=ax_corr, 
            alpha=0.2, 
            color='#6F42C1' # Cor roxa
        )
        ax_corr.set_title("Distribuição Histórica (Dados de Treino/Teste)")
        ax_corr.set_xlabel("Umidade do Solo (%)")
        ax_corr.set_ylabel("Rendimento Esperado (Simulado)")
        ax_corr.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig_corr)
    else:
        st.warning("Não foi possível carregar os dados de teste para o gráfico de correlação.")

# 5. MÉTRICAS DE DESEMPENHO (IR ALÉM 2)

st.markdown("---")
st.subheader("⚙️ Métricas de Desempenho dos Modelos")

metrics_df = pd.DataFrame(METRIC_DATA)

st.table(metrics_df.style.highlight_max(axis=0, subset=['R² (Coeficiente de Determinação)'], color='lightgreen'))

st.markdown("""
* **Domínio Técnico:** A solução demonstra integração completa entre Sensores IoT (simulado), Base de Dados SQL e Modelos de IA (Regressão).
* **Usabilidade:** O gestor agrícola tem uma visão clara das **tendências** e das **ações preditivas** sugeridas pela IA.
""")