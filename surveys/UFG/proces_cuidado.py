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
df = pd.read_csv('../../../../data/UFG/base_ilpi.csv', index=False)
df
# %%
# Renomeando a coluna institution_name para id_institution
df.rename(columns={'institution_name':'id_institution'}, inplace=True)
df
# %%
# Processos de Cuidado
# Área para que o residente possa tomar um banho de sol
# ---------------------
banho_sol = (df[["id_institution", "sunbathing"]]
                   .assign(df_filtered=df["sunbathing"].map({1: "Sim", 2: "Não"}))
                   [["id_institution", "df_filtered"]]
                .rename(columns={"id_institution": "ILPI", "df_filtered": "banho_sol"})
)

banho_sol
# %%
salvar_tabela_como_imagem(
    banho_sol,
    '../../UFG/tables/35_banho_sol.png'
)
# %%
# Gráfico 35 - Área banho de sol
# --------------------------
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
banho_sol.groupby('banho_sol').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Área para que o residente possa tomar um banho de sol')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/35_banho_sol.png")
plt.show()
# %%
# Área recebimento de visitas e familiares
# ----------------------
area_vis_familia = (df[["id_institution", "visiting_area"]]
                   .assign(df_filtered=df["visiting_area"].map({1: "Sim", 2: "Não"}))
                   [["id_institution", "df_filtered"]]
                .rename(columns={"id_institution": "ILPI", "df_filtered": "area_vis_familia"})
)

area_vis_familia
# %%
salvar_tabela_como_imagem(
    area_vis_familia,
    '../../UFG/tables/36_area_vis_familia.png'
)
# %%
# Gráfico 36 - Área recebimento de visitas e familiares
# --------------------------
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
area_vis_familia.groupby('area_vis_familia').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Área recebimento de visitas e familiares')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/36_area_vis_familia.png")
plt.show()
# %%

# Área de atividades sociais
# ---------------------
area_ativ_social = (df[["id_institution", "social_area"]]
                   .assign(df_filtered=df["social_area"].map({1: "Sim", 2: "Não"}))
                   [["id_institution", "df_filtered"]]
                .rename(columns={"id_institution": "ILPI", "df_filtered": "area_ativ_social"})
)

area_ativ_social
# %%
salvar_tabela_como_imagem(
    area_ativ_social,
    '../../UFG/tables/37_area_ativ_social.png'
)
# %%
# Gráfico 37 - Área de atividades sociais
# --------------------------
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
area_ativ_social.groupby('area_ativ_social').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Área de atividades sociais')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/37_area_ativ_social.png")
plt.show()
# %%
# Música ambiente na ILPI
# ---------------------------
musica_ambiente = (df[["id_institution", "ambient_music"]]
                   .assign(df_filtered=df["ambient_music"].map({1: "Sim", 2: "Não"}))
                   [["id_institution", "df_filtered"]]
                .rename(columns={"id_institution": "ILPI", "df_filtered": "musica_ambiente"})
)

musica_ambiente
# %%
salvar_tabela_como_imagem(
    musica_ambiente,
    '../../UFG/tables/38_musica_ambiente.png'
)
# %%
# Gráfico 38 - Área de atividades sociais
# --------------------------
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
musica_ambiente.groupby('musica_ambiente').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Área de atividades sociais')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/38_musica_ambiente.png")
plt.show()
# %%
# Cardápio visível para consulta
# ---------------------------
cardapio_visivel = (df[["id_institution", "menu"]]
                   .assign(df_filtered=df["menu"].map({1: "Sim", 2: "Não"}))
                   [["id_institution", "df_filtered"]]
                .rename(columns={"id_institution": "ILPI", "df_filtered": "cardapio_visivel"})
)

cardapio_visivel
# %%
salvar_tabela_como_imagem(
    cardapio_visivel,
    '../../UFG/tables/39_cardapio_visivel.png'
)
# %%
# Gráfico 39 - Cardápio visível para consulta
# --------------------------
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
cardapio_visivel.groupby('cardapio_visivel').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Cardápio visível para consulta')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/39_cardapio_visivel.png")
plt.show()
# %%
# Frequência que o cardápio é atualizado
# ----------------------------------
freq_atualiz_cardapio = (df[["id_institution", "semanal_menu"]]
                   .assign(df_filtered=df["semanal_menu"].map({1: "Sim", 2: "Não"}))
                   [["id_institution", "df_filtered"]]
                   .rename(columns={"id_institution": "ILPI", "df_filtered": "atualiz_cardapio"})
                   .fillna("Não é informado")
)

freq_atualiz_cardapio 
# %%
salvar_tabela_como_imagem(
    freq_atualiz_cardapio,
    '../../UFG/tables/40_freq_atualiz_cardapio.png'
)
# %%
# Gráfico 40 - Cardápio visível para consulta
# --------------------------
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
freq_atualiz_cardapio.groupby('atualiz_cardapio').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Frequência que o cardápio é atualizado')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/40_atualiz_cardapio.png")
plt.show()
# %%
# Realização de oficinas e atividades
# ---------------------------
oficinas_atividades = (df[["id_institution", "recreation_type___1", "recreation_type___2", "recreation_type___3",
                      "recreation_type___4", "recreation_type___5", "recreation_type___6", "recreation_type___7"]]
                  .assign(
                        oficinas_atividades_list=(
                              df["recreation_type___1"].map(lambda x: 'Oficina de jardinagem' if x == 1 else '') +
                              df["recreation_type___2"].map(lambda x: ', Oficina de costura' if x == 1 else '') +
                              df["recreation_type___3"].map(lambda x: ', Oficina de artesanato' if x == 1 else '') +
                              df["recreation_type___4"].map(lambda x: ', Oficina de marcenaria' if x == 1 else '') +
                              df["recreation_type___5"].map(lambda x: ', Dança de salão' if x == 1 else '') +
                              df["recreation_type___6"].map(lambda x: ', Datas comemorativas' if x == 1 else '') +
                              df["recreation_type___7"].map(lambda x: ', Missas/Cultos Ecumênicos' if x == 1 else '')
                        )
                  )
                  .assign(oficinas_atividades_list=lambda x: x['oficinas_atividades_list'].str.lstrip(', '))  # Limpar vírgula no início da string
                  .rename(columns={"id_institution": "ILPI"})  # Renomeando a coluna
                  [["ILPI", "oficinas_atividades_list"]]  # Selecionando apenas as colunas finais
)

oficinas_atividades

# %%
salvar_tabela_como_imagem(
    oficinas_atividades,
    '../../UFG/tables/41_oficinas_atividades.png'
)
# %%

# --------------------
# Gráfico 41 - Realização de oficinas e atividades

plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
oficinas_atividades.groupby('oficinas_atividades_list').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Realização de oficinas e atividades')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/41_oficinas_atividades.png")
plt.show()
# %%
