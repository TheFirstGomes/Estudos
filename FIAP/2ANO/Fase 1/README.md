# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# CardioIA — Fase 1: Batimentos de Dados

## Nome do grupo
*Cardios da Vida - CardioIA*

## 👨‍🎓 Integrantes:
- <a href="https://www.linkedin.com/in/luan-g-432896b5/">Luan Gonçalves Gomes</a>

## 👩‍🏫 Professores:
### Tutor(a)
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b/">Sabrina Otoni</a>

## 📜 Descrição

Na Fase 1 do CardioIA assumimos o papel de cientistas de dados hospitalares:
o desafio é levantar, organizar e documentar os dados cardiológicos que
alimentarão os módulos inteligentes do CardioIA nas fases seguintes, com
atenção constante à Governança de Dados e a possíveis vieses.

Foram preparados três tipos de dados fundamentais:

1. **Dados numéricos** de pacientes cardíacos (idade, sexo, pressão arterial,
   colesterol, sintomas, frequência cardíaca etc.) — dataset real do UCI
   Machine Learning Repository (subconjunto Cleveland, 303 pacientes).
2. **Textos** médicos/científicos sobre saúde cardiovascular, para uso
   futuro em NLP — um texto histórico-fundacional (Harvey, 1628) e um artigo
   científico contemporâneo (SciELO).
3. **Imagens** de exames cardiológicos (ECG), para uso futuro em Visão
   Computacional — 120 imagens reais, amostradas de forma balanceada a
   partir de um dataset público (Mendeley Data).

Priorizamos, sempre que possível, **dados reais e publicamente citáveis** em
vez de dados simulados, para que as próximas fases (modelagem, comparações,
geração de soluções) partam de uma base mais próxima da realidade clínica —
com as limitações dessa escolha deixadas explícitas na seção de Governança
de Dados e Vieses, ao final deste documento.

Os detalhes de cada uma das três partes — origem dos dados, dicionário de
variáveis, justificativa clínica e como cada base pode ser explorada por
algoritmos de IA — estão nas seções **Parte 1**, **Parte 2** e **Parte 3**
abaixo.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>assets</b>: arquivos não-estruturados de apoio ao repositório (ex.:
  logo da FIAP).

- <b>data</b>: Parte 1 — dataset numérico (`cardio_dataset.csv`) usado pelos
  módulos de IoT/dados tabulares do CardioIA.

- <b>docs</b>: Parte 2 — textos médicos/científicos (`.txt`) usados pelos
  módulos de NLP do CardioIA.

- <b>images</b>: Parte 3 — imagens de ECG. A subpasta `sample/` traz uma
  amostra de preview (3 imagens por classe) já dentro do repositório; o
  conjunto completo (120 imagens) está hospedado em nuvem — ver link na
  seção "Parte 3" abaixo — para não inflar o repositório Git com binários
  grandes.

- <b>scripts</b>: scripts auxiliares que documentam e reproduzem a
  preparação dos dados (`prepare_numeric_dataset.py`,
  `select_images_sample.py`).

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o
  projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

Pré-requisitos: Python 3.10+ (sem dependências externas — apenas
biblioteca padrão).

1. Clone este repositório.
2. Os dados já preparados estão disponíveis diretamente em `data/`, `docs/`
   e `images/sample/` — não é necessário rodar nada para consultá-los.
3. Para **reproduzir** a geração do dataset numérico ou da amostra de
   imagens a partir das fontes brutas (opcional, útil para auditoria):
   ```bash
   cd scripts
   python prepare_numeric_dataset.py   # gera data/cardio_dataset.csv
   python select_images_sample.py      # gera a amostra em images/
   ```
   Ambos os scripts documentam, em comentário no topo do arquivo, a fonte de
   dados bruta original e as transformações aplicadas.

---

## Parte 1 — Dados Numéricos (IoT)

**Arquivo:** [`data/cardio_dataset.csv`](data/cardio_dataset.csv) (303 linhas
de pacientes + cabeçalho, 14 colunas)
**Cópia hospedada em nuvem (link público):** `https://drive.google.com/drive/folders/1JxzOJaJ4gQdzVfWKUJKhvED25Ti9pHJ6?usp=drive_link`

### Origem dos dados

