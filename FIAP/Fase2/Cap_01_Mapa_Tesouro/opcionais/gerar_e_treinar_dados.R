# ===============================================================
# FarmTech - Analise em R (Opcional 2)
# - Dataset: hum, ph, N, P, K, pop, rain3h, label
# - Modelos: Regressao Logistica, Arvore de Decisao
# - Saidas: metricas, graficos, coeficientes p/ C++, regras da arvore
# ===============================================================

suppressPackageStartupMessages({
  libs <- c("tidyverse","rsample","yardstick","broom",
            "gt","rpart","rpart.plot","readr")
  missing <- libs[!libs %in% installed.packages()[,"Package"]]
  if (length(missing)) install.packages(missing, repos="https://cloud.r-project.org")
  lapply(libs, library, character.only = TRUE)
})

# ----------------------- Args CLI ------------------------------
args <- commandArgs(trailingOnly = TRUE)
# Uso: Rscript analise_farmtech.R --input dados.csv --outdir outputs --gen N
arg_val <- function(flag, default=NULL) {
  idx <- which(args == flag)
  if (length(idx)==0 || idx==length(args)) return(default)
  args[idx+1]
}
INPUT  <- arg_val("--input",  "dados.csv")
OUTDIR <- arg_val("--outdir", "outputs")
ASSETS <- file.path(OUTDIR, "assets")
GENN   <- arg_val("--gen",    NA)  # se não existir CSV, gerar N linhas (ex: 1000)

dir.create(OUTDIR, showWarnings = FALSE, recursive = TRUE)
dir.create(ASSETS, showWarnings = FALSE, recursive = TRUE)

set.seed(42)

# -------------------- Utilidades -------------------------------
save_png <- function(plot_obj, path, width=7, height=4.5, dpi=160) {
  ggsave(filename = path, plot = plot_obj, width = width, height = height, dpi = dpi)
}

f1_at_tau <- function(prob, label, tau) {
  pred <- ifelse(prob >= tau, 1, 0)
  cm <- table(factor(pred, levels=c(0,1)), factor(label, levels=c(0,1)))
  tn <- cm[1,1]; fp <- cm[2,1]; fn <- cm[1,2]; tp <- cm[2,2]
  precision <- ifelse((tp+fp)==0, 0, tp/(tp+fp))
  recall    <- ifelse((tp+fn)==0, 0, tp/(tp+fn))
  if ((precision+recall)==0) return(list(f1=0, precision=precision, recall=recall))
  f1 <- 2*precision*recall/(precision+recall)
  list(f1=f1, precision=precision, recall=recall)
}

gen_sintetico <- function(n=1000) {
  hum    <- runif(n, 10, 90)
  ph     <- runif(n, 4.5, 8.0)
  N      <- rbinom(n, 1, 0.6)
  P      <- rbinom(n, 1, 0.6)
  K      <- rbinom(n, 1, 0.6)
  pop    <- runif(n, 0, 1)
  # chuva 3h, maioria baixa, cauda direita
  rain3h <- rgamma(n, shape = 2, rate = 1.2)
  
  latent <- (hum < 35 & ph >= 6 & ph <= 6.8 & (N + P + K == 3) & pop < 0.5 & rain3h < 2)
  label  <- rbinom(n, 1, ifelse(latent, 0.85, 0.15))
  tibble(hum, ph, N, P, K, pop, rain3h, label)
}

export_cpp_block <- function(coefs, tau, out_file){
  # coefs: named numeric vector from glm coef()
  B0    <- unname(coefs[1])
  B_h   <- unname(coefs["hum"])
  B_pH  <- unname(coefs["ph"])
  B_N   <- unname(coefs["N"])
  B_P   <- unname(coefs["P"])
  B_K   <- unname(coefs["K"])
  B_pop <- unname(coefs["pop"])
  B_rain<- unname(coefs["rain3h"])
  txt <- paste0(
    "// ==== MODELO LOGISTICO (gerado em R) ====\n",
    "const float B0    = ", sprintf("%.6f", B0), ";\n",
    "const float B_h   = ", sprintf("%.6f", B_h), ";\n",
    "const float B_pH  = ", sprintf("%.6f", B_pH), ";\n",
    "const float B_N   = ", sprintf("%.6f", B_N), ";\n",
    "const float B_P   = ", sprintf("%.6f", B_P), ";\n",
    "const float B_K   = ", sprintf("%.6f", B_K), ";\n",
    "const float B_pop = ", sprintf("%.6f", B_pop), ";\n",
    "const float B_rain= ", sprintf("%.6f", B_rain), ";\n",
    "const float TAU   = ", sprintf("%.4f", tau), ";\n",
    "\n",
    "float probIrrigacao(float hum, float ph, bool N_ok, bool P_ok, bool K_ok, float pop, float rain3h) {\n",
    "  float xN = N_ok ? 1.0f : 0.0f;\n",
    "  float xP = P_ok ? 1.0f : 0.0f;\n",
    "  float xK = K_ok ? 1.0f : 0.0f;\n",
    "  float z  = B0 + B_h*hum + B_pH*ph + B_N*xN + B_P*xP + B_K*xK + B_pop*pop + B_rain*rain3h;\n",
    "  float prob = 1.0f / (1.0f + expf(-z));\n",
    "  return prob;\n",
    "}\n"
  )
  writeLines(txt, out_file)
}

