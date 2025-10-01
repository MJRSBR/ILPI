# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')
# %%
# --------------------
# Bibliotecas
# --------------------
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
from matplotlib.ticker import MaxNLocator

from utils.utils import criar_diretorios
from funcoes.f_plot import plot_config, salvar_tabela_como_imagem
# %%
# ------------------------------
# Carregando configuraçoes e utilitários
# ------------------------------
# Configuraçao dos gráficos
plot_config()

# Cria diretórios para plots e tabelas
criar_diretorios()
# %%
# ---------------------
# Leitura dos dados
df = pd.read_csv('../../../../data/UFG/base_ilpi.csv')
df
# %%
# Renomeando a coluna institution_name para id_institution
df.rename(columns={'institution_name':'id_institution'}, inplace=True)
df
# %%
# Gerenciamento Resíduos
# ---------------------------
# Separação do lixo (orgânico/reciclável)

reciclagem_lixo = (df[["id_institution", "trash_recicling"]]
                   .assign(df_filtered=df["trash_recicling"].map({1: "Sim", 2: "Não"}))
                   [["id_institution", "df_filtered"]]
                .rename(columns={"id_institution": "ILPI", "df_filtered": "Reciclagem_lixo"})
)

reciclagem_lixo
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    reciclagem_lixo,
    '../../UFG/tables/33_reciclagem_lixo.png'
)
# %%
# Gráfico 33 - Reciclagem de lixo
# --------------------------
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
reciclagem_lixo.groupby('Reciclagem_lixo').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Separação de lixo (orgânico/reciclável)')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/33_reciclagem_lixo.png")
plt.show()
# %%
# Recipientes adequados e devidamente rotulados para descarte dos diferentes tipos de resíduos
# ---------------------------

container_adequados = (df[["id_institution", "trash_container___1", "trash_container___2", "trash_container___3", 
                           "trash_container___4","trash_container___5"]]
                  .assign(
                        container_adequados_list=(
                              df["trash_container___1"].map(lambda x: 'Resíduo infectante' if x == 1 else '') +
                              df["trash_container___2"].map(lambda x: ', Resíduo químico' if x == 1 else '') +
                              df["trash_container___3"].map(lambda x: ', Resíduo radioativo' if x == 1 else '') +
                              df["trash_container___4"].map(lambda x: ', Resíduo perfurocortante' if x == 1 else '') +
                              df["trash_container___5"].map(lambda x: ', Resíduo comum' if x == 1 else '') 
                        )
                  )
                  .assign(container_adequados_list=lambda x: x['container_adequados_list'].str.lstrip(', '))  # Limpar vírgula no início da string
                  .rename(columns={"id_institution": "ILPI"})  # Renomeando a coluna
                  [["ILPI", "container_adequados_list"]]  # Selecionando apenas as colunas finais
)

container_adequados
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    container_adequados,
    '../../UFG/tables/34_container_adequados.png'
)
# %%
# --------------------
# Gráfico 34 - Recipientes adequados e devidamente rotulados para descarte dos diferentes
# tipos de resíduos

plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
container_adequados.groupby('container_adequados_list').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Recipientes adequados/rotulados para descarte dos diferentes tipos de resíduos')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/34_container_adequados.png")
plt.show()
# %%
