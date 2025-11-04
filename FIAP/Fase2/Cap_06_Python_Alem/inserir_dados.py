from datetime import datetime

def inserir_dados_manualmente(db):
    """Permite que o usuário insira um registro manualmente no banco Oracle."""
    print("\nInserção manual de dados - Colheita de Cana-de-Açúcar")
    try:
        data_colheita = input("Data da colheita (AAAA-MM-DD): ")
        datetime.strptime(data_colheita, "%Y-%m-%d")  # valida formato

        regiao = input("Região: ")
        area_hectares = float(input("Área (hectares): "))
        producao_total_ton = float(input("Produção total (toneladas): "))
        perda_ton = float(input("Perda estimada (toneladas): "))
        tipo_colheita = input("Tipo de colheita (Manual/Mecânica): ").capitalize()
        umidade_percentual = float(input("Umidade média (%): "))

        # Cálculos automáticos
        percentual_perda = round((perda_ton / producao_total_ton) * 100, 2)
        eficiencia_colheita = round(((producao_total_ton - perda_ton) / producao_total_ton) * 100, 2)

        # Classificação automática
        if percentual_perda < 3: 
            classificacao = 'Baixa'
        elif percentual_perda < 6: 
            classificacao = 'Média'
        elif percentual_perda < 9: 
            classificacao = 'Alta'
        else:
            classificacao = 'Crítica'

        query = """
        INSERT INTO PERDAS_CANA (
            DATA_COLHEITA, REGIAO, AREA_HECTARES, PRODUCAO_TOTAL_TON,
            PERDA_TON, PERCENTUAL_PERDA, TIPO_COLHEITA, UMIDADE_PERCENTUAL,
            EFICIENCIA_COLHEITA, CLASSIFICACAO_PERDA
        )
        VALUES (TO_DATE(:1, 'YYYY-MM-DD'), :2, :3, :4, :5, :6, :7, :8, :9, :10)
        """

        db.executar(query, (
            data_colheita, regiao, area_hectares, producao_total_ton, perda_ton,
            percentual_perda, tipo_colheita, umidade_percentual, eficiencia_colheita, classificacao
        ))

        print(f"Registro inserido com sucesso! Classificação: {classificacao}")

    except ValueError:
        print("Erro: valor numérico inválido ou formato de data incorreto (use AAAA-MM-DD).")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")