extract_rules <- function(tree, out_file){
  leaves <- rownames(tree$frame[tree$frame$var=="<leaf>",])
  paths <- path.rpart(tree, nodes = leaves)
  rules <- sapply(paths, function(p) paste(p, collapse=" & "))
  rules <- gsub("^root & ", "", rules)
  writeLines(rules, out_file)
  invisible(rules)
}

# -------------------- Carregar/Gerar Dados ---------------------
if (file.exists(INPUT)) {
  message("-> Lendo dataset: ", INPUT)
  dados <- read_csv(INPUT, show_col_types = FALSE,
                    col_types = cols(
                      hum=col_double(), ph=col_double(),
                      N=col_double(), P=col_double(), K=col_double(),
                      pop=col_double(), rain3h=col_double(),
                      label=col_double()
                    ))
} else {
  n <- if (is.na(GENN)) 1000 else as.integer(GENN)
  message("-> '", INPUT, "' não encontrado. Gerando dataset sintético com n=", n)
  dados <- gen_sintetico(n)
  write_csv(dados, INPUT)
  message("-> Sintético salvo em: ", INPUT)
}

# Sanidade
stopifnot(all(c("hum","ph","N","P","K","pop","rain3h","label") %in% names(dados)))
dados <- dados %>%
  mutate(
    label = factor(label, levels=c(0,1))
  )

# -------------------- Split ---------------------
set.seed(123)
split <- initial_split(dados, prop = 0.8, strata = label)
train <- training(split)
test  <- testing(split)

# ----------------- Regressao Logistica -----------
mod_log <- glm(label ~ hum + ph + N + P + K + pop + rain3h,
               data = train, family = binomial())
saveRDS(mod_log, file.path(OUTDIR, "modelo_logistico.rds"))

# Probabilidades
test$prob_log <- predict(mod_log, newdata = test, type = "response")

# Varre thresholds p/ melhor F1
taus <- seq(0.20, 0.80, by=0.01)
scores <- map_dfr(taus, function(t) {
  m <- f1_at_tau(test$prob_log, as.numeric(as.character(test$label)), t)
  tibble(tau=t, precision=m$precision, recall=m$recall, f1=m$f1)
})
best <- scores %>% arrange(desc(f1)) %>% slice(1)

# Métricas no melhor tau
tau <- best$tau[1]
pred_log <- ifelse(test$prob_log >= tau, 1, 0)
precision_val <- precision_vec(truth = test$label, estimate = factor(pred_log, levels=c(0,1)), event_level = "second")
recall_val    <- recall_vec(truth = test$label, estimate = factor(pred_log, levels=c(0,1)), event_level = "second")
f1_val        <- f_meas_vec(truth = test$label, estimate = factor(pred_log, levels=c(0,1)), beta=1, event_level = "second")
roc_val       <- roc_auc(test, truth = label, prob_log, event_level = "second")

# Tabela de métricas (gt)
metrics_tbl <- tibble(
  Métrica = c("Precision","Recall","F1","ROC AUC"),
  Valor   = c(precision_val, recall_val, f1_val, roc_val$.estimate)
) %>% mutate(Valor = sprintf("%.3f", as.numeric(Valor)))

gt_metrics <- metrics_tbl %>%
  gt() %>%
  tab_header(
    title = md("**Desempenho (Teste) — Regressão Logística**"),
    subtitle = md(paste0("Threshold (τ) = **", sprintf('%.2f', tau), "**"))
  ) %>%
  fmt_markdown(columns = everything())

gtsave(gt_metrics, filename = file.path(ASSETS, "metricas_logistica.png"))

# Curva ROC
roc_df <- yardstick::roc_curve(test, truth = label, prob_log, event_level = "second")
p_roc <- ggplot(roc_df, aes(1 - specificity, sensitivity)) +
  geom_line(size=1) + geom_abline(linetype=2) +
  labs(title = sprintf("Curva ROC (AUC = %.3f)", roc_val$.estimate),
       x="1 - Especificidade", y="Sensibilidade") +
  theme_minimal(base_size = 12)
save_png(p_roc, file.path(ASSETS, "roc_logistica.png"))

# F1 vs tau
p_f1 <- ggplot(scores, aes(tau, f1)) +
  geom_line(size=1) +
  geom_point(data=best, aes(tau, f1), size=2) +
  labs(title="F1 vs. Threshold (τ)", x="τ", y="F1") +
  theme_minimal(base_size = 12)
save_png(p_f1, file.path(ASSETS, "f1_vs_tau.png"))

