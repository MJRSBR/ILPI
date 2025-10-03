# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')
# %%
# --------------------
# Bibliotecas
# --------------------
import pandas as pd
import os

from funcoes.f_process import processa_binario
from funcoes.f_plot import plot_bar_flex_unificado
from funcoes.f_plot import plot_config, plot_barh, salvar_tabela_como_imagem
# %%
# ------------------------------
# Carregando configuraçoes e utilitários
# ------------------------------
# Configuraçao dos gráficos
plot_config()

# Cria diretórios para plots e tabelas
os.makedirs('../../UFG/tables', exist_ok=True)
os.makedirs('../../UFG/plots', exist_ok=True)
# %%
# ---------------------
# Leitura dos dados
df = pd.read_csv('../../../data/UFG/base_ilpi.csv')
df
# %%
# Renomeando a coluna institution_name para id_institution
df.rename(columns={'institution_name':'id_institution'}, inplace=True)
df
# %%
# ---------------------
# NUMERO DE RESIDENTES
# ---------------------
qtde_residentes = (
    df[['id_institution', 'residents_number']]
    .rename(columns={'id_institution': 'ILPI', 'residents_number': 'Número de residentes'})
    .sort_values(by='Número de residentes', ascending=False)
)

qtde_residentes
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    qtde_residentes,
    '../../UFG/tables/01_qtde_residentes.png'
)
# %%
# Gráfico 01 - Qtde Residentes

plot_bar_flex_unificado(
    qtde_residentes,
    'Distribuição Residentes por ILPI',
    '',
    '',
    '../../UFG/plots/01_residentes_ILPI.png',
    col_categoria='ILPI',
    col_grupo='ILPI',
    orientation= 'v',
    value_format='absolute'

)

# %%
# ---------------------
# DISPOSIÇÃO DAS CAMAS DOS RESIDENTES DE ACORDO COM A NORMA
# ---------------------

camas = processa_binario(df, 
                         'residents_bedroom', 
                         'Camas segundo a Norma?', 
                         {1: 'Sim', 2: 'Não'})

camas
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    camas,
    '../../UFG/tables/02_camas.png'
)

# %%
# ---------------------
# Gráfico 1 - Camas segundo a Norma
# Contando os valores de 'Camas segundo a Norma?' (Sim e Não)
camas_count= camas['Camas segundo a Norma?'].value_counts()

plot_barh(
    camas_count,
    'Distribuição de Camas segundo a Norma',
    'Número de ILPIs',
    'Camas de acordo com a norma',
    '../../UFG/plots/02_camas_norma.png',
    obs=2
)
# %%
# ---------------------
# VEÍCULOS
# ---------------------

veiculo = processa_binario(df, 
                         'residents_bedroom', 
                         'Existe veículo à disposição?', 
                         {1: 'Sim', 2: 'Não'})

veiculo
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    veiculo,
    '../../UFG/tables/03_veiculos.png'
)
# %%
#----------------------
# Gráfico 2 - Veículos à disposição da ILPI
# Contando os valores (Sim e Não)
veiculo_counts = veiculo['Existe veículo à disposição?'].value_counts()
veiculo_counts

plot_barh(
    veiculo_counts,
    'Existe veículo à disposição nas ILPIs',
    'Número de ILPIs',
    'veiculos',
    '../../UFG/plots/03_veiculo.png',
    obs=2
)
# %%

