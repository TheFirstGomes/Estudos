import oracledb
import os 
from dotenv import load_dotenv

load_dotenv()

class OracleDB: 
    def __init__(self):
        self.user = os.getenv('ORACLE_USER')
        self.password = os.getenv('ORACLE_PASSWORD') 
        self.dsn = os.getenv('ORACLE_DSN')
        self.conn = None
        self.cursor = None

    def conectar(self):
        try: 
            self.conn = oracledb.connect(
                user=self.user, 
                password=self.password, 
                dsn=self.dsn
            )
            self.cursor = self.conn.cursor()
            self.criar_tabela()
            print('Conexão Oracle estabelecida com sucesso!')
        except Exception as e: 
            print(f'Erro ao conectar no banco: {e}')
    
    def criar_tabela(self):
        """Cria a tabela PERDAS_CANA caso ela não exista."""
        try:
            sql = """
            DECLARE
                tabela_existente EXCEPTION;
                PRAGMA EXCEPTION_INIT(tabela_existente, -955);
            BEGIN
                EXECUTE IMMEDIATE '
                    CREATE TABLE PERDAS_CANA (
                        ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        DATA_COLHEITA DATE NOT NULL,
                        REGIAO VARCHAR2(100),
                        AREA_HECTARES NUMBER(10,2),
                        PRODUCAO_TOTAL_TON NUMBER(10,2),
                        PERDA_TON NUMBER(10,2),
                        PERCENTUAL_PERDA NUMBER(5,2),
                        TIPO_COLHEITA VARCHAR2(20),
                        UMIDADE_PERCENTUAL NUMBER(5,2),
                        EFICIENCIA_COLHEITA NUMBER(8,2),
                        CLASSIFICACAO_PERDA VARCHAR2(20)
                    )';
            EXCEPTION
                WHEN tabela_existente THEN
                    NULL; -- ignora se já existir
            END;
            """
            self.cursor.execute(sql)
            print("Tabela 'PERDAS_CANA' verificada/criada com sucesso.")
        except Exception as e:
            print(f'Erro ao criar/verificar tabela: {e}')
    
    def inserir_perda(self, dados):
        sql = """
        INSERT INTO PERDAS_CANA (
            DATA_COLHEITA, REGIAO, AREA_HECTARES,
            PRODUCAO_TOTAL_TON, PERDA_TON, PERCENTUAL_PERDA,
            TIPO_COLHEITA, UMIDADE_PERCENTUAL, EFICIENCIA_COLHEITA,
            CLASSIFICACAO_PERDA
        ) VALUES (
            TO_DATE(:data_colheita, 'YYYY-MM-DD'), :regiao, :area_hectares,
            :producao_total_ton, :perda_ton, :percentual_perda,
            :tipo_colheita, :umidade_percentual, :eficiencia_colheita,
            :classificacao_perda
        )
        """
        self.cursor.executemany(sql, dados)
        self.conn.commit()
        print(f'{len(dados)} registros inseridos com sucesso!')

    def consultar(self, query): 
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def executar(self, query, params=None):
        """Executa um comando SQL (INSERT, UPDATE, DELETE) com ou sem parâmetros."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except oracledb.DatabaseError as e:
            print(f"Erro ao executar comando SQL: {e}")
            self.conn.rollback()
    
    def fechar(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print('Conexão encerrada')