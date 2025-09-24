# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')

# %%
import pandas as pd

from utils.utils import criar_diretorios
from funcoes.f_plot import plot_config, salvar_tabela_como_imagem, plot_bar_flex_unificado
from funcoes.f_process import criar_diretorios

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
df = pd.read_csv("../../../../data/SMSAp/ILPI/base_perfil_epidemiologico.csv",
                 sep=";")
df.head()
# %%
## ------------------------
## ----- 12 - Estado de Saúde 
## ------------------------
# Cria um DataFrame para a estado_saude dos residentes
estado_saude = df[['id_institution', 'health_condition']]
estado_saude.head()
# %%
# Filtra apenas as linhas com estado_saude dos residentes
estado_saude = estado_saude[estado_saude['health_condition'].notna()].astype({'health_condition': 'int64'})
estado_saude.head()
# %%
# Cria a tabela Estado Saúde para data lake
estado_saude_residente = df[['id_institution', 'uuidv5', 'health_condition']]
estado_saude_residente = (estado_saude_residente[estado_saude_residente['health_condition']
                                                 .notna()]
                                                 .astype({'health_condition': 'int64'})
)
# %%
##### VERIFICAR NECESSIDADE
# Salva tabela
estado_saude_residente.to_csv('../../../../data/SMSAp/Lake/EstadoSaude.csv')
# %%
# Agrupa por 'health_condition, usa .size() para contar quantas vezes cada estado_saude aparece e
# renomeia a coluna de contagem para 'total'
estado_saude_grouped = estado_saude.groupby('health_condition').size().reset_index(name='total')
estado_saude_grouped.head()
# %%
# Calcula proporção dentro de cada instituição com .transform()
# Para cada grupo (cada institution_name), ele calcula a soma dos valores na coluna total.
# mas ao invés de reduzir o grupo a um único valor (como o .sum() padrão faria), ele replica 
# esse valor para cada linha do grupo.
estado_saude_grouped['proporcao'] = estado_saude_grouped['total'] / estado_saude_grouped['total'].sum()
estado_saude_grouped['proporcao'] = (estado_saude_grouped['proporcao']).round(2)
estado_saude_grouped
# %%
# Define um dicionário para mapear os códigos de estado_saude para strings
estado_saude_grouped['health_condition'] = estado_saude_grouped['health_condition'].replace({ 
    1 : 'ótimo',
    2 : 'bom',
    3 : 'regular',
    4 : 'ruim ou péssimo',
})
estado_saude_grouped.rename(columns={'health_condition' : 'estado_saude'}, inplace=True)
estado_saude_grouped
# %%
salvar_tabela_como_imagem(
    estado_saude_grouped,
    '../tables/12_tabela_estado_saude_geral.png',
    largura_max_coluna=25,
                          )

# %%

plot_bar_flex_unificado(
    estado_saude_grouped,
    title='Frequência de Estado de Saúde do Residente',
    xlabel='',ylabel='Número de Residentes',
    filename='../plots/12_grafico_estado_saude_residentes.png',
    orientation='v', 
    value_format='absolute',
    col_valor='total',
    col_categoria='estado_saude',
    show_values=True,
    show_text=False
)
# %%
# Agrupa por 'health_condition', usa .size() para contar quantas vezes cada 'health_condition' aparece e
# renomeia a coluna de contagem para 'total'
estado_saude_instit = estado_saude.groupby(['id_institution', 'health_condition']).size().reset_index(name='total')
estado_saude_instit
# %%
# Calcula a proporção de cada health_condition para cada ILPI
estado_saude_instit['proporcao'] = estado_saude_instit['total'] / estado_saude_instit.groupby('id_institution')['total'].transform('sum')
estado_saude_instit['proporcao'] = estado_saude_instit['proporcao'].round(2)
estado_saude_instit
# %%
# Define um dicionário para mapear os códigos de estado_saude para strings
estado_saude_instit['health_condition'] = estado_saude_instit['health_condition'].replace({ 
    1 : 'ótimo',
    2 : 'bom',
    3 : 'regular',
    4 : 'ruim ou péssimo',
})
estado_saude_instit.rename(columns={'id_institution':'ILPI', 'health_condition' : 'estado_saude'}, inplace=True)
estado_saude_instit
# %%
# Salva a tabela de Estado de Saúde por ILPI
salvar_tabela_como_imagem(
    estado_saude_instit,
    '../tables/12_tabela_estado_saude_por_ILPI.png',
    largura_max_coluna=25,
)
# %%
# Gráfico Estado de Saúdes por ILPI percentagem
plot_bar_flex_unificado(
    estado_saude_instit,
    title='Frequência do Estado de Saúde dos Residentes por ILPI',
    xlabel='', ylabel='Número de residentes',
    filename='../plots/12_grafico_estado_saude_por_ILPI_percent.png',
    orientation='v',
    value_format='percent',
    show_values=True,
    show_text=False,
    col_categoria='ILPI',
    col_valor='total',
)
# %%
