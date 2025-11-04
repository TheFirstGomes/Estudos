# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto
## Polyvox  
> (De “Poly” (muitos) + “Vox” (voz): referência ao reconhecimento multilíngue.)

## Nome do grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/luan-g-432896b5/">Luan Gonçalves Gomes</a>


## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b/">Sabrina Otoni</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Coordenador</a>


## 📜 Descrição

Em ambientes turísticos e culturais, como museus, centros de visitação e cabines de informação, é comum a presença de visitantes de diversas regiões e nacionalidades.
A comunicação entre o público e os atendentes, ou até mesmo com totens convencionais, ainda enfrenta barreiras de idioma, sotaque e acessibilidade.

Além disso, muitas dessas estruturas não coletam dados relevantes sobre interesses dos visitantes, padrões de engajamento e fluxos de visitação, o que limita o aprimoramento da experiência e o planejamento estratégico das instituições.

### 💡 Solução Proposta
O Totem Inteligente FlexAI é uma solução interativa desenvolvida para cabines de informação turística e espaços culturais.
Por meio de Inteligência Artificial e sensores integrados, ele é capaz de:
 - Reconhecer o idioma e o sotaque do visitante (português de diferentes regiões, inglês, espanhol, etc.);
- Responder em linguagem natural e adaptar o conteúdo ao perfil do visitante (voz, texto e imagens);
- Fornecer informações culturais e turísticas de forma acessível e inclusiva;
- Registrar dados de interação (tempo de uso, idiomas mais utilizados, temas mais buscados);
- Gerar insights em tempo real para dashboards conectados em nuvem.

### 🌎 Impacto Esperado
A solução promove:
- Inclusão linguística e cultural;
- Engajamento interativo em espaços físicos;
- Coleta inteligente de métricas de comportamento;
- Apoio à tomada de decisão para gestores culturais e turísticos;
- Expansão do ecossistema FlexMedia para novas aplicações de IA em ambientes públicos.

## ⚙️ Tecnologias Utilizadas
O desenvolvimento do Totem Inteligente FlexAI foi planejado com base em uma arquitetura modular, segura e escalável, integrando hardware físico, processamento em nuvem e modelos de Inteligência Artificial.

A seguir, estão listadas as principais tecnologias e componentes definidos para cada camada do sistema.
#### 🧩 1. Hardware e Sensores

| Componente | Função | Justificativa |
| :--- | :--- | :--- |
| ESP32-CAM | Captura de imagem e vídeo | Permite detecção de presença e reconhecimento visual básico, com baixo custo e boa integração IoT. |
| ESP32 | Controle e comunicação entre sensores | Microcontrolador versátil com conectividade Wi-Fi e Bluetooth, ideal para IoT. |
| Sensor PIR (Presença) | Detecção automática de movimento | Ativa o totem ao identificar aproximação de visitantes, otimizando energia. |
| Tela Touch LCD | Interface de interação | Permite navegação intuitiva e feedback visual das respostas da IA. |
| Microfone e Alto-falante | Entrada e saída de áudio | Necessários para interação por voz, reconhecimento de idioma e resposta natural. |

#### ☁️ 2. Infraestrutura de Nuvem e Backend

| Tecnologia | Função | Justificativa |
| :--- | :--- | :--- |
| Google Cloud Platform (GCP) | Hospedagem e integração geral | Fornece APIs avançadas de IA e tradução, com escalabilidade global. |
| Firebase Realtime Database / Firestore | Armazenamento de dados das interações | Armazena métricas e logs de uso em tempo real. |
| Cloud Functions / FastAPI (Python) | Backend e comunicação entre módulos | Garante controle das requisições entre hardware, IA e banco de dados. |
| Cloud Storage / Supabase | Armazenamento de mídia (áudio, imagens, logs) | Solução segura e compatível com dados de IoT e IA. |

#### 🧠 3. Inteligência Artificial e Modelos de Linguagem

| Tecnologia / API | Função | Justificativa |
| :--- | :--- | :--- |
| Google Cloud Speech-to-Text | Conversão de fala para texto em múltiplos idiomas | Permite entender comandos de voz com sotaques regionais e diferentes idiomas. |
| Google Translate API / Hugging Face Transformers | Tradução neural e NLP | Processa a linguagem natural e traduz automaticamente, adaptando a resposta ao idioma detectado. |
| Text-to-Speech (TTS) | Resposta por voz com tom natural | Gera voz sintética em português, inglês e espanhol, personalizada por gênero e sotaque. |
| Modelo de IA Local (Python + TensorFlow Lite) | Classificação e análise offline (fallback) | Permite funcionamento mesmo em locais sem conexão constante à internet. |

