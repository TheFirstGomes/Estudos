import pandas as pd 
import matplotlib.pyplot as plt 
import os
from datetime import datetime

class Relatorios: 
    @staticmethod
    def gerar_relatorio(df: pd.DataFrame):
        print('\nEstatísticas Gerais: ')
        print(df.describe())

        perda_media = df['percentual_perda'].mean()
        print(f'\nPercentual médio de perda: {perda_media:.2f}%')

        plt.figure(figsize=(8,5))
        df['classificacao_perda'].value_counts().plot(kind='bar', color='green')
        plt.title('Distribuição de Classificação das Perdas')
        plt.xlabel('Classificação')
        plt.ylabel('Frequência')
        plt.grid(axis='y')
        plt.show()

    @staticmethod
    def relatorio_predicao(df): 
        # Classificação
        df['alerta'] = df.apply(lambda x: 'ALTO' if x['percentual_perda'] > 9 else 'NORMAL', axis=1)
        df = df.sort_values(by=['alerta', 'percentual_perda'], ascending=[False, False])

        print("\n================= RELATÓRIO PREDITIVO =================\n")

        # Mostra top 10 e bottom 10 com IDs
        print(">>> Top 10 maiores perdas (ALTO):\n")
        print(df[df['alerta'] == 'ALTO'][['id', 'regiao', 'tipo_colheita', 'percentual_perda', 'alerta']].head(10).to_string(index=False))
        
        print("\n>>> Top 10 menores perdas (NORMAL):\n")
        print(df[df['alerta'] == 'NORMAL'][['id', 'regiao', 'tipo_colheita', 'percentual_perda', 'alerta']].head(10).to_string(index=False))

        # Resumo percentual por região
        resumo_regiao = df.groupby('regiao')['alerta'].value_counts(normalize=True).unstack(fill_value=0) * 100
        resumo_regiao = resumo_regiao.round(1)
        print("\n------ % de ALERTAS por REGIÃO ------")
        print(resumo_regiao.to_string())

        # Resumo percentual por tipo de colheita
        resumo_tipo = df.groupby('tipo_colheita')['alerta'].value_counts(normalize=True).unstack(fill_value=0) * 100
        resumo_tipo = resumo_tipo.round(1)
        print("\n------ % de ALERTAS por TIPO DE COLHEITA ------")
        print(resumo_tipo.to_string())

        # Estatísticas gerais
        total = len(df)
        criticos = (df['alerta'] == 'ALTO').sum()
        print("\n=========================================================")
        print(f"Total de registros analisados: {total}")
        print(f"Alertas críticos (ALTO): {criticos} ({(criticos/total)*100:.2f}%)")
        print("=========================================================\n")

        # Salva CSV completo com ID
        os.makedirs("relatorios", exist_ok=True)
        path = f"relatorios/relatorio_predicao_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        df.to_csv(path, index=False, encoding='utf-8-sig')
        print(f"Relatório completo salvo em: {path}\n")

        return df