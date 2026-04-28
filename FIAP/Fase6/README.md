# FarmTech Solutions — Previsão de Rendimento de Safra
### FIAP · Fase 6 · Cap. 1 ·  O despertar da Rede Neural

---

## Links Rapidos

| Recurso | Link |
|---|---|
| **Video Demonstrativo (Entrega 1)** | [Assistir no YouTube](https://youtu.be/ihUIHOewe8k) |
| **Video Demonstrativo (Entrega 2)** | [Assistir no YouTube](https://youtu.be/V0xefvv9eL0) |

---

## Sobre o Projeto

Este projeto tem como objetivo demonstrar, na prática, a aplicação de técnicas de visão computacional para detecção e classificação de objetos.
Foram implementadas e comparadas diferentes abordagens:

- YOLO customizado (detecção de objetos)
- YOLO pré-treinado
- CNN treinada do zero
- Transfer Learning com MobileNetV2 + Fine Tuning
- Segmentação + Classificação

O projeto simula um cenário real da empresa FarmTech Solutions, aplicando IA em problemas de monitoramento e análise visual.

Este repositório contém as entregas da Fase 6:

- **Entrega 1:** Sistema de visão computacional usando o YOLO
- **Entrega 2:** Usando Transfer Learning e Fine Tuning

---

## 🧩 Estrutura do Projeto

Este projeto está dividido em três partes principais:

### 🔹 Entrega 1 — YOLO Customizado
- Treinamento com dataset próprio
- Comparação entre 40 e 80 épocas
- Avaliação com métricas (Precision, Recall, mAP)

### 🔹 Entrega 2 — Comparação de Abordagens
- YOLO pré-treinado
- CNN treinada do zero
- Análise comparativa entre modelos

### 🔹 🚀 Ir Além — Transfer Learning e Segmentação
- Transfer Learning com MobileNetV2
- Fine Tuning do modelo
- Aplicação de segmentação de imagens
- Classificação com e sem segmentação
- Validação de hipóteses

---  
## Dataset
O dataset foi construído manualmente com 3 classes:
- 🚗 Carros 
- 🏍️ Motos
- 🚜 Tratores

---

## 🏷️ Etapa 1 — Detecção com YOLO
🔹 YOLO Customizado

Foram realizados dois experimentos:

- 40 épocas 
- 80 épocas

### 📊 Resultados

| Métrica        | 40 épocas | 80 épocas |
|----------------|----------|----------|
| Precision      | ~0.75    | ~0.85    |
| Recall         | Instável | Mais estável |
| mAP@0.5        | ~0.75    | ~0.80    |
| mAP@0.5:0.95   | ~0.40    | ~0.45    |
###
🔹 YOLO Pré-treinado 
- Fácil de usar
- Sem custo de treinamento
- Menor precisão no dataset específico

🧠 Conclusão:
O aumento de épocas melhora a performance até certo ponto, porém com indícios de overfitting.

## 🟡 Etapa 2 — CNN do Zero

Foi implementada uma rede convolucional simples para classificação.

### 📊 Resultado:
Acurácia: ~50%

🧠 Análise:
- Desempenho limitado pelo baixo volume de dados
- Incapacidade de localizar objetos na imagem
- Sensível a ruídos e background

## 🔵 Etapa 3 — Transfer Learning (MobileNetV2)

Foi utilizada a arquitetura MobileNetV2, pré-treinada na ImageNet.

🔹 Estratégia:
1. Congelamento inicial das camadas
2. Treinamento da camada final
3. Fine Tuning (descongelamento parcial)

#### 📊 Resultado:
- Acurácia superior à CNN do zero

🧠 Justificativa:
- Aproveitamento de features aprendidas em larga escala
- Redução da necessidade de dados
- Melhor generalização

## 🟢 Etapa 4 — Segmentação + Classificação
🔹 Processo:
- Geração de máscara da imagem
- Remoção do background
- Classificação da imagem segmentada

#### 🖼️ Exemplo:
- Imagem original
- Máscara
- Imagem segmentada

#### 🧠 Hipótese:
Remover informações irrelevantes melhora a classificação.

#### 📊 Resultado observado:
- Melhor desempenho em imagens com fundo complexo
- Impacto reduzido em imagens simples
---

## ⚖️ Comparação Geral

| Método                       | Performance        |
|------------------------------|------------------|
| CNN do zero                  | Baixa (~50%)     |
| Transfer Learning            | Alta             |
| Segmentação + Classificação  | Média/Alta       |
| YOLO Customizado             | Alta             |

---

## 🧠 Conclusão

- YOLO é ideal para detecção de objetos  
- Transfer Learning é a melhor abordagem para classificação  
- Segmentação pode melhorar resultados em cenários com ruído  
- CNN do zero é limitada com poucos dados  

---

## ⚠️ Limitações

- Dataset pequeno  
- Baixa diversidade de imagens  
- Possível overfitting  

## Grupo

> Projeto desenvolvido para a disciplina de Deep Learning — FIAP · Fase 6
> Luan Gonçalves Gomes - RM566806