#### 🔐 4. Segurança e Privacidade

| Recurso | Função | Justificativa |
| :--- | :--- | :--- |
| Anonimização de Dados | Remoção de dados pessoais identificáveis | Conformidade com a LGPD e proteção à privacidade dos visitantes. |
| Criptografia TLS/SSL | Comunicação segura entre dispositivos e nuvem | Evita interceptação de dados sensíveis durante transmissões. |
| Controle de Acesso via Tokens JWT | Autenticação segura para APIs e dashboards | Garante que apenas dispositivos e usuários autorizados acessem o sistema. |

#### 🧰 5. Desenvolvimento e Ferramentas de Apoio

| Ferramenta | Função |
| :--- | :--- |
| Python 3.12+ | Linguagem principal para IA e backend |
| FastAPI / Flask | Framework para criação de APIs leves e seguras |
| draw.io / diagrams.net | Criação dos diagramas de arquitetura |
| GitHub | Controle de versão e documentação colaborativa |
| Visual Studio Code | IDE principal de desenvolvimento |
| Docker (futuro) | Padronização do ambiente de execução |

#### 🪙 6. Blockchain e Registro Imutável (Visão Futura)

| Tecnologia / Framework | Função | Justificativa |
| :--- | :--- | :--- |
| Ethereum / Polygon / Avalanche (Layer 2) | Rede descentralizada para registro imutável de dados | Permite validar e registrar interações do totem (ex: feedbacks, dados de engajamento) de forma transparente e auditável. |
| IPFS (InterPlanetary File System) | Armazenamento distribuído de mídia e logs | Garante persistência e integridade de dados de forma descentralizada, útil para registros públicos e culturais. |
| Smart Contracts (Solidity) | Automação de registros e consentimentos | Permite criar contratos automáticos para registro de uso e validação de consentimento do visitante, em conformidade com a LGPD. |
| NFTs Culturais (ERC-721 / ERC-1155) | Tokens não fungíveis de engajamento cultural | Possibilita emissão de certificados digitais de visita ou conquistas, fomentando o turismo e a gamificação da experiência. |

#### 🚀 7. Escalabilidade e Futuras Integrações
O projeto foi planejado para evoluir em futuras sprints com:
- Integração com dashboards interativos (Google Data Studio / Power BI);
- Expansão para novos idiomas e sotaques regionais;
- Adição de sensores complementares (clima, temperatura, contagem de fluxo de pessoas);
- Módulo de recomendação cultural com IA generativa.

## 🧱 Esboço da Arquitetura da Solução
![Arquitetura do Totem FlexAI](document/arquitetura.png)

#### 🧠 Camadas da Arquitetura
| Camada | Componentes | Função |
| :--- | :--- | :--- |
| **1. Edge / IoT (Totem Físico)** | ESP32, ESP32-CAM, sensores PIR, microfone, alto-falante, tela touch | Captura dados do ambiente e do usuário, realiza pré-processamento e envia solicitações para o backend. |
| **2. Processamento e IA** | Python, FastAPI, APIs de IA (Speech-to-Text, Translate, Text-to-Speech) | Processa os dados capturados, identifica idioma e gera respostas inteligentes personalizadas. |
| **3. Nuvem e Armazenamento** | Google Cloud Platform, Firebase, Supabase | Armazena dados das interações, mídias e logs, permitindo consultas em tempo real e segurança na nuvem. |
| **4. Dashboard e Analytics** | Google Data Studio, Power BI, Grafana | Fornece visualização dos dados de engajamento e comportamento dos visitantes para instituições culturais. |

#### 🔄 Fluxo de Dados Simplificado
Etapa	Descrição
1️⃣	Visitante se aproxima → sensor PIR ativa o totem.
2️⃣	Microfone e câmera capturam voz e presença.
3️⃣	Totem envia áudio para a API Speech-to-Text.
4️⃣	Backend interpreta idioma, traduz e gera resposta via IA.
5️⃣	Totem reproduz a resposta por voz e texto na tela.
6️⃣	Dados anônimos da interação são enviados para o banco em nuvem.
7️⃣	Dashboard exibe métricas e estatísticas de uso.

