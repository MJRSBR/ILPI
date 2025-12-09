# %%
# ---------------------
# Leitura dos dados
# ---------------------
import sys
sys.path.append('/Users/mjrs/Documents/ILPI')

import pandas as pd

from funcoes.f_process import classificar_risco
from funcoes.f_plot import salvar_tabela_como_imagem

df_score = pd.read_csv("../data/SMSAp/lake/mpiScore.csv")
df_score.head()
# %%
## --------------------
##  - COMPONENTES DE FRAGILIDADE
# ## --------------------

condicao_critica = {
    'risk': lambda x: x == 'Alto (MPI 3)'
}

condicao_alerta = {
    'risk': lambda x: x == 'Moderado (MPI 2)'
}

condicao_atencao = {
    'risk': lambda x: x == 'Leve (MPI 1)'
}
# %%

df_score.head(10)[["id_institution", "uuidv5", "full_name", "MPI", "risk"]]
df_score.sort_values(by="MPI", ascending=False)
# %%
top_score = df_score.sort_values(by="MPI", ascending=False).head(20)
top_score

# %%
# Salvando a tabela Top 20 para o lake
top_score.to_csv("../data/SMSAp/lake/mpiTopScore.csv", index=False)
print("✅Tabela MPI Top Score foi salva no lake!")

# %%

salvar_tabela_como_imagem(
    top_score[["id_institution", "uuidv5", "full_name", "MPI", "risk"]],
    'Top20ScoreFragilidade.png',
    titulo='Top 20 Score de Fragilidade do Residente por ILPI',
    largura_total_max=180
)
# %%
## --------------------
##  - COMPONENTES DE FRAGILIDADE
# ## --------------------

resultado, resumo = classificar_risco(df_score, condicao_critica, condicao_alerta, condicao_atencao)
# %%
resultado

# %%
resumo.sort_values(by="total", ascending=False)

# %%

from IPython.display import display, HTML

# Exibe o resultado com cores
display(HTML(resultado.to_html(escape=False)))
# %%
# Mostra o resumo correto
display(HTML(resumo.to_html(escape=False)))
# %%
# ######## PAREI AQUI
# # %%
salvar_tabela_como_imagem(
    resumo,
    'Tabela_resumo_score_fragilidade.png',
    titulo='Score de Fragilidade do Residente por ILPI',
    largura_total_max=100
)
# %%