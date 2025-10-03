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
from funcoes.f_process import processa_binario, processa_uma_variavel_com_opcoes
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
# ---------------------
# Serviço Lavanderia
# Separação de roupas limpas e sujas

roupa_segreg = processa_binario(df, 
                                'dirty_clothing_segregation', 
                                'Separacao_roupas_sujas_limpas', 
                                {1: 'Sim', 2: 'Não'}
)

roupa_segreg
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    roupa_segreg,
    '../../UFG/tables/31_roupa_segreg.png'
)
# %%
# -------------------------
# Gráfico 31 - Separação de roupas limpas e sujas

plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
roupa_segreg.groupby('Separacao_roupas_sujas_limpas').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Separação de roupas limpas e sujas')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('Número de ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/31_roupa_segreg.png")
plt.show()
# %%
# Frequência de troca de roupas de cama e toalhas

freq_troca_roupa_cama = (df[["id_institution", "dirty_clothing_change"]]
                  .assign(
                        freq_troca_roupa_cama_list=(
                              df["dirty_clothing_change"].map(lambda x: 'diario' if x == 1 else '') +
                              df["dirty_clothing_change"].map(lambda x: ', semanal' if x == 2 else '') +
                              df["dirty_clothing_change"].map(lambda x: ', quinzenal' if x == 3 else '') +
                              df["dirty_clothing_change"].map(lambda x: ', mensal' if x == 4 else '')
                        )
                  )
                  .assign(freq_troca_roupa_cama_list=lambda x: x['freq_troca_roupa_cama_list'].str.lstrip(', '))  # Limpar vírgula no início da string
                  .rename(columns={"id_institution": "ILPI"})  # Renomeando a coluna
                  [["ILPI", "freq_troca_roupa_cama_list"]]  # Selecionando apenas as colunas finais
)
# %%

# %%

mapa = {
    1: 'diário',
    2: 'semanal',
    3: 'quinzenal',
    4: 'mensal'
}

freq_troca_roupa_cama = processa_uma_variavel_com_opcoes(
    df,
    "dirty_clothing_change",
    "freq_troca_roupa_cama_list",
    mapa
)

freq_troca_roupa_cama
# %%

# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    freq_troca_roupa_cama,
    '../../UFG/tables/32_freq_troca_roupa_cama.png'
)
# %%
# --------------------
# Gráfico 32 - Frequência de troca de roupas de cama e toalhas

plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
freq_troca_roupa_cama.groupby('freq_troca_roupa_cama_list').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Frequência de troca de roupas de cama e toalhas')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('Número de ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/32_freq_troca_roupa_cama.png")
plt.show()

# %%
