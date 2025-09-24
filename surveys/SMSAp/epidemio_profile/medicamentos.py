# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')

# %%

import pandas as pd

from utils.utils import criar_diretorios
from funcoes.f_plot import plot_config, salvar_tabela_como_imagem, plot_bar_flex_unificado
from funcoes.f_process import extrair_medicamentos
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
# ---------------------
df = pd.read_csv("../../../data/SMSAp/ILPI/base_perfil_epidemiologico.csv",
                 sep=";")
df.head()

## --------------------
## ----- 10 - Medicamentos
## --------------------

# Criar um DF para registro de medicamentos

medic_registro = df[['id_institution', 'recorded']]
medic_registro.head(20)
# %%

# Filtra apenas as linhas que existam dado recorded
medic_registro_grouped = medic_registro[medic_registro['recorded'].notna()].astype({'recorded': 'int64'})
medic_registro_grouped.head(20)
# %%

# Agrupa por 'recorded', usa .size() para contar quantas vezes cada 'recorded' aparece e
# renomeia a coluna de contagem para 'total'
medic_registro_grouped = medic_registro_grouped.groupby('recorded').size().reset_index(name='total')
medic_registro_grouped
# %%
# Calcula a proporção de cada recorded
medic_registro_grouped['proporcao'] = medic_registro_grouped['total'] / medic_registro_grouped['total'].sum()
medic_registro_grouped['proporcao'] = medic_registro_grouped['proporcao'].round(2)
medic_registro_grouped
# %%

# Mapeia a coluna recorded e atribui valor "sim e não"
medic_registro_grouped['recorded'] = medic_registro_grouped['recorded'].map({1: 'Sim', 0: 'Não'})
medic_registro_grouped.rename(columns={'recorded':'Registro medicamentos'}, inplace=True)
medic_registro_grouped
# %%
salvar_tabela_como_imagem(
    medic_registro_grouped,
    '../tables/10_tabela_registro_medic.png',
    largura_max_coluna=25
)

# %%

# Plotagem 

plot_bar_flex_unificado(
    medic_registro_grouped,
    title='Frequência de Registro de Medicamentos do Residente',
    xlabel='',ylabel='Total de Registros',
    filename='../plots/10_gráfico_registro_medicamentos.png',
    orientation='v', 
    value_format='absolute',
    col_valor='total',
    col_categoria='Registro medicamentos',
    show_values=True,
    show_text=False
)
# %%
# Agrupa por 'recorded', usa .size() para contar quantas vezes cada 'recorded' aparece e
# renomeia a coluna de contagem para 'total'
medic_registro_instit = medic_registro.groupby(['id_institution', 'recorded']).size().reset_index(name='total')
medic_registro_instit['recorded'] = medic_registro_instit['recorded'].astype(int)
medic_registro_instit
# %%
# Calcula a proporção de cada recorded para cada ILPI
medic_registro_instit['proporcao'] = medic_registro_instit['total'] / medic_registro_instit.groupby('id_institution')['total'].transform('sum')
medic_registro_instit['proporcao'] = medic_registro_instit['proporcao'].round(2)
medic_registro_instit
# %%
# Mapeia a coluna recorded e atribui valor "sim e não"
medic_registro_instit['recorded'] = medic_registro_instit['recorded'].map({1: 'Sim', 0: 'Não'})
medic_registro_instit.rename(columns={'id_institution':'ILPI', 'recorded':'Registro medicamentos'}, inplace=True)
medic_registro_instit
# %%
# Salva a tabela de registro de medicamentos por ILPI
salvar_tabela_como_imagem(
    medic_registro_instit,
    '../tables/10_tabela_registro_medic_por_ILPI.png',
    largura_max_coluna=25,
)
# %%
# Gráfico registro medicamentos por ILPI percentagem
plot_bar_flex_unificado(
    medic_registro_instit,
    title='Frequência do Registro de Medicamentos dos Residentes por ILPI',
    xlabel='', ylabel='Total de Registros',
    filename='../plots/10_grafico_registro_medic_por_ILPI_percent.png',
    orientation='v',
    value_format='percent',
    show_values=True,
    show_text=False,
    col_categoria='ILPI',
    col_valor='total',
)
# %%
# Usar a funçao para montar uma tabela com os medicamentos
medic_por_residente = extrair_medicamentos(df)
medic_por_residente.head(20)
# %%
# # Agrupa por 'ILPI'', usa .size() para contar quantas vezes cada suporte aparece e
# renomeia a coluna de contagem para 'total'
contagem_medic_por_residente = medic_por_residente.groupby(['id_institution','uuidv5','full_name']).size().reset_index(name='Qtde Medicamentos')
contagem_medic_por_residente.head(20)
# %%
# Cria a tabela Contagem Medicamentos para o data lake
####. VERIFICAR
contagem_medicamento_residente = contagem_medic_por_residente[['ILPI', 'CPF', 'Qtde Medicamentos']]
contagem_medicamento_residente = (contagem_medicamento_residente
                                  .rename(columns={'ILPI': 'id_institution', 'CPF': 'cpf', 'Qtde Medicamentos': 'tot_medicin'})
)
# %%

####### VERIFICAR SE NECESSÁRIO
# Salva a tabela
contagem_medicamento_residente.to_csv('../../../../data/SMSAp/lake/QtdeMedicamentos.csv')