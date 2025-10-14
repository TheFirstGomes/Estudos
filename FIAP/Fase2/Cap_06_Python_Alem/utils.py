import random 
import json 
from datetime import datetime, timedelta, date
from models import PerdaCana

class Utils: 
    @staticmethod
    def gerar_dados(qtd=100):
        regioes =['São Paulo', 'Minas Gerais', 'Goiás', 'Mato Grosso do Sul', 'Paraná']
        tipo_colheita = ['Manual', 'Mecanizada']
        dados = []

        for _ in range(100):
            data = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
            regiao = random.choice(regioes)
            tipo = random.choice(tipo_colheita)
            area = round(random.uniform(100, 500), 2)
            umidade = round(random.uniform(60, 85), 2)
            producao = round(random.uniform(60, 120), 2)
            perda = round(producao * (0.03 if tipo == 'Manual' else random.uniform(0.05, 0.15)), 2)
            percentual = round((perda / producao) * 100, 2)
            eficiencia = round((producao - perda) / area, 2)

            if percentual < 3: 
                classificacao = 'Baixa'
            elif percentual < 6: 
                classificacao = 'Média'
            elif percentual < 9: 
                classificacao = 'Alta'
            else:
                classificacao = 'Crítica'
            
            dados.append(PerdaCana(
                data_colheita=data.date(), 
                regiao=regiao, 
                area_hectares=area, 
                producao_total_ton=producao, 
                perda_ton=perda,
                percentual_perda=percentual, 
                tipo_colheita=tipo, 
                umidade_percentual=umidade, 
                eficiencia_colheita=eficiencia,
                classificacao_perda=classificacao
            ))
        return dados 
    
    @staticmethod
    def exportar_json(dados, path='dados_cana_perdas.json'):
        def default_converter(obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            return str(obj)
        
        try: 
            json_data = [d.__dict__ for d in dados]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4, default=default_converter)
            print(f"Arquivo JSON salvo com {len(dados)} registros em {path}.")
        except Exception as e: 
            print(f'Erro ao exportar Json: {e}')
        
    @staticmethod
    def alerta_predicao(perda, umidade, eficiencia):
        '''Simula um alerta preditivo de desgaste com base em perda, umidade e eficiência'''
        risco = (perda * 0.5) + ((100 - eficiencia) * 0.3) + ((umidade - 60) * 0.2)
        if risco > 50: 
            return 'Alerta: Colhedora com alto risco de desgaste'
        elif risco > 30: 
            return 'Atenção: Verificar lâminas e calibragem'
        else: 
            return 'Operação dentro dos parâmetros ideais'