#### 🔒 Aspectos de Segurança na Arquitetura
- Comunicação criptografada via HTTPS/TLS.
- Dados anonimizados antes de serem armazenados.
- Tokens JWT para autenticação entre dispositivos e nuvem.
- Logs de auditoria para rastreabilidade e conformidade com LGPD.

## 📊 Estratégia de Coleta de Dados
A estratégia de coleta de dados do Totem Inteligente FlexAI foi planejada para equilibrar inovação tecnológica, privacidade e valor analítico.
O foco está em capturar informações relevantes sobre as interações dos visitantes — sempre de forma anônima, em conformidade com a Lei Geral de Proteção de Dados (LGPD).

#### 🎯 Objetivo da Coleta
- Compreender como os visitantes interagem com o totem (voz, idioma, tempo de uso, temas consultados);
- Aprimorar a experiência personalizada com base no idioma, sotaque e preferências culturais;
- Gerar métricas de engajamento para instituições parceiras (número de interações, idiomas mais utilizados, horários de pico, etc.);
- Treinar e otimizar modelos de IA para detecção de idioma e sotaque regional;
- Apoiar a tomada de decisão estratégica de espaços culturais e turísticos.

#### 📥 Dados Coletados
| Tipo de Dado | Descrição | Finalidade | Tipo de Armazenamento |
| :--- | :--- | :--- | :--- |
| Idioma e Sotaque Detectado | Idioma e variação regional reconhecida pela IA de voz | Aprimorar o reconhecimento e personalização das respostas | Nuvem (Firestore) |
| Tempo de Interação | Duração da conversa com o totem | Medir engajamento e fluxo de visitantes | Nuvem (Firestore) |
| Consultas Realizadas | Assuntos culturais, locais, eventos, rotas | Analisar temas de interesse do público | Nuvem (Firestore) |
| Horário e Local da Interação | Momento e ponto de instalação do totem | Identificar horários de pico e padrões de uso | Nuvem (Firestore) |
| Feedback (opcional) | Avaliação do atendimento (1 a 5 estrelas ou comando verbal) | Calcular satisfação do visitante | Nuvem (Firestore) |
| Dados de Hardware (logs) | Status dos sensores, temperatura e uptime do dispositivo | Diagnóstico técnico e manutenção preditiva | Local + Nuvem (Cloud Storage) |

#### 🔐 Privacidade e Conformidade (LGPD)

O projeto adota políticas rígidas de segurança e privacidade baseadas na LGPD (Lei 13.709/2018) e nos princípios da Privacy by Design:
| Princípio | Aplicação no Totem FlexAI |
| :--- | :--- |
| **Consentimento** | O visitante é informado de que a interação é anônima e pode interrompê-la a qualquer momento. |
| **Finalidade Específica** | Os dados são coletados exclusivamente para análise de uso e aprimoramento da IA. |
| **Minimização de Dados** | Somente dados essenciais são coletados, sem identificação pessoal. |
| **Anonimização** | Dados de voz são convertidos em texto e descartados após o processamento. |
| **Transparência** | O painel de administração exibe os tipos de dados coletados e seus usos. |
| **Segurança da Informação** | Comunicação criptografada (TLS/SSL), autenticação via tokens JWT e controle de acesso por função. |

#### ☁️ Pipeline de Coleta e Armazenamento

Fluxo resumido do tratamento de dados:

[Visitante Interage]
   ↓
[Sensores / Microfone / Tela Touch]
   ↓
[Totem (ESP32 + IA Local)]
   → Pré-processamento e anonimização
   ↓
[API Backend (FastAPI)]
   → Armazena dados essenciais
   ↓
[Firestore / Cloud Storage]
   → Registra métricas e logs
   ↓
[Dashboard]
   → Exibe estatísticas de uso e engajamento

#### 📈 Exemplos de Métricas Geradas
- Total de interações por dia / semana / mês;
- Idiomas e sotaques mais detectados;
- Tempo médio de uso por visitante;
- Assuntos culturais mais consultados;
- Índice de satisfação do usuário;
- Disponibilidade e uptime dos dispositivos.

#### 🔮 Evolução Futura
Em versões futuras, o sistema poderá:
- Utilizar modelos preditivos para sugerir conteúdos culturais com base em padrões de interação;
- Integrar camada blockchain para registro imutável de métricas e consentimentos;
- Criar painéis interativos para gestores com visualizações personalizadas por localidade e idioma.

