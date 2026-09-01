"""
Fase 7 — IA Como Fertilizante Digital
Cap. 1 — A Consolidação de um Sistema

Dashboard unificado FarmTech Solutions.
Integra os serviços das Fases 1 a 6 em uma única interface Streamlit.

Execução:
    cd FIAP/Fase7/FarmTech
    streamlit run dashboard/app.py
"""

import sys
import os
from pathlib import Path

# Garante que src/ seja encontrável independente do cwd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

# ── Importações dos módulos das fases ─────────────────────────────────────────
from src.fase1.area_insumos import (
    calcular_area_retangular, calcular_area_circular, calcular_area_triangular,
    calcular_insumos, calcular_custo_estimado, consultar_clima, clima_simulado,
)
from src.fase2.database import (
    inicializar_db, listar_culturas, inserir_cultura, deletar_cultura,
    atualizar_cultura, inserir_leitura, ultimas_leituras,
    registrar_irrigacao, historico_irrigacao,
    registrar_colheita, listar_colheitas,
)
from src.fase3.iot_simulacao import ler_sensores, decidir_bomba, simular_ciclo
from src.fase5.aws_alertas import processar_e_enviar, verificar_thresholds
from src.fase6.visao import analisar_imagem, sumarizar_batch, CLASSES_SAUDE

# Fase 4 — ML (carregamento tolerante a falha)
try:
    from src.fase4.ml_inferencia import fazer_previsoes, gerar_acoes, carregar_dados_teste_rendimento
    ML_DISPONIVEL = True
except Exception as _ml_err:
    ML_DISPONIVEL = False
    _ML_ERRO = str(_ml_err)


# ── Configuração da Página ────────────────────────────────────────────────────

