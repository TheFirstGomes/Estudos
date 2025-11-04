from dataclasses import dataclass
from datetime import date

@dataclass
class PerdaCana: 
    data_colheita: date
    regiao: str
    area_hectares: float
    producao_total_ton: float
    perda_ton: float
    percentual_perda: float
    tipo_colheita: str
    umidade_percentual: float
    eficiencia_colheita: float
    classificacao_perda: str
    