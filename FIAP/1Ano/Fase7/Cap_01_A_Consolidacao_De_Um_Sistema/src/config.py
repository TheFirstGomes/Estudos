from pathlib import Path

# Raiz do projeto FarmTech (Fase7/FarmTech/)
ROOT = Path(__file__).resolve().parents[1]

# Pastas locais do projeto
DATA_DIR   = ROOT / "data"
MODELS_DIR = DATA_DIR / "models"
RAW_DIR    = DATA_DIR / "raw"
IMAGES_DIR = DATA_DIR / "images"
TEST_DIR   = DATA_DIR / "test_sets"
DB_PATH    = DATA_DIR / "farmtech_fase7.db"

# Ponteiros para artefatos das fases anteriores
_FIAP = ROOT.parents[1]  # FIAP/

FASE2_DB_MODULE   = _FIAP / "Fase2" / "Cap_06_Python_Alem"
FASE3_CSV         = _FIAP / "Fase3" / "Cap_01_Etapas_Maquina_Agricola" / "raw" / "dados_irrigacao.csv"
FASE4_MODELS      = _FIAP / "Fase4" / "Cap1_Memorizando_Aprendendo_Dados" / "modelos_treinados"
FASE4_TESTS       = _FIAP / "Fase4" / "Cap1_Memorizando_Aprendendo_Dados" / "testes_streamlit"
FASE4_CSV         = _FIAP / "Fase4" / "raw" / "dados_irrigacao.csv"

# Thresholds para alertas (Fase 5 / AWS SNS)
ALERT_UMIDADE_MIN  = 35.0
ALERT_UMIDADE_MAX  = 65.0
ALERT_PH_MIN       = 5.5
ALERT_PH_MAX       = 7.5
ALERT_RENDIMENTO_BAIXO = 20.0
