# Ir Além — Fase 7 · IA Como Fertilizante Digital

**Aluno:** Luan Gonçalves Gomes — RM 566806  
**FIAP · Cap. 1 — A Consolidação de um Sistema**

---

## 🎥 Vídeo Demonstrativo

> *(link do YouTube — [https://youtu.be/NBThqXHFaRI])*

Duração: até 5 minutos · Cobre as duas opções de Ir Além.

---

## Opções implementadas

### Opção 1 · AWS Rekognition

Integração do serviço de visão computacional da AWS para análise de imagens de lavoura. Demonstrado via console AWS com imagens reais e documentado com arquitetura de integração ao dashboard FarmTech via boto3.

📄 [README completo da Opção 1](opcao_1_rekognition/README_Rekognition.md)

**Evidências:**
- `opcao_1_rekognition/docs/01_detect_labels_resultado.png` — DetectLabels com lavoura de milho (Corn 98.6%)
- `opcao_1_rekognition/docs/02_detect_labels_json.png` — Resposta JSON da API
- `opcao_1_rekognition/docs/03_detect_labels_custom.png` — Teste com imagem personalizada
- `opcao_1_rekognition/docs/04_custom_labels_overview.png` — Fluxo Custom Labels (6 passos)

---

### Opção 2 · Algoritmos Genéticos com Meta-Otimização

Implementação de um GA para otimização de alocação de insumos agrícolas (mochila binária), com extensão para **Meta-GA**: um segundo algoritmo genético que evolui automaticamente as configurações de hiperparâmetros do GA interno.

📓 [Notebook Jupyter — Opção 2](opcao_2_algoritmo_genetico/Luan_Gomes_RM566806_ir_alem_algoritmo_genetico.ipynb)

**Estrutura do notebook:**
1. Geração e salvamento de dados (`data/insumos_farmtech.csv`) — reprodutibilidade
2. Problema da mochila binária agrícola
3. GA base com 3 variações de `selection()`, `crossover()` e `mutation()`
4. GA baseline com configuração padrão
5. Meta-GA: espaço de busca de hiperparâmetros + fitness meta
6. Comparação: baseline vs. configuração otimizada pelo Meta-GA (5 rodadas)
7. Visualizações (convergência, boxplot, tempo, insumos selecionados)
8. Conclusão e justificativa técnica

**Evidências:**
- `opcao_2_algoritmo_genetico/data/comparativo_ga_meta_ga.png` — gráficos comparativos
- `opcao_2_algoritmo_genetico/data/insumos_farmtech.csv` — base de dados reprodutível
- `opcao_2_algoritmo_genetico/data/sumario_resultados.json` — métricas finais

---

## Arquitetura geral

```
Ir Além
├── Opção 1: Imagem de lavoura
│   └── AWS Rekognition (DetectLabels / Custom Labels)
│         └── Labels detectados → verificar_thresholds() → AWS SNS → e-mail
│
└── Opção 2: Dados de insumos FarmTech
      └── GA Interno (mochila binária — maximiza ganho agrícola)
            └── Meta-GA (evolui configurações do GA)
                  └── Melhor config → rodada final → comparação com baseline
```

---

## Como executar a Opção 2 (Google Colab)

1. Acesse [Google Colab](https://colab.research.google.com)
2. Faça upload do notebook `Luan_Gomes_RM566806_ir_alem_algoritmo_genetico.ipynb`
3. Runtime → Tipo de ambiente → **CPU** (GA não usa GPU)
4. Execute todas as células em ordem (`Runtime → Run all`)
5. Os resultados são salvos automaticamente em `data/`
