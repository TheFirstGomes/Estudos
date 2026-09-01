#LuanGoncalvesGomes_RM566806_fase2_cap7

# Análise Exploratória
# Variável: producao_toneladas

# Forma de identificar se todos os packages foram instalados, e caso contrário
# instalar todos de uma única vez. 
packages <- c('readxl', 'ggplot2', 'psych')
instalados <- packages %in% rownames(installed.packages())
if (any(!instalados)) install.packages(packages[!instalados])
lapply(packages, library, character.only=TRUE)

# Dados carregados base do excel
dados <- read_excel('~/Estudos/Estudos/FIAP/Fase2/Cap_07_Decolando_Ciencia_Dados/base_agronecocio.xlsx')
str(dados)

# 1. Média de tendência central: 
media <- round(mean(dados$producao_toneladas), 2)
mediana <- round(median(dados$producao_toneladas), 2)
moda <- as.numeric(names(sort(table(dados$producao_toneladas), decreasing = TRUE)[1]))

cat('Média: ', media, '\n')
cat('Mediana: ', mediana, '\n')
cat('Moda: ', moda, '\n')

# 2. Medidas de dispersão: 
variancia <- round(var(dados$producao_toneladas), 2)
desvio_padrao <- round(sd(dados$producao_toneladas), 2)
amplitude <- round(max(dados$producao_toneladas) - min(dados$producao_toneladas), 2)
coef_var <- round((desvio_padrao / media) * 100, 2)

cat('Variância: ', variancia, '\n')
cat('Desvio Padrão: ', desvio_padrao, '\n')
cat('Amplitude: ', amplitude, '\n')
cat('Coeficiente de Variacão (%): ', coef_var, '\n')

# 3. Medidas separatrizes: 
quartis <- round(quantile(dados$producao_toneladas, probs = c(0.25, 0.5, 0.75)), 2)
decis <- round(quantile(dados$producao_toneladas, probs = seq(0.1, 0.9, 0.1)), 2)
percentis <- round(quantile(dados$producao_toneladas, probs = seq(0.01, 0.99, 0.01)), 2)

cat('Quartis:\n');print(quartis)
cat('Decis:\n');print(decis)
cat('Percentis:\n');print(percentis)

# 4. Análise Gráfica com Histograma com densidade
ggplot(dados, aes(x=producao_toneladas)) + 
  geom_histogram(aes(y = after_stat(density)), bins=15, fill='steelblue', color='white', alpha=0.7) +
  geom_density(color='darkred', linewidth = 1) + 
  labs(title='Distribuição da Produção Agrícola (Toneladas)', 
       x='Produção (Toneladas)',
       y='Densidade') + 
  theme_minimal()

# 5. Resumo Estatístico completo
describe(dados$producao_toneladas)

# 6. Anpalise da variável qualitativa
# variável: classificacao_produtividade

#contagem absoluta e relativa
freq_abs <- table(dados$classificacao_produtividade)
freq_rel <- prop.table(freq_abs) * 100

tabela_freq <- data.frame(
  Classificacao = names(freq_abs), 
  Frequencia = as.numeric(freq_abs), 
  Percentual = round(as.numeric(freq_rel), 2)
)

tabela_freq

# 6.1 Análise gráfica gráfico de barras
ggplot(tabela_freq, aes(x=Classificacao, y=Frequencia, fill=Classificacao)) + 
  geom_bar(stat='identity', color='black') + 
  geom_text(aes(label=paste0(Percentual, '%')), vjust=-0.5, size=4) + 
  labs(title='Distribuição da Classificação de Produtividade',
       x='Classificação', 
       y='Frequência'
  ) + 
  theme_minimal() + 
  theme(text=element_text(size=12), 
        plot.title = element_text(hjust = 0.5, face='bold'))

# 6.2. Análise gráfica com gráfico de pizza
ggplot(tabela_freq, aes(x = "", y = Frequencia, fill = Classificacao)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar("y", start = 0) +
  geom_text(aes(label = paste0(Percentual, "%")), position = position_stack(vjust = 0.5)) +
  labs(title = "Distribuição da Classificação de Produtividade") +
  theme_void() +
  theme(plot.title = element_text(hjust = 0.5, face = "bold"))