from database import OracleDB
from utils import Utils
from relatorios import Relatorios
from inserir_dados import inserir_dados_manualmente
import pandas as pd
import time
import os

def limpar_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione ENTER para voltar ao menu...")
    limpar_console()

def exibir_menu():
    """Exibe o menu principal do sistema."""
    print("\n==============================================")
    print("SISTEMA DE MONITORAMENTO DE COLHEITA DE CANA-DE-AÇÚCAR")
    print("==============================================")
    print("1️  - Gerar dados simulados e exportar JSON")
    print("2️  - Inserir dados simulados no banco Oracle")
    print("3️  - Inserir dados MANUALMENTE no banco Oracle")
    print("4️  - Consultar e gerar relatório estatístico")
    print("5️  - Gerar relatório preditivo (alertas de perda)")
    print("6  - Apagar toda a tabela do sistema!")
    print("7  - Sair do sistema")
    print("==============================================")
    return input("Escolha uma opção (1-6): ")


def main():
    print("Inicializando o sistema...\n")

    # Instancia os objetos principais
    db = OracleDB(user='rm566806', password='Fiap#2025', dsn='oracle.fiap.com.br:1521/ORCL')
    utils = Utils()
    relatorios = Relatorios()

    # Tentativa de conexão
    db.conectar()
    time.sleep(1)

    while True:
        opcao = exibir_menu()
        limpar_console()

        try:
            # 1️ Gerar dados simulados e salvar em JSON
            if opcao == '1':
                qtd = int(input("Quantos registros deseja gerar (ex: 100)? "))
                dados = utils.gerar_dados(qtd)
                utils.exportar_json(dados)
                print(f"{qtd} registros gerados e salvos em JSON com sucesso!")
                pausar()

            # 2️ Inserir dados simulados no banco Oracle
            elif opcao == '2':
                qtd = int(input("Quantos registros deseja gerar e inserir no banco? "))
                dados = utils.gerar_dados(qtd)
                db.inserir_perda([d.__dict__ for d in dados])
                print(f"{qtd} registros inseridos com sucesso no banco Oracle!")
                pausar()

            # 3️ Inserir dados manualmente
            elif opcao == '3':
                inserir_dados_manualmente(db)
                pausar()

            # 4️ Consultar e gerar relatório estatístico
            elif opcao == '4':
                print("Consultando dados no banco Oracle...")
                query = """
                    SELECT DATA_COLHEITA, REGIAO, AREA_HECTARES, PRODUCAO_TOTAL_TON,
                           PERDA_TON, PERCENTUAL_PERDA, TIPO_COLHEITA, UMIDADE_PERCENTUAL,
                           EFICIENCIA_COLHEITA, CLASSIFICACAO_PERDA
                    FROM PERDAS_CANA
                """
                registros = db.consultar(query)

                if not registros:
                    print("Nenhum dado encontrado no banco.")
                    continue

                colunas = [
                    'DATA_COLHEITA', 'REGIAO', 'AREA_HECTARES', 'PRODUCAO_TOTAL_TON',
                    'PERDA_TON', 'PERCENTUAL_PERDA', 'TIPO_COLHEITA', 'UMIDADE_PERCENTUAL',
                    'EFICIENCIA_COLHEITA', 'CLASSIFICACAO_PERDA'
                ]

                df = pd.DataFrame(registros, columns=colunas)
                df.columns = [c.lower() for c in df.columns]
                relatorios.gerar_relatorio(df)
                pausar()

            # 5️ Gerar relatório preditivo
            elif opcao == '5':
                print("Gerando relatório preditivo...")
                query = "SELECT REGIAO, TIPO_COLHEITA, PERCENTUAL_PERDA FROM PERDAS_CANA"
                registros = db.consultar(query)

                if not registros:
                    print("Nenhum dado encontrado para predição.")
                    continue

                df = pd.DataFrame(registros, columns=['REGIAO', 'TIPO_COLHEITA', 'PERCENTUAL_PERDA'])
                df.columns = [c.lower() for c in df.columns]
                resultado = relatorios.relatorio_predicao(df)
                print("\n===== RELATÓRIO PREDITIVO =====\n")
                print(resultado.to_string(index=False))
                pausar()

            # 6 Apagar toda a tabela e recriar
            elif opcao == '6':
                print("Esta ação irá APAGAR e RECRIAR a tabela PERDAS_CANA do zero.")
                confirmar = input("Tem certeza que deseja continuar? (s/n): ").strip().lower()
                
                if confirmar != 's':
                    print("Operação cancelada.")
                    pausar()
                    continue

                try:
                    db.executar("DROP TABLE PERDAS_CANA")
                    print("Tabela PERDAS_CANA excluída com sucesso.\n")
                except Exception as e:
                    print(f"Aviso: {e} (provavelmente a tabela não existia)")

                # Recria a tabela
                create_table_sql = db.criar_tabela()

                try:
                    db.executar(create_table_sql)
                    print("Tabela PERDAS_CANA recriada com sucesso!")
                except Exception as e:
                    print(f"Erro ao recriar a tabela: {e}")

                pausar()
            # 7 Sair do sistema
            elif opcao == '7':
                print("Encerrando o sistema e fechando conexão com o banco...")
                db.fechar()
                time.sleep(1)
                print("Sistema encerrado com sucesso. Até logo!")
                break   

            # Validação de opção inválida
            else:
                print("Opção inválida. Digite um número entre 1 e 6.")
                pausar()

        except ValueError:
            print("Entrada inválida! Digite apenas números inteiros.")
            pausar()
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            pausar()


if __name__ == "__main__":
    main()