# Importância por |coef|
coefs_tbl <- broom::tidy(mod_log) %>%
  filter(term != "(Intercept)") %>%
  mutate(Importance = abs(estimate),
         term = factor(term, levels = term[order(Importance)]))
p_imp <- ggplot(coefs_tbl, aes(Importance, term)) +
  geom_col() +
  labs(title="Importância (|coeficiente|) — Regressão Logística",
       x="|Coef|", y=NULL) +
  theme_minimal(base_size = 12)
save_png(p_imp, file.path(ASSETS, "importancia_coef.png"))

# Exportar bloco C++ (coeficientes + TAU)
coefs <- coef(mod_log) # (Intercept), hum, ph, N, P, K, pop, rain3h
export_cpp_block(coefs, tau, file.path(OUTDIR, "bloco_cpp_logistica.txt"))

# ----------------- Arvore de Decisao ---------------------------
mod_tree <- rpart(label ~ hum + ph + N + P + K + pop + rain3h,
                  data = train, method = "class",
                  control = rpart.control(cp = 0.005, minsplit = 20))
saveRDS(mod_tree, file.path(OUTDIR, "modelo_arvore.rds"))

# Predição prob classe 1
test$prob_tree <- predict(mod_tree, newdata = test, type = "prob")[, "1"]

# Varre tau para árvore (igual)
scores_tree <- map_dfr(taus, function(t) {
  m <- f1_at_tau(test$prob_tree, as.numeric(as.character(test$label)), t)
  tibble(tau=t, precision=m$precision, recall=m$recall, f1=m$f1)
})
best_tree <- scores_tree %>% arrange(desc(f1)) %>% slice(1)

# Métricas da árvore
tau_t <- best_tree$tau[1]
pred_tree <- ifelse(test$prob_tree >= tau_t, 1, 0)
precision_t <- precision_vec(truth=test$label, estimate=factor(pred_tree, levels=c(0,1)), event_level="second")
recall_t    <- recall_vec(truth=test$label, estimate=factor(pred_tree, levels=c(0,1)), event_level="second")
f1_t        <- f_meas_vec(truth=test$label, estimate=factor(pred_tree, levels=c(0,1)), beta=1, event_level="second")
roc_t       <- roc_auc(test, truth=label, estimate=prob_tree, event_level="second")

metrics_tree <- tibble(
  Métrica = c("Precision","Recall","F1","ROC AUC"),
  Valor   = c(precision_t, recall_t, f1_t, roc_t$.estimate)
) %>% mutate(Valor = sprintf("%.3f", as.numeric(Valor)))

gt_tree <- metrics_tree %>%
  gt() %>%
  tab_header(
    title = md("**Desempenho (Teste) — Árvore de Decisão**"),
    subtitle = md(paste0("Threshold (τ) = **", sprintf('%.2f', tau_t), "**"))
  ) %>%
  fmt_markdown(columns = everything())

gtsave(gt_tree, filename = file.path(ASSETS, "metricas_arvore.png"))

# Plot da árvore
png(file.path(ASSETS, "arvore_plot.png"), width=900, height=600)
rpart.plot(mod_tree, main="Árvore de Decisão — FarmTech")
dev.off()

# Exportar regras em texto
rules <- extract_rules(mod_tree, file.path(OUTDIR, "regras_arvore.txt"))

# ----------------- Relatorio curto (stdout) -------------------
cat("\n================= RESUMO =================\n")
cat("Dataset: ", INPUT, " | Linhas: ", nrow(dados), "\n")
cat("Saidas em: ", OUTDIR, "\n\n")

cat("[LOGISTICA]\n")
cat("  Melhor τ: ", sprintf("%.2f", tau),
    " | Precision: ", sprintf("%.3f", as.numeric(precision_val)),
    " | Recall: ", sprintf("%.3f", as.numeric(recall_val)),
    " | F1: ", sprintf("%.3f", as.numeric(f1_val)),
    " | ROC AUC: ", sprintf("%.3f\n", roc_val$.estimate), sep="")
cat("  Coeficientes salvos em: ", file.path(OUTDIR, "bloco_cpp_logistica.txt"), "\n\n")

cat("[ARVORE]\n")
cat("  Melhor τ: ", sprintf("%.2f", tau_t),
    " | Precision: ", sprintf("%.3f", as.numeric(precision_t)),
    " | Recall: ", sprintf("%.3f", as.numeric(recall_t)),
    " | F1: ", sprintf("%.3f", as.numeric(f1_t)),
    " | ROC AUC: ", sprintf("%.3f\n", roc_t$.estimate), sep="")
cat("  Regras salvas em: ", file.path(OUTDIR, "regras_arvore.txt"), "\n")

cat("\n[ASSETS gerados]\n")
cat("  - assets/metricas_logistica.png\n")
cat("  - assets/roc_logistica.png\n")
cat("  - assets/f1_vs_tau.png\n")
cat("  - assets/importancia_coef.png\n")
cat("  - assets/metricas_arvore.png\n")
cat("  - assets/arvore_plot.png\n")
cat("===========================================\n")