Estes são **dados reais**, não simulados. Trata-se do subconjunto **Cleveland**
do *Heart Disease Data Set* do **UCI Machine Learning Repository**, uma das
bases mais usadas e citadas em pesquisa e ensino de IA aplicada à cardiologia.

- Fonte oficial: https://archive.ics.uci.edu/dataset/45/heart+disease
- Arquivo bruto usado: `processed.cleveland.data`
- Coleta original: Cleveland Clinic Foundation (Robert Detrano), com
  contribuições do Hungarian Institute of Cardiology (Budapest), University
  Hospital de Zurique e University Hospital de Basel.
- Doado ao UCI ML Repository por David W. Aha.

O dataset original tem 76 atributos; a versão "processed" amplamente usada
(e adotada aqui) seleciona os **14 atributos clinicamente mais relevantes**,
já validados pela literatura de referência em cardiologia preditiva.

O script [`scripts/prepare_numeric_dataset.py`](scripts/prepare_numeric_dataset.py)
documenta exatamente a transformação aplicada: apenas adição de nomes de
coluna legíveis e conversão explícita do marcador de dado ausente `"?"` em
campo vazio — **nenhum valor numérico original foi alterado, imputado ou
inventado**.

### Dicionário de variáveis

| Coluna | Descrição | Por que é clinicamente relevante |
|---|---|---|
| `age` | Idade do paciente (29–77 anos na amostra) | Fator de risco cardiovascular independente; risco cresce de forma não linear com a idade |
| `sex` | Sexo biológico (1 = masculino, 0 = feminino) | Perfil de risco e apresentação de sintomas variam significativamente entre sexos (ex.: mulheres têm mais frequentemente sintomas atípicos de infarto) |
| `chest_pain_type` | Tipo de dor torácica (1 a 4, de angina típica a assintomático) | Um dos sinais clínicos mais diretos de doença coronariana |
| `resting_bp` | Pressão arterial em repouso (mm Hg) | Hipertensão é um dos principais fatores de risco modificáveis para infarto e AVC |
| `cholesterol` | Colesterol sérico (mg/dl) | LDL elevado e HDL baixo estão diretamente ligados à aterosclerose |
| `fasting_blood_sugar_gt120` | Glicemia de jejum > 120 mg/dl (1/0) | Proxy para diabetes, comorbidade que multiplica o risco cardiovascular |
| `resting_ecg` | Resultado do ECG em repouso (0–2) | Sinal objetivo (não autorrelatado) de alterações elétricas cardíacas |
| `max_heart_rate` | Frequência cardíaca máxima atingida em teste de esforço | Capacidade funcional cardiovascular; valores baixos associam-se a pior prognóstico |
| `exercise_angina` | Angina induzida por exercício (1/0) | Sintoma de isquemia miocárdica sob estresse |
| `st_depression` | Depressão do segmento ST induzida por exercício | Marcador quantitativo de isquemia, usado em protocolos clínicos reais |
| `st_slope` | Inclinação do segmento ST no pico do exercício | Complementa `st_depression` na avaliação de isquemia |
| `n_major_vessels` | Nº de vasos principais visíveis em fluoroscopia (0–3) | Medida direta e objetiva de obstrução coronariana |
| `thalassemia` | Resultado do teste de tálio (normal / defeito fixo / defeito reversível) | Indica áreas de perfusão sanguínea comprometida no músculo cardíaco |
| `diagnosis` | Variável-alvo: 0 = sem doença; 1–4 = presença/gravidade de doença cardíaca | Rótulo principal para treinar modelos supervisionados de risco cardíaco |

**Variáveis mais relevantes para um projeto de IA em saúde**, na nossa
avaliação: `age`, `chest_pain_type`, `max_heart_rate`, `st_depression` e
`n_major_vessels` concentram o maior poder discriminativo entre pacientes
com e sem doença nesta base (é o padrão relatado na literatura que usa este
dataset), o que os torna bons candidatos a *features* centrais em modelos de
classificação de risco.

### Qualidade dos dados

- 6 das 303 linhas têm valores ausentes (`?` no arquivo original) nas colunas
  `n_major_vessels` ou `thalassemia` — mantidos como células vazias no CSV,
  em vez de preenchidos artificialmente, para que o tratamento de dados
  faltantes seja uma decisão explícita nas próximas fases (imputação,
  remoção, etc.), e não um viés silencioso introduzido agora.
