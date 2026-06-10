# Ir Além — Opção 1: AWS Rekognition para Monitoramento de Lavoura

### FIAP · Fase 7 · IA Como Fertilizante Digital
**Aluno:** Luan Gonçalves Gomes — RM 566806

---

## Objetivo

Substituir ou complementar a análise OpenCV da Fase 6 com **AWS Rekognition**, serviço de visão computacional da AWS que detecta objetos, cenas e rótulos personalizados em imagens de lavoura sem necessitar de treinamento local.

---

## Arquitetura

```
[Câmera IoT / Upload no Dashboard]
           │
           ▼
[S3 Bucket: farmtech-imagens-lavoura]
           │
           ▼
[AWS Rekognition: DetectLabels / DetectCustomLabels]
           │
           ├─ Label: "Plant Disease" (Confidence > 80%)  ──▶  [SNS Alert]
           ├─ Label: "Healthy Vegetation"                ──▶  [Log OK]
           └─ Label: "Pest" / "Insect" (Confidence > 75%) ──▶  [SNS Alert]
                                                                    │
                                                                    ▼
                                                        [Dashboard Streamlit]
```

---

## Configuração Passo a Passo

### Passo 1 — Criar Bucket S3

Acesse **AWS Console → S3 → Criar bucket**:

| Campo | Valor |
|-------|-------|
| Nome do bucket | `farmtech-imagens-lavoura` |
| Região | `us-east-2` |
| Bloqueio de acesso público | Mantido (acesso via IAM) |

![Criar bucket S3](docs/01_criar_bucket_s3.png)

---

### Passo 2 — Permissões IAM para Rekognition

Adicione a política ao usuário/role IAM da FarmTech:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rekognition:DetectLabels",
        "rekognition:DetectCustomLabels",
        "rekognition:CreateProject",
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "*"
    }
  ]
}
```

![Política IAM Rekognition](docs/02_iam_policy_rekognition.png)

---

### Passo 3 — Testar DetectLabels via Console

No **AWS Console → Rekognition → Demonstrar labels**:
1. Faça upload de uma imagem de lavoura
2. Observe os rótulos detectados com percentual de confiança
3. Rótulos relevantes para agricultura: `Plant`, `Vegetation`, `Leaf`, `Soil`, `Crop`

![Teste DetectLabels](docs/03_detect_labels_console.png)

---

### Passo 4 — Custom Labels (Modelo Personalizado)

Para detecção específica de doenças e pragas da FarmTech:

1. **AWS Console → Rekognition → Custom Labels → Criar projeto**
   - Nome: `farmtech-saude-lavoura`

2. **Criar dataset de treinamento**:
   - Upload de imagens rotuladas: `saudavel`, `praga`, `doenca_foliar`, `deficiencia_nutricional`
   - Mínimo recomendado: 50 imagens por classe

3. **Treinar modelo** (tempo estimado: 30-90 minutos)

4. **Iniciar endpoint** (custo: ~$4/hora — desligue após uso)

![Custom Labels projeto](docs/04_custom_labels_projeto.png)

---

### Passo 5 — Integração com o Dashboard FarmTech

Código Python para integração com o dashboard existente (`src/fase6/visao.py`):

```python
import boto3
from pathlib import Path

def analisar_rekognition(caminho_imagem: str, bucket: str = "farmtech-imagens-lavoura",
                          regiao: str = "us-east-2") -> dict:
    """
    Analisa imagem de lavoura com AWS Rekognition DetectLabels.
    Retorna classificação de saúde e ação corretiva.
    """
    s3  = boto3.client("s3", region_name=regiao)
    rek = boto3.client("rekognition", region_name=regiao)

    # 1. Upload da imagem para S3
    nome_s3 = f"lavoura/{Path(caminho_imagem).name}"
    s3.upload_file(caminho_imagem, bucket, nome_s3)

    # 2. Detectar labels
    resp = rek.detect_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": nome_s3}},
        MaxLabels=20,
        MinConfidence=60,
    )

    labels = {l["Name"]: l["Confidence"] for l in resp["Labels"]}

    # 3. Classificar saúde baseado nos labels
    if "Disease" in labels and labels["Disease"] > 75:
        return {"classe": "Doença foliar",
                "confianca": labels["Disease"],
                "acao": "Aplicar fungicida. Retirar folhas afetadas."}

    if any(l in labels for l in ["Pest", "Insect", "Bug"]):
        conf = max(labels.get(l, 0) for l in ["Pest", "Insect", "Bug"])
        return {"classe": "Praga detectada",
                "confianca": conf,
                "acao": "Aplicar defensivo. Isolar talhão afetado."}

    if "Plant" in labels or "Vegetation" in labels:
        return {"classe": "Saudável",
                "confianca": labels.get("Plant", labels.get("Vegetation", 95)),
                "acao": "Nenhuma ação. Monitoramento contínuo."}

    return {"classe": "Inconclusivo",
            "confianca": 0,
            "acao": "Coletar amostra de solo. Verificar manualmente."}
```

---

### Passo 6 — Teste via Dashboard

Após integrar o código acima na aba **Visão Computacional** do dashboard Streamlit:

1. Selecione modo `Rekognition (AWS)` no seletor de modo
2. Faça upload de uma imagem de lavoura
3. O resultado aparece com classe, confiança e ação corretiva

![Integração no dashboard](docs/05_dashboard_rekognition.png)

---

## Comparação: OpenCV vs. Rekognition

| Critério | OpenCV (Fase 6) | AWS Rekognition |
|----------|----------------|----------------|
| **Custo** | Gratuito | $0,001/imagem (DetectLabels) |
| **Precisão** | Média (análise HSV) | Alta (modelos pré-treinados) |
| **Doenças específicas** | Não detecta | Detecta com Custom Labels |
| **Dependências** | opencv-python local | boto3 + S3 + IAM |
| **Latência** | < 100ms | 200-800ms (rede) |
| **Uso offline** | Sim | Não (requer conexão AWS) |
| **Treinamento customizado** | Requer código | Interface visual + API |

**Recomendação:** OpenCV para alertas rápidos em campo (tempo real via ESP32-CAM); Rekognition para análise periódica de alta precisão e auditoria de lavoura.

---

## Custos Estimados (Conta Pessoal AWS)

| Operação | Preço | Volume estimado/mês |
|----------|-------|---------------------|
| DetectLabels | $0,001/imagem | 500 imagens = **$0,50** |
| Custom Labels (inferência) | $0,004/imagem | 200 imagens = **$0,80** |
| Custom Labels (endpoint ativo) | $4,00/hora | 2h/mês = **$8,00** |
| S3 armazenamento | $0,023/GB | 1 GB = **$0,023** |
| **Total estimado** | | **~$9,32/mês** |

> Desligue o endpoint Custom Labels após o uso para evitar cobranças contínuas.

---

## Integração com SNS (Alertas Automáticos)

Rekognition + SNS criam um pipeline completo de detecção e notificação:

```
Imagem detectada com doença (Confiança > 80%)
    └─▶ verificar_thresholds() [já implementado na Fase 5]
            └─▶ enviar_alerta_sns() [já implementado na Fase 5]
                    └─▶ E-mail para lggomesconsul@gmail.com
```

A integração aproveita 100% do código já desenvolvido na Fase 5, apenas substituindo a entrada (imagem → classificação Rekognition → thresholds → SNS).

---

## Referências

- [AWS Rekognition Developer Guide](https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html)
- [boto3 Rekognition API](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html)
- [Custom Labels Getting Started](https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/getting-started.html)
