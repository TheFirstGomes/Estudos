# 🌾 Sistema de Monitoramento de Colheita de Cana-de-Açúcar

## 🧠 Tema do Projeto
**Análise Preditiva de Manutenção de Colhedoras de Cana-de-Açúcar**

---

## 🎯 Objetivo
Desenvolver uma aplicação em **Python** conectada ao **Oracle Database**, capaz de **monitorar, registrar e prever perdas de produção** em colheitas de cana-de-açúcar.

O sistema simula dados reais e fornece **alertas preditivos** sobre possíveis **desgastes em componentes críticos das colhedoras** (como facas de corte), com base em variáveis de campo como:
- Horas de uso (implícitas nos dados);
- Umidade do solo;
- Volume processado (produção e perdas);
- Eficiência operacional.

---

## 🧩 Justificativa
A cana-de-açúcar representa uma das principais culturas do agronegócio brasileiro.  
Estudos da **UNESP** e **SOCICANA** apontam que **o desgaste precoce dos equipamentos de colheita** é responsável por perdas significativas de produtividade e aumento de custos operacionais.

Este projeto traz uma abordagem de **Ciência de Dados e IoT Simulada**, permitindo:
- Antecipar falhas operacionais;
- Reduzir custos com manutenção;
- Melhorar o rendimento agrícola e industrial.

---

## ⚙️ Funcionalidades do Sistema
O sistema é executado via **menu interativo em terminal** e permite:

| Opção | Descrição |
|-------|------------|
| **1** | Gerar dados simulados e exportar em JSON |
| **2** | Inserir dados simulados automaticamente no banco Oracle |
| **3** | Inserir dados manualmente (interação com o usuário) |
| **4** | Consultar e gerar relatório estatístico |
| **5** | Gerar relatório preditivo com alertas de perda |
| **6** | Recriar a tabela `PERDAS_CANA` do zero (limpar base) |

---

## 🧮 Conteúdos Técnicos Atendidos (Capítulos 3 a 6 - FIAP)

| Conteúdo | Implementação no Projeto |
|-----------|--------------------------|
| **Subalgoritmos (funções e procedimentos)** | Classes e métodos modulares (`OracleDB`, `Utils`, `Relatorios`, etc.) |
| **Estruturas de dados (lista, tupla, dicionário)** | Uso em geração de dados (`list`), parâmetros SQL (`tuple`) e registros JSON (`dict`) |
| **Manipulação de arquivos (texto e JSON)** | Exportação de dados simulados para `dados_cana_perdas.json` |
| **Conexão com Banco de Dados Oracle** | Implementada com `oracledb.connect()` em `database.py`, com criação automática da tabela |
| **Tratamento de erros e validação de entrada** | Todos os menus possuem checagem de entrada e mensagens amigáveis |

---

## 🧱 Estrutura do Projeto
📂 Projeto_CanaDeAcucar
├── database.py # Classe OracleDB - conexão, criação e manipulação do banco
├── models.py # Classe PerdaCana - estrutura dos dados
├── utils.py # Classe Utils - geração, exportação e alertas preditivos
├── relatorios.py # Classe Relatorios - análises estatísticas e preditivas
├── inserir_dados.py # Função para inserção manual de registros
├── main.py # Menu principal e controle do sistema
├── dados_cana_perdas.json # Arquivo gerado com dados simulados
└── README.md

--- 

## 🧾 Estrutura da Tabela no Oracle
```sql
CREATE TABLE PERDAS_CANA (
    ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    DATA_COLHEITA DATE,
    REGIAO VARCHAR2(100),
    AREA_HECTARES FLOAT,
    PRODUCAO_TOTAL_TON FLOAT,
    PERDA_TON FLOAT,
    PERCENTUAL_PERDA FLOAT,
    TIPO_COLHEITA VARCHAR2(50),
    UMIDADE_PERCENTUAL FLOAT,
    EFICIENCIA_COLHEITA FLOAT,
    CLASSIFICACAO_PERDA VARCHAR2(20)
);


## 📊 Exemplo de Saída — Relatório Preditivo

| Região             | Tipo de Colheita | Percentual de Perda (%) | Alerta |
|--------------------|------------------|--------------------------|--------|
| São Paulo          | Mecanizada       | 12.15                    | 🚨 ALTO |
| Goiás              | Manual           | 3.00                     | ✅ NORMAL |
| Paraná             | Mecanizada       | 8.76                     | ⚠️ NORMAL |
| Minas Gerais       | Mecanizada       | 14.05                    | 🚨 ALTO |
| Mato Grosso do Sul | Manual           | 3.00                     | ✅ NORMAL |



💡 Inovação e Valor Prático
Uso de dados simulados realistas para modelar perdas de colheita;
Geração automática de alertas preditivos com base em regras estatísticas;
Estrutura pensada para futura integração com sensores IoT reais;
Projeto modular preparado para expansão com modelos de regressão preditiva (Machine Learning).


🚀 Como Executar o Projeto
1️⃣ Instalar dependências
pip install oracledb pandas

2️⃣ Configurar conexão com o banco Oracle
No arquivo database.py, ajuste:
conn = oracledb.connect(
    user='seu_usuario',
    password='sua_senha',
    dsn='oracle.fiap.com.br:1521/ORCL'
)

3️⃣ Executar o sistema
python main.py


👨‍💻 Autor
Luan Gomes (RM566806)
Curso: Inteligência Artificial — FIAP
Fase 2 — Capítulo 6: Python e além


🧩 Observação Final
Este projeto foi desenvolvido com base em estudos e boas práticas de Engenharia de Dados e Ciência de Dados aplicadas ao agronegócio, demonstrando como Python, bancos relacionais e análises preditivas podem gerar valor real e mensurável no campo.