- Distribuição do alvo (`diagnosis`): 164 sem doença (0), 139 com algum grau
  de doença (1 a 4) — razoavelmente balanceada para fins didáticos.
- Distribuição de sexo: 206 homens / 97 mulheres — **desbalanceamento real**
  da coleta original (ver seção de Governança abaixo).

---

## Parte 2 — Dados Textuais (NLP)

Dois textos em `docs/`, de naturezas diferentes (um histórico/literário, um
científico/contemporâneo), propositalmente, para dar diversidade de
vocabulário e estilo ao futuro pipeline de NLP.

### Texto 1 — [`01_harvey_motion_of_the_heart_1628.txt`](docs/01_harvey_motion_of_the_heart_1628.txt)

- **Título:** *An Anatomical Disquisition on the Motion of the Heart and
  Blood in Animals* (De Motu Cordis, 1628)
- **Autor:** William Harvey — obra fundadora da fisiologia cardiovascular
  moderna, na qual Harvey descreve pela primeira vez a circulação sanguínea.
- **Fonte:** Project Gutenberg (domínio público) —
  https://www.gutenberg.org/ebooks/67065
- **Licença:** domínio público nos EUA; texto redistribuído com a licença
  Project Gutenberg incluída no próprio arquivo.

### Texto 2 — [`02_scielo_fatores_de_risco_cardiovascular.txt`](docs/02_scielo_fatores_de_risco_cardiovascular.txt)

- **Título:** *Fatores de risco para doença cardiovascular: velhos e novos
  fatores de risco, velhos problemas!*
- **Autores:** Raul D. Santos Filho, Tânia L. da Rocha Martinez (InCor,
  HC-FMUSP / Sociedade Brasileira de Cardiologia)
- **Fonte:** SciELO Brasil, Arquivos Brasileiros de Endocrinologia &
  Metabologia —
  https://www.scielo.br/j/abem/a/SQNbwgnV9t5zyNdnCmbYmMb/?lang=pt
- **Licença:** conteúdo de acesso aberto SciELO.

### Como esses textos podem alimentar algoritmos de NLP

- **Extração de entidades/sintomas:** reconhecer termos clínicos (ex.:
  "angina", "hipertensão", "dislipidemia") via NER customizado ou listas de
  termos, para estruturar sintomas e fatores de risco citados em texto livre.
- **Classificação de tópicos:** treinar um classificador para distinguir
  trechos sobre *fatores de risco*, *fisiologia* ou *tratamento* — útil para
  triar literatura médica automaticamente.
- **Análise de sentimento/tom:** embora o texto científico seja
  predominantemente neutro, comparar o tom entre a prosa histórica de Harvey
  e o texto científico contemporâneo é um bom exercício para calibrar
  modelos de estilo/registro textual.
- **Sumarização automática:** gerar resumos de artigos científicos longos
  para apoiar profissionais de saúde com pouco tempo de leitura.

Essas análises são relevantes para um projeto de IA em saúde porque boa
parte do conhecimento médico ainda vive em texto não estruturado (prontuários,
artigos, laudos); NLP é o que permite transformar esse conteúdo em
informação estruturada e acionável pelos demais módulos do CardioIA.

---

## Parte 3 — Dados Visuais (Visão Computacional)

**Conjunto completo (120 imagens, ~26 MB, link público):** `https://drive.google.com/drive/folders/1JxzOJaJ4gQdzVfWKUJKhvED25Ti9pHJ6?usp=drive_link`
**Amostra de preview no próprio repositório:** [`images/sample/`](images/sample/) (12 imagens, 3 por classe)

### Origem dos dados

Imagens **reais** de eletrocardiograma (ECG), extraídas do dataset público
*"ECG Images dataset of Cardiac Patients"*.

- **Autores:** Ali Haider Khan, Muzammil Hussain (University of Management
  and Technology / Ch. Pervaiz Elahi Institute of Cardiology, Multan,
  Paquistão)
