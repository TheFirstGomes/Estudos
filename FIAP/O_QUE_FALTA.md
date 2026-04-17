# O Que Falta — Tarefas Manuais (Você Precisa Fazer)

Este arquivo lista o que **não foi possível automatizar** e que você precisará fazer manualmente antes de entregar as Sprints 3 e 4.

---

## 🔴 PRIORIDADE ALTA (obrigatório para entregar)

### 1. Gravar e publicar o vídeo da Sprint 4 no YouTube
**Por quê:** O tutor exige um link de vídeo não-listado no YouTube demonstrando o projeto.

**O que gravar (máximo 3 minutos):**
1. Execute `python codes/run.py` e mostre o pipeline rodando (30s)
2. Abra `streamlit run codes/app_sprint4.py` e mostre:
   - Aba Chatbot: digite 2-3 perguntas em pt/en/es e mostre as respostas (1min)
   - Aba Visão Computacional: clique em "Executar Simulação" e mostre os gráficos (30s)
   - Aba Recomendações: gere uma recomendação e explique brevemente (30s)
   - Aba Métricas: mostre os analytics de engajamento (15s)
3. Fale brevemente sobre as decisões técnicas (30s)

**Após gravar:**
- Faça upload no YouTube como "Não listado"
- Copie o link e cole no `README_SPRINT4.md` substituindo `*[Inserir link do YouTube não listado]*`

---

### 2. Inserir link do vídeo Sprint 4 no README_SPRINT4.md

No arquivo [README_SPRINT4.md](README_SPRINT4.md), linha 11, substitua:
```
**Link do Vídeo (Sprint 4):** *[Inserir link do YouTube não listado]*
```
Por:
```
**Link do Vídeo (Sprint 4):** [YouTube — não listado](SEU_LINK_AQUI)
```

---

### 3. Fazer push para o repositório GitHub privado do tutor

```bash
# Na pasta Challenge_FIAP/, execute:
git add .
git commit -m "Sprint 3 e 4: Integração completa + IA Interativa"
git push origin main
```

**Certifique-se de que o tutor (Sabrina Otoni) tem acesso ao repositório privado.**

---

## 🟡 PRIORIDADE MÉDIA (melhora a nota)

### 4. Testar o sistema localmente antes de entregar

Execute estes comandos na pasta `Challenge_FIAP/` e verifique se tudo funciona:

```bash
# Instalar dependências (se ainda não instalou)
pip install -r requirements.txt

# Rodar pipeline completo
python codes/run.py
# → Escolha opção 1 (fluxo completo)
# → Ao final, escolha 4 para abrir o Dashboard Sprint 4

# OU abrir diretamente
streamlit run codes/app_sprint4.py
```

**O que verificar:**
- [ ] Dashboard Sprint 3 abre sem erros: `streamlit run codes/app_streamlit.py`
- [ ] Dashboard Sprint 4 abre sem erros: `streamlit run codes/app_sprint4.py`
- [ ] Chatbot responde a perguntas em pt, en e es
- [ ] Simulação de visão computacional gera gráficos
- [ ] Aba de Recomendações funciona
- [ ] Aba de Segurança: botão "Verificar Integridade" retorna resultados

---

### 5. Criar/atualizar diagrama de arquitetura

O arquivo `document/arquitetura.png` existe da Sprint 1.  
Idealmente, atualize o diagrama para incluir os módulos da Sprint 3 e 4.

**Ferramentas sugeridas:** draw.io (gratuito) ou diagrams.net

**O que incluir no novo diagrama:**
- Todos os módulos Python (setas mostrando o fluxo de dados)
- As 3 tabelas do SQLite
- Os 2 dashboards Streamlit
- Indicação de quais partes são simuladas vs. planejadas para produção

---

### 6. Preencher o README_SPRINT4.md com métricas reais

Após executar o sistema, os valores das métricas no README_SPRINT4.md podem ser atualizados com os valores reais que aparecem no dashboard.  
As métricas atuais são estimativas baseadas nos dados sintéticos gerados.

---

## 🟢 OPCIONAL (se quiser melhorar ainda mais)

### 7. Vídeo da Sprint 3 (se ainda não entregou)
O link do vídeo da Sprint 3 já está preenchido no `README_SPRINT3.md` com o link antigo (`https://youtu.be/gtwXErxIsrk`).  
Se esse vídeo **não demonstra** os módulos da Sprint 3 (security_module, analise_estatistica, app_streamlit com 4 tabs), grave um novo vídeo e atualize o link.

---

### 8. Hardware físico (ESP32/ESP32-CAM)
Todos os módulos de hardware foram **simulados por software** por falta de acesso ao componente físico.  
Para uma demonstração mais próxima do real, seria necessário:
- ESP32-CAM para substituir `visao_computacional.py` por captura real via OpenCV
- ESP32 com sensor PIR para substituir `simulacao_hardware.py`

Isso **não é obrigatório** para a nota — a simulação é documentada e justificada.

---

### 9. Speech-to-Text (voz para texto)
O chatbot atual aceita **texto digitado**.  
Para adicionar entrada por voz (como previsto na arquitetura original), seria necessário:
- `pip install SpeechRecognition pyaudio`
- Integrar com o chatbot no `app_sprint4.py`

Isso também **não é obrigatório** — a interface de texto é funcional e suficiente para demonstração.

---

## 📋 Checklist Final Antes de Entregar

- [ ] Vídeo Sprint 3 no YouTube (link no `README_SPRINT3.md`)
- [ ] Vídeo Sprint 4 no YouTube (link no `README_SPRINT4.md`)
- [ ] Código testado e funcionando localmente
- [ ] Push para o repositório privado do tutor
- [ ] Tutor tem acesso ao repositório
- [ ] READMEs com links de vídeo preenchidos