## 🗓️ Plano Inicial de Desenvolvimento e Divisão de Responsabilidades
#### 🚀 Etapas de Desenvolvimento

| Fase | Descrição | Entregáveis | Status |
| :--- | :--- | :--- | :--- |
| **Fase 1 – Planejamento e Arquitetura (Sprint 1)** | Definição do escopo, arquitetura técnica, tecnologias e estratégia de dados. | Documentação inicial no GitHub (README, diagramas, plano técnico). | ✅ Concluída |
| **Fase 2 – Protótipo de Hardware (Sprint 2)** | Montagem do totem físico (ESP32, sensores, câmera, microfone). Integração local e comunicação com backend. | Protótipo funcional básico de coleta de voz e presença. | ⏳ Planejada |
| **Fase 3 – Backend e APIs de IA (Sprint 3)** | Criação da API em FastAPI, integração com Speech-to-Text, Translate e Text-to-Speech. | API funcional com tradução e resposta multilíngue. | ⏳ Planejada |
| **Fase 4 – Armazenamento e Dashboard (Sprint 4)** | Integração com Firebase / Supabase e construção de dashboard de métricas (Data Studio ou Power BI). | Painel de visualização de dados em tempo real. | ⏳ Planejada |
| **Fase 5 – Segurança e LGPD (Sprint 5)** | Implementação de criptografia, autenticação JWT e anonimização de dados. | Camada de segurança validada e documentação de conformidade. | ⏳ Planejada |
| **Fase 6 – Testes, Otimização e Blockchain (Futuro)** | Testes de usabilidade e performance. Integração opcional com blockchain para registro imutável de interações. | Versão final escalável e segura. | 🔮 Futuro |

#### 🧠 Distribuição de Responsabilidades (Funções Técnicas)

> Mesmo sendo um projeto individual, as responsabilidades são apresentadas por função técnica para fins acadêmicos e de clareza de papéis.

| Função | Responsável | Principais Atividades |
| :--- | :--- | :--- |
| **Arquiteto de Solução / Desenvolvedor Principal** | [Luan Gomes] | Definição da arquitetura, desenvolvimento backend (FastAPI), integração com APIs e nuvem. |
| **Engenheiro de Hardware / IoT** | [Luan Gomes] | Configuração do ESP32, ESP32-CAM e sensores; programação embarcada e comunicação com API. |
| **Especialista em IA e NLP** | [Luan Gomes] | Implementação de reconhecimento de fala, tradução neural e geração de voz. |
| **Engenheiro de Dados / Cloud** | [Luan Gomes] | Modelagem e integração com Firebase, Firestore e dashboards. |
| **Analista de Segurança / LGPD** | [Luan Gomes] | Planejamento de políticas de anonimização e controle de acesso seguro. |
| **Documentação e Gestão de Projeto** | [Luan Gomes] | Manutenção do repositório GitHub, versionamento e documentação técnica. |

#### 🧾 Cronograma Estimado (Macroplanejamento)

| Semana | Tarefa Principal | Subtarefas | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| 1–2 | Refinamento do escopo e desenho da arquitetura | Finalizar README, diagramas e plano técnico | Documentação validada |
| 3–4 | Protótipo de hardware (ESP32 + sensores) | Configurar sensores PIR, câmera, microfone e comunicação Wi-Fi | Protótipo físico básico |
| 5–6 | Desenvolvimento do backend | Criar API FastAPI + integração com IA (voz e tradução) | Backend funcional |
| 7–8 | Armazenamento e dashboard | Conectar Firebase / Firestore + gerar painel de dados | Dashboard ativo |
| 9–10 | Segurança e testes | Implementar criptografia, tokens JWT e anonimização | Sistema seguro e testado |
| 11+ | Apresentação e refinamento | Ajustes finais e integração opcional com blockchain | Entrega final pronta |

#### 🧩 Metodologia de Trabalho
O desenvolvimento seguirá o modelo ágeis adaptado (Scrum simplificado):
- Reuniões de checkpoint semanais (individuais de revisão).
- Controle de tarefas via GitHub Projects e issues.
- Documentação viva e versionada a cada entrega de sprint.
- Entregas incrementais com feedback contínuo.

#### 🧱 Critérios de Sucesso
- Protótipo do totem funcional e responsivo.
- Reconhecimento e tradução multilíngue precisos.
- Integração estável com nuvem e dashboard.
- Segurança e conformidade com LGPD.
- Documentação completa, clara e atualizada no GitHub.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