- **Fonte:** Mendeley Data — DOI
  [10.17632/gwbz3fsgp8.2](https://data.mendeley.com/datasets/gwbz3fsgp8/2)
- **Licença:** CC BY 4.0 (uso livre com atribuição)
- **Dataset original:** ~929 imagens em 4 classes (Normal, Infarto Agudo do
  Miocárdio, Histórico de Infarto, Batimento Anormal/Arritmia)

### Amostragem

Para manter o repositório leve e, ao mesmo tempo, **evitar herdar o
desbalanceamento de classes do dataset original** (que varia de 172 a 284
imagens por classe), selecionamos uma amostra **balanceada e aleatória** de
**30 imagens por classe (120 no total)**, com semente fixa (`seed=42`) para
reprodutibilidade — ver
[`scripts/select_images_sample.py`](scripts/select_images_sample.py).

| Classe | Imagens na amostra | Imagens disponíveis na fonte |
|---|---|---|
| Normal | 30 | 284 |
| Infarto agudo do miocárdio | 30 | 240 |
| Histórico de infarto | 30 | 172 |
| Arritmia / batimento anormal | 30 | 233 |

### Como essas imagens podem ser analisadas por Visão Computacional

- **Detecção de bordas e extração do traçado:** técnicas clássicas (Canny,
  thresholding) para isolar a curva do ECG do fundo/grade impressa,
  transformando a imagem em um sinal 1D analisável.
- **Reconhecimento de padrões/anomalias:** CNNs treinadas para diferenciar
  os quatro padrões (normal, infarto agudo, histórico de infarto, arritmia),
  simulando uma triagem automática de exames.
- **Detecção de picos e segmentação de ondas (P, QRS, T):** uso de visão
  computacional para localizar automaticamente os complexos QRS e medir
  intervalos, replicando por imagem o que normalmente é feito em sinal
  digital bruto.
- **Comparação com o dataset numérico (Parte 1):** os rótulos de classe das
  imagens (normal vs. patológico) espelham conceitualmente a variável
  `diagnosis` do dataset tabular, permitindo, em fases futuras, comparar o
  desempenho de um modelo tabular com o de um modelo de imagem para a mesma
  pergunta clínica.

A importância dessas análises para IA em saúde está em automatizar uma
primeira leitura de exames em grande volume — reduzindo tempo de triagem e
apoiando (nunca substituindo) o diagnóstico médico especializado.

---

## ⚠️ Governança de Dados e Vieses

Pontos de atenção identificados nesta fase, para que sejam considerados
(e não esquecidos) nas fases seguintes do CardioIA:

- **Desbalanceamento de sexo no dataset numérico** (206 homens / 97
  mulheres): um modelo treinado ingenuamente nessa base tende a performar
  pior para pacientes do sexo feminino — um risco conhecido na literatura de
  IA em cardiologia, já que mulheres historicamente são sub-representadas em
  estudos cardiovasculares e apresentam sintomas mais atípicos.
- **Origem geográfica limitada:** os dados numéricos vêm de populações dos
  EUA/Europa (anos 1980) e as imagens de ECG vêm de um único hospital no
  Paquistão; nenhuma das duas bases é brasileira. Modelos treinados aqui não
  devem ser assumidos como diretamente generalizáveis à população atendida
  pelo CardioIA sem validação local.
- **Dado ausente tratado de forma explícita:** os 6 registros com valores
  ausentes no CSV foram mantidos como campos vazios (não imputados
  automaticamente), para que a estratégia de tratamento seja uma decisão
  deliberada e documentada em fases posteriores, e não um viés introduzido
  silenciosamente agora.
- **Amostragem balanceada nas imagens:** optamos por 30 imagens por classe
  (em vez de usar a distribuição original desbalanceada) justamente para não
  propagar, sem discussão, um viés de classe para os módulos de Visão
  Computacional das próximas fases.
- **Dados clínicos sensíveis:** mesmo sendo bases públicas e anonimizadas,
  ambas envolvem dados de pacientes reais; qualquer uso além deste exercício
  acadêmico exigiria revisão de privacidade/consentimento e adequação a
  regulações como a LGPD.

## 🗃 Histórico de lançamentos

* 0.1.0 - 01/09/2026
    * Fase 1: dataset numérico (UCI Heart Disease), textos (Harvey + SciELO)
      e amostra balanceada de imagens de ECG (Mendeley), com documentação de
      origem, dicionário de variáveis e considerações de Governança de
      Dados e Vieses.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

As licenças específicas de cada base de dados usada neste repositório (UCI
Heart Disease, Project Gutenberg, SciELO e Mendeley Data) estão detalhadas
nas seções "Parte 1", "Parte 2" e "Parte 3" acima.