st.set_page_config(
    page_title="FarmTech | Fase 7",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.image("https://img.icons8.com/emoji/96/tractor-emoji.png", width=80)
    st.title("FarmTech Solutions")
    st.caption("Fase 7 — IA Como Fertilizante Digital\nCap. 1 — A Consolidação de um Sistema")
    st.divider()

    # Inicializa o banco ao abrir
    if "db_inicializado" not in st.session_state:
        try:
            inicializar_db()
            st.session_state["db_inicializado"] = True
        except Exception as e:
            st.error(f"Erro ao inicializar banco: {e}")

    culturas = listar_culturas()
    nomes_cult = [f"#{c['id_cultura']} — {c['nome']}" for c in culturas]
    cultura_sel_idx = st.selectbox(
        "Cultura ativa", range(len(nomes_cult)),
        format_func=lambda i: nomes_cult[i] if nomes_cult else "—",
    ) if nomes_cult else 0
    cultura_ativa = culturas[cultura_sel_idx] if culturas else None

    st.divider()
    st.caption("Navegue pelas abas para acessar cada fase.")

# ── Abas principais ───────────────────────────────────────────────────────────

abas = st.tabs([
    "🏠 Visão Geral",
    "📐 Fase 1-2 · Área & Banco",
    "🤖 Fase 3 · IoT & Irrigação",
    "🧠 Fase 4 · ML Preditivo",
    "🔔 Fase 5 · Alertas AWS",
    "👁️ Fase 6 · Visão Computacional",
])


# ═══════════════════════════════════════════════════════════════════════════════
# ABA 1 — VISÃO GERAL
# ═══════════════════════════════════════════════════════════════════════════════
with abas[0]:
    st.header("🌾 FarmTech Solutions — Sistema Integrado")
    st.markdown(
        "Dashboard unificado que consolida todos os serviços desenvolvidos nas **Fases 1 a 6** "
        "do projeto FarmTech. Selecione uma aba para acessar cada módulo."
    )

    c1, c2, c3, c4 = st.columns(4)
    leituras = ultimas_leituras(limite=100)
    irrig    = historico_irrigacao(limite=100)
    colheitas = listar_colheitas()

    c1.metric("Culturas cadastradas", len(culturas))
    c2.metric("Leituras de sensor", len(leituras))
    c3.metric("Eventos de irrigação", len(irrig))
    c4.metric("Colheitas registradas", len(colheitas))

    st.divider()
    st.subheader("Fases integradas neste sistema")
    fases = [
        ("Fase 1", "Base de Dados", "Cálculos de área, insumos e API meteorológica OpenWeatherMap."),
        ("Fase 2", "Banco Relacional", "Schema SQLite com CRUD para culturas, sensores, irrigação e colheitas."),
        ("Fase 3", "IoT & Automação", "Simulação ESP32: DHT22, LDR (pH), N/P/K, lógica de irrigação inteligente."),
        ("Fase 4", "Data Science / ML", "Random Forest para previsão de umidade, pH e rendimento esperado."),
        ("Fase 5", "Cloud & Alertas", "Serviço de mensageria AWS SNS com disparo de e-mail/SMS por threshold."),
        ("Fase 6", "Visão Computacional", "Classificação de saúde da plantação via OpenCV (YOLO/MobileNetV2 plugável)."),
    ]
    for codigo, titulo, desc in fases:
        with st.expander(f"**{codigo} — {titulo}**"):
            st.write(desc)

    if leituras:
        st.divider()
        st.subheader("Últimas 10 leituras de sensor")
        df_leit = pd.DataFrame(leituras[:10])
        st.dataframe(df_leit[["timestamp", "umidade_solo", "ph", "nitrogenio",
                                "fosforo", "potassio", "bloquear_irrig"]], use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ABA 2 — FASE 1-2: ÁREA & BANCO
# ═══════════════════════════════════════════════════════════════════════════════
with abas[1]:
    st.header("📐 Fase 1 — Cálculo de Área e Insumos")

    col_form, col_res = st.columns(2)

    with col_form:
        st.subheader("Parâmetros da área de plantio")
        formato = st.selectbox("Formato da área", ["Retangular", "Circular", "Triangular"])

        if formato == "Retangular":
            comp = st.number_input("Comprimento (m)", 1.0, 10000.0, 500.0)
            larg = st.number_input("Largura (m)", 1.0, 10000.0, 300.0)
            area_m2 = calcular_area_retangular(comp, larg)
        elif formato == "Circular":
            raio = st.number_input("Raio (m)", 1.0, 5000.0, 200.0)
            area_m2 = calcular_area_circular(raio)
        else:
            base = st.number_input("Base (m)", 1.0, 10000.0, 400.0)
            alt  = st.number_input("Altura (m)", 1.0, 10000.0, 250.0)
            area_m2 = calcular_area_triangular(base, alt)

        insumos  = calcular_insumos(area_m2)
        custo    = calcular_custo_estimado(insumos)

    with col_res:
        st.subheader("Resultado")
        st.metric("Área calculada", f"{area_m2:,.1f} m²", f"{area_m2/10000:.2f} ha")
        st.metric("Custo estimado de insumos", f"R$ {custo:,.2f}")
        st.write("**Quantidades de insumos:**")
        df_ins = pd.DataFrame(list(insumos.items()), columns=["Insumo", "Quantidade"])
        st.dataframe(df_ins, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("API Meteorológica (OpenWeatherMap — Fase 1)")
    col_wx1, col_wx2 = st.columns(2)
    with col_wx1:
        lat = st.number_input("Latitude", -35.0, 5.0, -23.55, format="%.4f")
        lon = st.number_input("Longitude", -74.0, -34.0, -46.63, format="%.4f")
        api_key = st.text_input("Chave OpenWeatherMap (opcional)", type="password",
                                help="Deixe em branco para usar dados simulados.")
    with col_wx2:
        if st.button("Consultar clima", type="primary"):
            with st.spinner("Consultando..."):
                dados = consultar_clima(lat, lon, api_key) if api_key else clima_simulado(lat, lon)
            if dados.get("erro"):
                st.error(dados["erro"])
            else:
                st.success(f"**{dados['descricao'].title()}** — {dados['timestamp']}")
                m1, m2 = st.columns(2)
                m1.metric("Temperatura", f"{dados['temperatura_c']} °C")
                m2.metric("Umidade do ar", f"{dados['umidade_ar_pct']}%")
                m1.metric("Prob. de chuva", f"{dados['prob_chuva_pop']*100:.0f}%")
                m2.metric("Chuva prevista (3h)", f"{dados['chuva_3h_mm']} mm")
                if dados["bloquear_irrigacao"]:
                    st.warning("⛈️ Irrigação bloqueada — chuva prevista.")
                else:
                    st.info("☀️ Condições permitem irrigação.")

    st.divider()
    st.header("🗃️ Fase 2 — Banco de Dados Relacional")

    tab_cult, tab_leit, tab_irrig, tab_colh = st.tabs(
        ["Culturas", "Leituras de Sensor", "Irrigação", "Colheitas"]
    )

    with tab_cult:
        st.subheader("Culturas cadastradas")
        df_cult = pd.DataFrame(listar_culturas())
        if not df_cult.empty:
            st.dataframe(df_cult, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma cultura cadastrada.")

        with st.expander("Adicionar nova cultura"):
            nc1, nc2, nc3 = st.columns(3)
            nome_c  = nc1.text_input("Nome", "Soja")
            var_c   = nc2.text_input("Variedade", "Convencional")
            area_c  = nc3.number_input("Área (ha)", 0.1, 10000.0, 10.0)
            if st.button("Cadastrar cultura"):
                inserir_cultura(nome_c, var_c, area_c)
                st.success(f"Cultura '{nome_c}' cadastrada!")
                st.rerun()

        with st.expander("Deletar cultura"):
            ids_cult = [c["id_cultura"] for c in listar_culturas()]
            if ids_cult:
                del_id = st.selectbox("ID da cultura", ids_cult)
                if st.button("Deletar", type="secondary"):
                    deletar_cultura(del_id)
                    st.warning(f"Cultura #{del_id} removida.")
                    st.rerun()

    with tab_leit:
        st.subheader("Últimas leituras de sensor")
        dados_leit = ultimas_leituras(
            id_cultura=cultura_ativa["id_cultura"] if cultura_ativa else None,
            limite=30,
        )
        if dados_leit:
            st.dataframe(pd.DataFrame(dados_leit), use_container_width=True, hide_index=True)
        else:
            st.info("Sem leituras. Execute a Aba 'Fase 3 · IoT' para gerar dados.")

    with tab_irrig:
        st.subheader("Histórico de irrigação")
        dados_irrig = historico_irrigacao(
            id_cultura=cultura_ativa["id_cultura"] if cultura_ativa else None
        )
        if dados_irrig:
            st.dataframe(pd.DataFrame(dados_irrig), use_container_width=True, hide_index=True)
        else:
            st.info("Sem eventos de irrigação registrados.")

    with tab_colh:
        st.subheader("Registro de colheitas")
        col_col1, col_col2 = st.columns(2)
        dados_colh = listar_colheitas(
            id_cultura=cultura_ativa["id_cultura"] if cultura_ativa else None
        )
        if dados_colh:
            with col_col1:
                st.dataframe(pd.DataFrame(dados_colh), use_container_width=True, hide_index=True)
        else:
            st.info("Sem colheitas registradas.")

        with col_col2:
            with st.expander("Registrar colheita"):
                if cultura_ativa:
                    data_colh    = st.date_input("Data da colheita")
                    prod_ton     = st.number_input("Produção (ton)", 0.0, 10000.0, 100.0)
                    perda_ton    = st.number_input("Perda (ton)", 0.0, prod_ton, 5.0)
                    tipo_colh    = st.selectbox("Tipo", ["mecanica", "manual", "semi-mecanica"])
                    if st.button("Registrar"):
                        registrar_colheita(
                            cultura_ativa["id_cultura"],
                            str(data_colh), prod_ton, perda_ton, tipo_colh,
                        )
                        st.success("Colheita registrada!")
                        st.rerun()
                else:
                    st.info("Selecione uma cultura na sidebar.")


# ═══════════════════════════════════════════════════════════════════════════════
# ABA 3 — FASE 3: IoT & IRRIGAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════
with abas[2]:
    st.header("🤖 Fase 3 — IoT & Automação Inteligente (ESP32 Simulado)")
    st.markdown(
        "Simula o comportamento do ESP32 com sensores DHT22 (umidade), "
        "LDR (pH), botões N/P/K e lógica de irrigação baseada em histerese + previsão do tempo."
    )

    col_ctrl, col_out = st.columns([1, 1])

    with col_ctrl:
        st.subheader("Controles do sensor")
        modo_iot = st.radio("Modo", ["Manual", "Automático (aleatório)"], horizontal=True)

        if modo_iot == "Manual":
            umid_in  = st.slider("Umidade do solo (%)", 10.0, 80.0, 40.0, 0.1)
            ph_in    = st.slider("pH do solo", 4.0, 8.0, 6.3, 0.01)
            n_in = st.checkbox("Nitrogênio (N) OK", True)
            p_in = st.checkbox("Fósforo (P) OK", True)
            k_in = st.checkbox("Potássio (K) OK", True)
            pop_in   = st.slider("Probabilidade de chuva", 0.0, 1.0, 0.2, 0.01)
            rain_in  = st.slider("Chuva prevista 3h (mm)", 0.0, 10.0, 0.5, 0.1)
            n_ciclos = 1
        else:
            umid_in = ph_in = None
            n_in = p_in = k_in = None
            pop_in = rain_in = None
            n_ciclos = st.slider("Número de leituras", 1, 20, 5)

        bomba_atual = st.session_state.get("bomba_on", False)
        st.info(f"Estado atual da bomba: {'💧 LIGADA' if bomba_atual else '⛔ DESLIGADA'}")

        if st.button("Executar leitura / ciclo", type="primary"):
            if not cultura_ativa:
                st.error("Selecione uma cultura na sidebar.")
            else:
                if modo_iot == "Manual":
                    leit = ler_sensores(
                        umidade_override=umid_in, ph_override=ph_in,
                        n_ok=n_in, p_ok=p_in, k_ok=k_in,
                        prob_chuva=pop_in, chuva_3h=rain_in,
                    )
                    nova_bomba, motivo = decidir_bomba(leit, bomba_atual)
                    inserir_leitura(
                        id_cultura=cultura_ativa["id_cultura"],
                        umidade=leit["umidade_pct"], ph=leit["ph"],
                        n=int(leit["N_ok"]), p=int(leit["P_ok"]), k=int(leit["K_ok"]),
                        temp=leit["temperatura"], prob_chuva=leit["prob_chuva"],
                        chuva_3h=leit["chuva_3h_mm"], bloquear=leit["wx_block"],
                    )
                    if nova_bomba and not bomba_atual:
                        registrar_irrigacao(
                            id_cultura=cultura_ativa["id_cultura"],
                            duracao_min=15.0, volume_litros=100.0, motivo=motivo,
                        )
                    st.session_state["bomba_on"] = nova_bomba
                    st.session_state["ultimo_ciclo"] = [
                        {**leit, "bomba_on": nova_bomba, "motivo": motivo}
                    ]
                else:
                    eventos = simular_ciclo(
                        n_leituras=n_ciclos,
                        id_cultura=cultura_ativa["id_cultura"],
                    )
                    st.session_state["bomba_on"] = eventos[-1]["bomba_on"]
                    st.session_state["ultimo_ciclo"] = eventos

                st.rerun()

    with col_out:
        st.subheader("Resultado da última leitura")
        ciclo = st.session_state.get("ultimo_ciclo")
        if ciclo:
            df_ciclo = pd.DataFrame(ciclo)
            cols_show = ["timestamp", "umidade_pct", "ph", "N_ok", "P_ok", "K_ok",
                         "wx_block", "bomba_on", "motivo"]
            cols_exist = [c for c in cols_show if c in df_ciclo.columns]
            st.dataframe(df_ciclo[cols_exist], use_container_width=True, hide_index=True)

            if len(df_ciclo) > 1:
                fig, axes = plt.subplots(1, 2, figsize=(10, 3))
                axes[0].plot(df_ciclo["umidade_pct"].values, marker="o", color="#1f77b4")
                axes[0].axhline(35, color="red", linestyle="--", label="Ligar (35%)")
                axes[0].axhline(45, color="orange", linestyle="--", label="Desligar (45%)")
                axes[0].set_title("Umidade do Solo")
                axes[0].set_ylabel("%")
                axes[0].legend(fontsize=7)

                axes[1].plot(df_ciclo["ph"].values, marker="s", color="#2ca02c")
                axes[1].axhline(6.0, color="red", linestyle="--", label="pH mín (6.0)")
                axes[1].axhline(6.8, color="orange", linestyle="--", label="pH máx (6.8)")
                axes[1].set_title("pH do Solo")
                axes[1].legend(fontsize=7)

                plt.tight_layout()
                st.pyplot(fig)
        else:
            st.info("Execute uma leitura para ver os resultados.")


# ═══════════════════════════════════════════════════════════════════════════════
# ABA 4 — FASE 4: ML PREDITIVO
# ═══════════════════════════════════════════════════════════════════════════════
with abas[3]:
    st.header("🧠 Fase 4 — Machine Learning Preditivo (Random Forest)")

    if not ML_DISPONIVEL:
        st.error(f"Modelos da Fase 4 não encontrados. Detalhe: {_ML_ERRO}")
        st.info(
            "Verifique se os arquivos `.joblib` estão em:\n"
            "`FIAP/Fase4/Cap1_Memorizando_Aprendendo_Dados/modelos_treinados/`"
        )
    else:
        col_ml1, col_ml2 = st.columns([1, 1])

        with col_ml1:
            st.subheader("Entrada dos sensores")
            with st.expander("Sensores de campo", expanded=True):
                ml_umid  = st.slider("Umidade atual (%)", 10.0, 80.0, 45.0, 0.1)
                ml_ph    = st.slider("pH atual", 4.0, 8.0, 6.5, 0.01)
                ml_mes   = st.slider("Mês", 1, 12, 10)
                ml_hora  = st.slider("Hora do dia", 0, 23, 14)

            with st.expander("Condições ambientais"):
                ml_pop   = st.slider("Prob. precipitação", 0.0, 1.0, 0.3, 0.01)
                ml_chuva = st.number_input("Chuva prevista (mm/3h)", 0.0, 10.0, 1.0, 0.1)
                ml_block = st.selectbox("Bloqueio meteorológico", [0, 1],
                                        format_func=lambda x: "Sim" if x else "Não")
                ml_n = st.selectbox("N (Nitrogênio)", [0, 1])
                ml_p = st.selectbox("P (Fósforo)", [0, 1])
                ml_k = st.selectbox("K (Potássio)", [0, 1])
                ml_bomba = st.selectbox("Bomba atual", [0, 1],
                                        format_func=lambda x: "Ligada" if x else "Desligada")

            if st.button("Gerar previsões ML", type="primary"):
                entrada_ml = {
                    "umidade": ml_umid, "ph": ml_ph,
                    "nitrogenio": ml_n, "fosforo": ml_p, "postassio": ml_k,
                    "probabilidade_precipitacao": ml_pop, "chuva_3h": ml_chuva,
                    "bloqueio_meteorológico": ml_block,
                    "estado_bomba": ml_bomba, "mes": ml_mes, "hora": ml_hora,
                }
                prev = fazer_previsoes(entrada_ml)
                acoes = gerar_acoes(prev["umidade_prevista"], prev["ph_previsto"],
                                    prev["rendimento_previsto"])
                st.session_state["ml_result"] = {"prev": prev, "acoes": acoes,
                                                   "umid_atual": ml_umid, "ph_atual": ml_ph}

        with col_ml2:
            st.subheader("Previsões e ações sugeridas")
            ml_res = st.session_state.get("ml_result")
            if ml_res:
                prev  = ml_res["prev"]
                acoes = ml_res["acoes"]
                c1, c2, c3 = st.columns(3)
                c1.metric("Umidade prevista", f"{prev['umidade_prevista']:.1f}%",
                          f"{prev['umidade_prevista'] - ml_res['umid_atual']:+.1f}")
                c2.metric("pH previsto", f"{prev['ph_previsto']:.2f}",
                          f"{prev['ph_previsto'] - ml_res['ph_atual']:+.2f}")
                c3.metric("Rendimento estimado", f"{prev['rendimento_previsto']:.1f}")

                st.subheader("Ações corretivas")
                for a in acoes:
                    cor = {"critico": "error", "alerta": "warning", "ok": "success"}.get(
                        a["nivel"], "info"
                    )
                    getattr(st, cor)(f"{a['icone']} {a['mensagem']}")
            else:
                st.info("Ajuste os parâmetros e clique em 'Gerar previsões ML'.")

        st.divider()
        df_teste = carregar_dados_teste_rendimento()
        if df_teste is not None:
            st.subheader("Correlação histórica: Umidade vs. Rendimento (dados de teste)")
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            ax2.scatter(df_teste["umidade"], df_teste["rendimento_esperado"],
                        alpha=0.15, color="#6F42C1", s=10)
            ax2.set_xlabel("Umidade do Solo (%)")
            ax2.set_ylabel("Rendimento Esperado")
            ax2.set_title("Distribuição histórica (conjunto de teste — Fase 4)")
            ax2.grid(linestyle="--", alpha=0.5)
            plt.tight_layout()
            st.pyplot(fig2)

        st.subheader("Métricas dos modelos (Fase 4)")
        metricas = pd.DataFrame({
            "Modelo":  ["Umidade", "pH", "Rendimento Esperado"],
            "MAE":     [7.60, 0.56, 4.00],
            "R²":      [0.078, 0.001, 0.749],
        })
        st.dataframe(metricas.style.highlight_max(subset=["R²"], color="lightgreen"),
                     use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ABA 5 — FASE 6: VISÃO COMPUTACIONAL
# ═══════════════════════════════════════════════════════════════════════════════
with abas[5]:
    st.header("👁️ Fase 6 — Visão Computacional (YOLO / MobileNetV2)")
    st.markdown(
        "Análise de saúde da plantação. Faça upload de imagens ou use o modo "
        "simulado para demonstrar a interface desenvolvida na Fase 6."
    )

    modo_vis = st.radio("Modo de inferência", ["Simulado", "OpenCV (análise de cor)"],
                        horizontal=True)
    modo_key = "simulado" if modo_vis == "Simulado" else "opencv"

    uploads = st.file_uploader(
        "Carregar imagens da lavoura",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )

    col_vis_btn = st.columns([1, 3])
    n_sim = col_vis_btn[0].number_input("Ou gerar N simulações", 1, 20, 5,
                                         help="Ignora uploads se preenchido manualmente.")

    if st.button("Analisar imagens", type="primary"):
        resultados_vis = []
        if uploads:
            for f in uploads:
                raw = f.read()
                res = analisar_imagem(raw, modo=modo_key)
                res["arquivo"] = f.name
                resultados_vis.append(res)
        else:
            for i in range(n_sim):
                resultados_vis.append(analisar_imagem(b"", modo="simulado"))
                resultados_vis[-1]["arquivo"] = f"talhao_{i+1}.jpg"

        st.session_state["vis_resultados"] = resultados_vis

    vis_res = st.session_state.get("vis_resultados")
    if vis_res:
        sumario = sumarizar_batch(vis_res)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total analisado", sumario["total_imagens"])
        c2.metric("Saudáveis",       sumario["saudaveis"])
        c3.metric("Com problema",    sumario["com_problema"])
        c4.metric("Confiança média", f"{sumario['conf_media']*100:.1f}%")

        # Gráfico de distribuição
        dist = sumario["distribuicao"]
        if dist:
            fig3, ax3 = plt.subplots(figsize=(7, 3))
            cores = ["#2ca02c" if k == "Saudável" else "#d62728" for k in dist.keys()]
            ax3.bar(dist.keys(), dist.values(), color=cores)
            ax3.set_title("Distribuição de classificações")
            ax3.set_ylabel("Imagens")
            plt.xticks(rotation=20, ha="right")
            plt.tight_layout()
            st.pyplot(fig3)

        st.subheader("Detalhes por imagem")
        df_vis = pd.DataFrame(vis_res)[["arquivo", "modo", "classe", "confianca",
                                         "deteccoes", "acao"]]
        st.dataframe(
            df_vis.style.apply(
                lambda col: ["background-color: #d4edda" if v == "Saudável"
                             else "background-color: #f8d7da" for v in col],
                subset=["classe"],
            ),
            use_container_width=True, hide_index=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ABA 6 — FASE 5: ALERTAS AWS
# ═══════════════════════════════════════════════════════════════════════════════
with abas[4]:
    st.header("🔔 Fase 5 — Serviço de Alertas AWS SNS")
    st.markdown(
        "Monitora os thresholds dos sensores/modelos e dispara alertas por e-mail/SMS "
        "via **AWS SNS**. Preencha o ARN do tópico para envio real; "
        "deixe em branco para simular."
    )

    col_sns1, col_sns2 = st.columns(2)

    with col_sns1:
        st.subheader("Configuração SNS")
        topic_arn_raw = st.text_input(
            "ARN do tópico SNS",
            value="arn:aws:sns:us-east-2:138532986857:FarmTechAlertas",
            help="Formato: arn:aws:sns:<regiao>:<conta>:<nome-topico>",
        )
        topic_arn = topic_arn_raw.strip()
        if topic_arn:
            st.caption(f"ARN detectado: `{topic_arn}`")

        regiao_aws = st.selectbox("Região AWS", ["us-east-2", "us-east-1", "us-west-2", "sa-east-1"])
        cultura_sns = st.text_input("Cultura / Talhão", "Soja — Talhão A")

        st.subheader("Valores do sensor para testar")
        sns_umid = st.number_input("Umidade (%)", 0.0, 100.0, 28.0, 0.5)
        sns_ph   = st.number_input("pH", 0.0, 14.0, 4.8, 0.01)
        sns_rend = st.number_input("Rendimento previsto", 0.0, 200.0, 15.0, 0.5)

        if st.button("Verificar thresholds e enviar alertas", type="primary"):
            resultados_sns = processar_e_enviar(
                umidade=sns_umid, ph=sns_ph, rendimento=sns_rend,
                cultura=cultura_sns,
                topic_arn=topic_arn,
                regiao=regiao_aws,
            )
            st.session_state["sns_resultado"] = resultados_sns

    with col_sns2:
        st.subheader("Resultado dos alertas")
        sns_res = st.session_state.get("sns_resultado")
        if sns_res is not None:
            if not sns_res:
                st.success("Todos os valores dentro dos limites. Nenhum alerta disparado.")
            else:
                for r in sns_res:
                    a = r["alerta"]
                    cor = "error" if a["severidade"] == "CRITICO" else "warning"
                    getattr(st, cor)(
                        f"**{a['severidade']}** — {a['tipo']}\n\n"
                        f"Valor: **{a['valor']}** | Limite: **{a['limite']}**\n\n"
                        f"Ação: {a['acao']}\n\n"
                        f"Modo: `{r['modo']}` | Enviado: {'Sim ✅' if r['enviado'] else 'Não'}"
                        + (f"\n\n⚠️ Erro: `{r['detalhe']}`" if "erro" in r["modo"] else "")
                    )
        else:
            st.info("Configure os parâmetros e clique em 'Verificar thresholds'.")

        st.divider()
        st.subheader("Thresholds configurados (src/config.py)")
        from src.config import (ALERT_UMIDADE_MIN, ALERT_UMIDADE_MAX,
                                 ALERT_PH_MIN, ALERT_PH_MAX, ALERT_RENDIMENTO_BAIXO)
        thresh_df = pd.DataFrame({
            "Variável": ["Umidade mínima", "Umidade máxima",
                         "pH mínimo", "pH máximo", "Rendimento baixo"],
            "Threshold": [ALERT_UMIDADE_MIN, ALERT_UMIDADE_MAX,
                          ALERT_PH_MIN, ALERT_PH_MAX, ALERT_RENDIMENTO_BAIXO],
            "Unidade": ["%", "%", "pH", "pH", "ton/ha"],
        })
        st.dataframe(thresh_df, use_container_width=True, hide_index=True)

        with st.expander("Como configurar o AWS SNS"):
            st.markdown("""
1. Acesse o **AWS Console → SNS → Topics → Create topic**
2. Tipo: **Standard**; nomeie como `FarmTechAlertas`
3. Copie o **ARN** gerado e cole no campo acima
4. Em **Subscriptions**, adicione um endpoint de e-mail ou SMS
5. Confirme a assinatura pelo e-mail recebido
6. Configure as credenciais AWS localmente via `aws configure` ou variáveis de ambiente:
   ```
   AWS_ACCESS_KEY_ID=...
   AWS_SECRET_ACCESS_KEY=...
   AWS_DEFAULT_REGION=us-east-1
   ```
            """)
