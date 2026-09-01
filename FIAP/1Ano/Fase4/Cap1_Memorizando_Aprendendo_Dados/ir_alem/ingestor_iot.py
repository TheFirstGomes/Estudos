import pandas as pd
import sqlite3
import time
import os
from datetime import datetime


# CONFIGURAÇÕES
DB_NAME = 'farmtech_database.db'
CSV_PATH = r'C:\Users\Usuario\Documents\Estudos\FIAP\Fase4\raw\dados_irrigacao.csv' 
INGESTION_INTERVAL_SECONDS = 0.05 
MAX_ROWS_TO_INGEST = 1000 

# FUNÇÕES DO BANCO DE DADOS
def setup_database():
    """Cria a tabela sensor_data no SQLite se ela não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            timestamp TEXT PRIMARY KEY,
            umidade REAL,
            ph REAL,
            nitrogenio INTEGER,
            fosforo INTEGER,
            postassio INTEGER,
            probabilidade_precipitacao REAL,
            chuva_3h REAL,
            bloqueio_meteorológico INTEGER,
            estado_bomba INTEGER
        )
    """)
    conn.commit()
    conn.close()
    print(f"Base de dados '{DB_NAME}' configurada.")

def ingest_data_row(conn, row):
    """Insere uma única linha de dados na base de dados."""
    # Preparar a tupla de valores a partir da série do Pandas
    values = (
        row['timestamp'], row['umidade'], row['ph'], row['nitrogenio'],
        row['fosforo'], row['postassio'], row['probabilidade_precipitacao'],
        row['chuva_3h'], row['bloqueio_meteorológico'], row['estado_bomba']
    )
    # SQL INSERT
    sql = """
        INSERT OR IGNORE INTO sensor_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        conn.execute(sql, values)
        return True
    except sqlite3.Error as e:
        print(f"Erro de ingestão para {row['timestamp']}: {e}")
        return False

# FUNÇÃO PRINCIPAL DE INGESTÃO
def simulate_iot_ingestion():
    """Simula a leitura e ingestão contínua de dados de sensores."""
    try:
        # 1. Carregar a fonte de dados (seu CSV completo)
        df = pd.read_csv(CSV_PATH)
        df = df.fillna(df.mean(numeric_only=True)) # Tratamento de NA
        
        # 2. Conectar-se ao banco de dados
        conn = sqlite3.connect(DB_NAME)
        
        print(f"\n--- INÍCIO DA SIMULAÇÃO DE INGESTÃO IOT (MAX {MAX_ROWS_TO_INGEST} linhas) ---")
        
        # 3. Iterar e Ingerir
        ingested_count = 0
        
        # Iterar sobre o DataFrame até o limite
        for index, row in df.head(MAX_ROWS_TO_INGEST).iterrows():
            if ingest_data_row(conn, row):
                ingested_count += 1
                
                # Exibe o progresso a cada 100 linhas (para não sobrecarregar)
                if ingested_count % 100 == 0:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {ingested_count} linhas ingeridas no DB.")
                
            time.sleep(INGESTION_INTERVAL_SECONDS)
            
        conn.commit()
        conn.close()
        
        print(f"\nSIMULAÇÃO CONCLUÍDA. Total de {ingested_count} registros inseridos em '{DB_NAME}'.")

    except FileNotFoundError:
        print(f"\nERRO: Arquivo CSV '{CSV_PATH}' não encontrado. Por favor, verifique o caminho.")
    except Exception as e:
        print(f"\nOcorreu um erro geral durante a ingestão: {e}")

if __name__ == '__main__':
    setup_database()
    simulate_iot_ingestion()