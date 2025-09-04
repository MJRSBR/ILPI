
# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')

# %%
import os
import re
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import textwrap # serve para formatar textos, ajustando-os para caber em uma largura específica, com a possibilidade de quebrar linhas e aplicar recuo.
from matplotlib.ticker import MaxNLocator

from funcoes.f_plot import salvar_tabela_como_imagem, plot_barh, plot_bar_flex_unificado, plot_percentual_por_ilpi
from funcoes.f_process import criar_diretorios, processa_multiresposta, extrair_morbidades, extrair_medicamentos, classificar_risco
# %%
# ---------------------
# Leitura dos dados
# ---------------------
df = pd.read_csv("../../../../data/SMSAp/ILPI/base_perfil_epidemiologico.csv",
                 sep=";")
df.head()

# %%
# --------------------
# Configurações Globais dos Gráficos
# ---------------------
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

pd.set_option('display.max_rows', None) #para mostrar todas as linhas. 

# Ajustar a exibição do pandas para mostrar mais caracteres
pd.set_option('display.max_colwidth', None)  # Permite exibir a coluna inteira


# ------------------------------
# Funções utilitárias
# ------------------------------

#def criar_diretorios():
#    os.makedirs('../tables', exist_ok=True)
#    os.makedirs('../plots', exist_ok=True)

# Cria diretórios para plots e tabelas
criar_diretorios()

# usando matplotlib
matplotlib.rc('font', size=10)


# %%
## ---------------------
## Análises e Gráficos
## ---------------------

## --------------------
## ---- 1 - Gênero
## -------------------

## Filtra os valores válidos (1 = Masculino, 2 = Feminino)
df_filtered = df[df['sex'].isin([1, 2])].copy()

# Mapeia os valores de sexo para strings
df_filtered['sex'] = df_filtered['sex'].map({1: 'Masculino', 2: 'Feminino'})

# Agrupa por institution_name e sexo e reorganiza com unstack
gender = df_filtered.groupby(['institution_name', 'sex']).size().unstack(fill_value=0).reset_index()

# Remove o nome do eixo de colunas
gender.columns.name = None
gender

# %%
# Calcula a porcentagem de cada sexo por instituição
gender_prop = (round(gender[['Feminino', 'Masculino']]
                        .div(gender[['Feminino', 'Masculino']]
                        .sum(axis=1), axis=0), 2))

# Adiciona a coluna de nome da instituição
gender_prop.insert(0, 'institution_name', gender['institution_name'])
gender_prop = gender_prop.rename(columns={'Feminino':'Feminino(prop)', 'Masculino':'Masculino(prop)'})
gender_prop
# %%
# Agrupando as tabelas
gender_join = gender.merge(gender_prop)
gender_join = gender_join[[
    'institution_name', 
    'Feminino', 'Feminino(prop)', 
    'Masculino', 'Feminino(prop)', 
    'Masculino(prop)']]
gender_join.rename(columns={'institution_name':'ILPI'}, inplace=True)
gender_join
# %%
# Salvando como imagem
salvar_tabela_como_imagem(
    gender_join,
    '../tables/01_tabela_genero_abs_prop.png',
    largura_max_coluna=15
)
 
# %%
# Gráfico 01 -- Gênero dos Residentes da ILPI

# Pivot da tabela para formato wide (um DataFrame por faixa etária por ILPI)
#pivot_df = gender_prop.pivot(index='institution_name', columns=['Feminimo', 'Masculino'])

plot_barh(gender.set_index('institution_name'), 
          title='Gênero dos Residentes da ILPI', 
          xlabel='Número de residentes', ylabel='ILPIs',
          filename='../plots/01_grafico_genero_perc.png',
          obs=2,
          show_text=True,
          show_values=True)

# %%

## --------------------
## ---- 2 - Idade 
## --------------------

# Cria um DataFrame para a idade dos residentes
df_idade = df[['institution_name', 'elder_age']]

# Filtra apenas as linhas com idade dos residentes
df_idade = df_idade[df_idade['elder_age'].notna()].astype({'elder_age': 'int64'})
df_idade.head()
# %%
# Criando tabela de residentes para data lake
residentes_ILPI = df[['institution_name', 'record_id', 'cpf', 'full_name', 'date_of_birth', 'elder_age', 'sex', 'race']]
residentes_ILPI = residentes_ILPI[residentes_ILPI['elder_age'].notna()].astype({'elder_age': 'int64'})

# Salvando tabela residentes_ILPI
residentes_ILPI.to_csv('../../../../data/SMSAp/lake/Residente.csv')
# %%
## ----- Plotando a idade dos residentes com linha de média
# Calcula a média geral
media_idade = df_idade['elder_age'].mean().__round__(1)
media_idade
# %%
# Cria um eixo X com base no índice dos residentes
x = range(len(df_idade))

# Plot
plt.figure(figsize=(12, 6))

# Pontos individuais
plt.scatter(x, df_idade['elder_age'], color='gray', alpha=0.6, label='Residentes')

# Linha de média
plt.axhline(y=media_idade, color='red', linestyle='--', linewidth=1.5, label=f'Média: {media_idade:.1f}')

# Eixos
plt.xlabel('Residentes')
plt.ylabel('Idade')
plt.title('Idade dos Residentes - Linha Média')

# Legenda
plt.legend()

# Layout e salvamento
plt.tight_layout()
plt.savefig('../plots/02_grafico_idades_residentes_com_media.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico de Idade dos Residentes salvo como imagem.")
plt.show()
# %%
## --------------------
## ---- Idade por ILPI
## -------------------

# Agrupa por ILPI e calcula a média de idade dos residentes

# Calcula a média por ILPI
media_idade = df_idade.groupby('institution_name')['elder_age'].mean().reset_index()
media_idade.columns = ['institution_name', 'Média']

# Define ILPIs únicos e ordenados (para o eixo X)
ilpis = sorted(df_idade['institution_name'].unique())

# Plot
plt.figure(figsize=(12, 6))

# Pontos individuais
plt.scatter(df_idade['institution_name'], df_idade['elder_age'], color='gray', alpha=0.6, label='Residentes')

# Médias por ILPI em vermelho
plt.scatter(media_idade['institution_name'], media_idade['Média'], color='red', s=100, marker='D', label='Média por ILPI')

# Eixos e rótulos
plt.xlabel('ILPI')
plt.ylabel('Idade dos Residentes')
plt.title('Idade dos Residentes por ILPI com Média Destacada')

# Definir o eixo X com os valores inteiros das ILPIs
plt.xticks(ilpis)

# Legenda, layout e salvamento
plt.legend()
plt.tight_layout()
plt.savefig('../plots/02_grafico_idades_residentes_por_ilpi.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico de Idade dos Residentes por ILPI salvo como imagem.")
plt.show()

# %%
## --------------------
## ---- Faixa Etária por ILPI
## -------------------

# Agrupa por institution_name e idade, contando os residentes
idade = df_idade['elder_age'].value_counts().reset_index()
idade.head()
# %%
# Define os intervalos de idade para as categorias

elder_age_bins = {
    '61 a 65 anos': (60, 65),
    '66 a 70 anos': (65, 70),
    '71 a 75 anos': (70, 75),
    '76 a 80 anos': (75, 80),
    '81 a 85 anos': (80, 85),
    '86 a 90 anos': (85, 90),
    '91 a 95 anos': (90, 95),
    '96 a 100 anos': (95, 100)       
}

# Gera a lista de bins e labels
bins = [60] + [v[1] for v in elder_age_bins.values()]
labels = list(elder_age_bins.keys())

# Cópia do data frame para criar novo data frame
idade_count = df_idade.copy()

# Cria a coluna de faixa etária
idade_count['elder_age_bin'] = pd.cut(idade_count['elder_age'],bins=bins,labels=labels,right=False)

# Deleta a coluna 'elder_age' original
idade_count = idade_count.drop(columns=['elder_age'])

# Filtra apenas as linhas com faixa etária atribuída (i.e., que não são NaN) e
# Exibe a contagem de residentes por faixa etária
idade_count = idade_count[idade_count['elder_age_bin'].notna()].value_counts().sort_index()
idade_count

# %%
# Cria um DataFrame a partir da série de contagem
idade_count = idade_count.reset_index()
idade_count
# %%
# Renomeia as colunas
idade_count = idade_count.rename(columns={'institution_name': 'ILPI', 'elder_age_bin': 'Faixa Etária', 'count': 'Número de Residentes'}) 
idade_count

# %%
# Salvando a tabela de idades
salvar_tabela_como_imagem(
    idade_count,
    '../tables/02_tabela_idade.png',
    largura_max_coluna=25
)
# %%

# Pivot da tabela para formato wide (um DataFrame por faixa etária por ILPI)
pivot_df = idade_count.pivot(index='ILPI', columns='Faixa Etária', values='Número de Residentes')

plot_percentual_por_ilpi(
    pivot_df,
    '../plots/02_grafico_faixa_etaria_por_ilpi.png',
    title='Distribuíção por Faixa Etária dos Residentes por ILPI (% por ILPI)',
    legend_title='Faixa Etária',
    )
# %%
## --------------------
## ---- 3 - Raça e Cor
## -------------------

# Cria um DataFrame para a raça dos residentes
df_raca = df[['institution_name', 'race']]
df_raca.head()
# %%
# Filtra apenas as linhas com raça dos residentes       
df_raca = df_raca[df_raca['race'].notna()].astype({'race': 'int64'})
df_raca.head()
# %%
# Agrupa por 'race', usa .size() para contar quantas vezes cada raça aparece e
# renomeia a coluna de contagem para 'total'
df_raca_grouped = df_raca.groupby('race').size().reset_index(name='total')
df_raca_grouped
# %%
# Calcula proporção de cada raça
df_raca_grouped['proporcao'] = df_raca_grouped['total'] / df_raca_grouped['total'].sum()
df_raca_grouped['proporcao'] = (df_raca_grouped['proporcao']).round(2)
df_raca_grouped
# %%
# Define um dicionário para mapear os códigos de raça para strings
df_raca_grouped['race'] = df_raca_grouped['race'].replace({ 
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena',
    6: 'Não Informado',
})

df_raca_grouped.rename(columns={'race': 'Raça/Cor'}, inplace=True) 
df_raca_grouped

# %%
# Salvando a tabela de raça 
# A tabela df_raca_grouped contém a proporção de raça geral
salvar_tabela_como_imagem(
    df_raca_grouped,
    '../tables/03_tabela_raca_geral.png', 
    largura_max_coluna=25,
)                             
# %%

plot_bar_flex_unificado(
    df_raca_grouped,
    title='Distribuíção por Raça/Cor dos Residentes',
    xlabel='Raça/Cor', ylabel='Número de residentes',
    filename='../plots/03_grafico_raca_geral.png',
    show_values=True,
    show_text=False,
    value_format='absolute',
    orientation='v',
    xtick_rotation=0,
    col_categoria='Raça/Cor',
    col_valor='total'

)

# %%
# Cria um DataFrame raça por ILPI
df_raca_inst = df_raca.groupby(['institution_name', 'race']).size().reset_index(name='total')
df_raca_inst
# %%
# Calcula proporção dentro de cada instituição com .transform()
# Para cada grupo (cada institution_name), ele calcula a soma dos valores na coluna total.
# mas ao invés de reduzir o grupo a um único valor (como o .sum() padrão faria), ele replica 
# esse valor para cada linha do grupo.
df_raca_inst['proporcao'] = df_raca_inst['total'] / df_raca_inst.groupby('institution_name')['total'].transform('sum')
df_raca_inst['proporcao'] = (df_raca_inst['proporcao']).round(2)
df_raca_inst        
# %%
# Define um dicionário para mapear os códigos de raça para strings por ILPI
df_raca_inst['race'] = df_raca_inst['race'].replace({ 
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena',
    6: 'Não sabe',
})

df_raca_inst.rename(columns={'institution_name':'ILPI', 'race':'Raça/Cor'}, inplace=True)
df_raca_inst
# %%
# Salvando a tabela de raça 
# A tabela df_raca_grouped contém a proporção de raça geral
salvar_tabela_como_imagem(
    df_raca_inst,
    '../tables/03_tabela_raca_por_ILPI.png', 
    largura_max_coluna=25,
)                             

# %%
# Gráfico residentes por ILPI percentual
plot_bar_flex_unificado(
    df_raca_inst,
    col_categoria='ILPI',
    col_valor='total',
    col_grupo='Raça/Cor',
    value_format='percent',  # Texto em %
    orientation='v',
    title='Distribuição por Raça/Cor dos Residentes por ILPI',
    xlabel='ILPI',
    ylabel='Número de residentes',  # Eixo Y correto: absolutos
    filename='../plots/03_grafico_raca_por_ilpi_percentual.png',
    show_text=False
)

# %%
## --------------------
## ---- 4 - Escolaridade
## -------------------

# Cria um DataFrame para a escolaridade dos residentes
df_escolaridade = df[['institution_name', 'scholarship']]
df_escolaridade.head()
# %%
# Filtra apenas as linhas com escolaridade dos residentes
df_escolaridade = df_escolaridade[df_escolaridade['scholarship'].notna()].astype({'scholarship': 'int64'})
df_escolaridade.head()
# %%
# Agrupa por 'scholarshiphip, usa .size() para contar quantas vezes cada escolaridade aparece e
# renomeia a coluna de contagem para 'total'
df_escolaridade_grouped = df_escolaridade.groupby('scholarship').size().reset_index(name='total')
df_escolaridade_grouped.head()
# %%
# Calcula proporção dentro de cada instituição com .transform()
# Para cada grupo (cada institution_name), ele calcula a soma dos valores na coluna total.
# mas ao invés de reduzir o grupo a um único valor (como o .sum() padrão faria), ele replica 
# esse valor para cada linha do grupo.
df_escolaridade_grouped['proporcao'] = df_escolaridade_grouped['total'] / df_escolaridade_grouped['total'].sum()
df_escolaridade_grouped['proporcao'] = (df_escolaridade_grouped['proporcao']).round(2)
df_escolaridade_grouped
# %%
# Define um dicionário para mapear os códigos de escolaridade para strings
df_escolaridade_grouped['scholarship'] = df_escolaridade_grouped['scholarship'].replace({ 
    1: 'nenhuma',
    2: '1 a 3 anos',
    3: '4 a 7 anos',
    4: '8 anos ou mais',
    5: 'não há registro',
})
df_escolaridade_grouped.rename(columns={'scholarship': 'escolaridade'}, inplace=True)
df_escolaridade_grouped
# %%
salvar_tabela_como_imagem(
    df_escolaridade_grouped,
    '../tables/04_tabela_escolaridade_geral.png',
    largura_max_coluna=25,
                          )
# %%
plot_bar_flex_unificado(
    df_escolaridade_grouped,
    title='Escolaridade Geral dos Residentes',
    xlabel='Tempo de estudo', ylabel='Número de Residentes',
    filename='../plots/04_grafico_escolaridade_residente_por_ILPI.png',
    show_text=False,
    value_format='absolute',
    orientation='v',
    xtick_rotation=0,
    col_categoria='escolaridade',
    col_valor='total'

)
# %%
# Cria um Data Frame escolaridade por ILPI
df_escolar_inst = df_escolaridade.groupby(['institution_name', 'scholarship']).size().reset_index(name='total')
df_escolar_inst
# %%

# Calcula proporção de cada escolaridade
df_escolar_inst['proporcao'] = df_escolar_inst['total'] / df_escolar_inst.groupby('institution_name')['total'].transform('sum')
df_escolar_inst['proporcao'] = (df_escolar_inst['proporcao']).round(2)
df_escolar_inst
# %%
# Define um dicionário para mapear os códigos de escolaridade para strings
df_escolar_inst['scholarship'] = df_escolar_inst['scholarship'].replace({ 
    1: 'nenhuma',
    2: '1 a 3 anos',
    3: '4 a 7 anos',
    4: '8 anos ou mais',
    5: 'não há registro',
})

df_escolar_inst.rename(columns={'institution_name': 'ILPI', 'scholarship': 'escolaridade'}, inplace=True)
df_escolar_inst
# %%
salvar_tabela_como_imagem(
    df_escolar_inst,
     '../tables/04_tabela_escolaridade_por_ILPI.png',
    largura_max_coluna=25,
)
# %%
# Criando gráfico escolaridade por ILPI absoluto
plot_bar_flex_unificado(
    df_escolar_inst,
    title='Distribuíção por escolaridade por ILPI (absoluto e %)',
    xlabel='ILPI', ylabel='Número de residentes',
    filename='../plots/04_grafico_escolaridade_por_ILPI_absoluto.png',
    show_text=False,
    value_format='percent',
    orientation='v',
    xtick_rotation=0,
    col_categoria='ILPI',
    col_valor='total'

)
# %%

## --------------------
## ----- 5 - Tempo institucionalizado
## --------------------
# Estatística básica
df['institut_time_years'].describe()
# %%
# Acha os registros que provavelmente estejam errados
df.loc[df['institut_time_years'] > 30]
# %%
temp_instit = df[['institution_name', 'institut_time_years']]
temp_instit.head()
# %%
# Filtra apenas as linhas com tempo de institucionalização
temp_instit = temp_instit[temp_instit['institut_time_years'].notna()].astype({'institut_time_years':'int64'})
temp_instit.head()
# %%
# Cria tabela Tempo Institucionalizado
tempo_instit_residentes = df[['institution_name', 'cpf', 'institut_time_years']]
tempo_instit_residentes = (tempo_instit_residentes[tempo_instit_residentes['institut_time_years']
                                                   .notna()]
                                                   .astype({'institut_time_years': 'int64'}))
# Salva a tabela para uso no data lake
tempo_instit_residentes.to_csv('../../../../data/SMSAp/Lake/TempoInstituicao.csv')
# %%
# Agrupa por 'institut_time_years', usa .size() para contar quantas vezes cada escolaridade aparece e
# renomeia a coluna de contagem para 'total'
temp_instit_grouped = temp_instit.groupby('institut_time_years').size().reset_index(name='total')
temp_instit_grouped.head()
# %%
# Calcula proporcao de tempo de institucionalização
temp_instit_grouped['proporcao'] = temp_instit_grouped['total'] / temp_instit_grouped['total'].sum()
temp_instit_grouped['proporcao'] = temp_instit_grouped['proporcao'].round(2)
temp_instit_grouped.rename(columns={'institut_time_years': 'Tempo institucionalizado'}, inplace=True)
temp_instit_grouped
# %%
salvar_tabela_como_imagem(
    temp_instit_grouped,
    '../tables/05_tabela_tempo _institucionalização.png',
    largura_max_coluna=25,
)
# %%
# Criando gráfico escolaridade por ILPI absoluto
plot_bar_flex_unificado(
    temp_instit_grouped,
    title='Tempo (anos) de Institucionalização dos Residentes',
    xlabel='Tempo de instituíção', ylabel='Número de residentes',
    filename='../plots/05_grafico_tempo_instit.png',
    show_text=False,
    value_format='absolute',
    orientation='v',
    xtick_rotation=0,
    col_categoria='Tempo institucionalizado',
    col_valor='total'

)
# %%
# Criando faixas de tempo 
# Define os intervalos tempo instituíção para as categorias

inst_time_bins = {
    '0 a 5 anos': (0, 5),
    '6 a 10 anos': (5, 10),
    '11 a 15 anos': (10, 15),
    '16 a 20 anos': (15, 20),
    '21 a 25 anos': (20, 25),
    '26 a 30 anos': (25, 30),
    'mais de 31 anos': (30, 50)       
}

# Gera a lista de bins e labels
bins = [0] + [v[1] for v in inst_time_bins.values()]
labels = list(inst_time_bins.keys())

# Garante que estamos trabalhando com uma cópia
temp_instit = temp_instit.copy()

# Cria a coluna de faixa etária
temp_instit['inst_time_bin'] = pd.cut(temp_instit['institut_time_years'],bins=bins,labels=labels,right=False)

# Deleta a coluna 'institut_time_years' original
temp_instit = temp_instit.drop(columns=['institut_time_years'])

# Filtra apenas as linhas com faixa etária atribuída (i.e., que não são NaN) e
# Exibe a contagem de residentes por faixa etária
temp_instit = temp_instit[temp_instit['inst_time_bin'].notna()].value_counts().sort_index()
temp_instit

# %%
# Cria um DataFrame a partir da série de contagem
temp_instit = temp_instit.reset_index()
temp_instit
# %%
# Renomeia as colunas
temp_instit = temp_instit.rename(columns={'institution_name': 'ILPI', 'inst_time_bin': 'Faixa Tempo Instituíção', 'count': 'Número de Residentes'}) 
temp_instit
# %%
# Salvando a tabela de idades
salvar_tabela_como_imagem(
    temp_instit,
    '../tables/05_tabela_faixa_tempo_institucionalização.png',
    largura_max_coluna=25
)

# %%
# Configura o tamanho do gráfico
plot_bar_flex_unificado(temp_instit,
                        #col_categoria='Faixa Tempo Instituíção',
                        col_valor='Número de Residentes',
                        col_grupo='Faixa Tempo Instituíção',
                        title='Tempo de Institucionalização dos Residentes por ILPI',
                        xlabel='Tempo de instituíção', ylabel='Número de residentes',
                        filename='../plots/05_grafico_tempo_instit_por_ILPI.png',
                        orientation='v',
                        value_format='absolute',
                        show_values=True,
                        show_text=False
)
# %%
# Criando gráfico tempo institucionalização por ILPI absoluto
plot_bar_flex_unificado(temp_instit,
                        #col_categoria='Faixa Tempo Instituíção',
                        col_valor='Número de Residentes',
                        col_grupo='Faixa Tempo Instituíção',
                        title='Tempo de Institucionalização Percentual dos Residentes por ILPI ',
                        xlabel='Tempo de instituíção', ylabel='Número de residentes',
                        filename='../plots/05_grafico_proporcao_tempo_instit_por_ILPI.png',
                        orientation='v',
                        value_format='percent',
                        show_values=True,
                        show_text=False
)

# %%
## --------------------
## ----- 6 - Suporte Familiar
## --------------------

# Cria um DF com suporte familiar
suporte = df[['institution_name', 'family_support']]
suporte.head(20)
# %%
# Filtra apenas as linhas que existam dados de suporte familiar
suporte_gruped = suporte[suporte['family_support'].notna()].astype({'family_support':'int64'})
suporte_gruped.head(20)
# %%
# Cria tabela Suporte Familiar para data lake
suporte_familiar_residente = df[['institution_name', 'cpf', 'family_support']]
suporte_familiar_residente = (suporte_familiar_residente[suporte_familiar_residente['family_support']
                                                         .notna()]
                                                         .astype({'family_support': 'int64'})
)

# Salva a tabela para data lake
suporte_familiar_residente.to_csv('../../../../data/SMSAp/lake/SuporteFamiliar.csv')

# %%
# Agrupa por 'family_support', usa .size() para contar quantas vezes cada suporte aparece e
# renomeia a coluna de contagem para 'total'
suporte_gruped = suporte.groupby('family_support').size().reset_index(name='total')
suporte_gruped
# %%
# Calcula proporção de cada raça
suporte_gruped['proporcao'] = suporte_gruped['total'] / suporte_gruped['total'].sum()
suporte_gruped['proporcao'] = (suporte_gruped['proporcao']).round(2)
suporte_gruped
# %%
# Define um dicionário para mapear os códigos de raça para strings
suporte_gruped['family_support'] = suporte_gruped['family_support'].replace({ 
    1: 'Sim',
    2: 'Não',
    3: 'Não consta no prontuário',
})

suporte_gruped.rename(columns={'family_support': 'suporte_familiar'}, inplace=True)
suporte_gruped
# %%
# Salva a tabela geral de suporte familiar
salvar_tabela_como_imagem(
    suporte_gruped,
    '../tables/06_tabela_suporte_famil_geral.png',
    largura_max_coluna=25,

)
# %%
# Gráfico Geral Suporte familiar absoluto
plot_bar_flex_unificado(
    suporte_gruped,
    title='Frequência do Suporte Familiar dos Residentes',
    xlabel='', ylabel='Número de residentes',
    filename='../plots/06_grafico_suporte_familiar_absoluto.png',
    orientation='v',
    value_format='absolute',
    show_values=True,
    show_text=False,
    col_categoria='suporte_familiar',
    col_valor='total',
)
# %%
# Agrupa por 'institutuin_name' e 'family_support', usa .size() para contar quantas vezes cada suporte aparece e
# renomeia a coluna de contagem para 'total'
suporte_inst = suporte.groupby(['institution_name', 'family_support']).size().reset_index(name='total')
suporte_inst
# %%
# Calcula proporçao de cada suporte dentro de cada ILPI
suporte_inst['proporcao'] = suporte_inst['total'] / suporte_inst.groupby('institution_name')['total'].transform('sum')
suporte_inst['proporcao'] = (suporte_inst['proporcao']).round(2)
suporte_inst
# %%
# Define um dicionário para mapear os códigos de raça para strings
suporte_inst['family_support'] = suporte_inst['family_support'].replace({ 
    1: 'Sim',
    2: 'Não',
    3: 'Não consta no prontuário',
})

suporte_inst.rename(columns={'institution_name':'ILPI', 'family_support': 'Suporte Familiar'}, inplace=True)
suporte_inst
# %%
# Salvando a tabela de suporte familiar por ILPI
salvar_tabela_como_imagem(
    suporte_inst,
    '../tables/06_tabela_suporte_famil_por_ILPI.png',
    largura_max_coluna=25,
)
# %%
# Gráfico Suporte familiar por ILPI absoluto
plot_bar_flex_unificado(
    suporte_inst,
    title='Frequência do Suporte Familiar dos Residentes por ILPI',
    xlabel='', ylabel='Número de residentes',
    filename='../plots/06_grafico_suporte_familiar_por_ILPI.png',
    orientation='v',
    value_format='absolute',
    show_values=True,
    show_text=False,
    col_categoria='ILPI',
    col_valor='total',
)
# %%
# Gráfico Suporte familiar por ILPI percentagem
plot_bar_flex_unificado(
    suporte_inst,
    title='Frequência do Suporte Familiar dos Residentes por ILPI (%)',
    xlabel='', ylabel='Número de residentes',
    filename='../plots/06_grafico_suporte_familiar_por_ILPI_percent.png',
    orientation='v',
    value_format='percent',
    show_values=True,
    show_text=False,
    col_categoria='ILPI',
    col_valor='total',
)
# %%
## --------------------
## ----- 7 - Grau de dependência
## --------------------

# Cria um DF com grau_dependencia
grau_dependencia = df[['institution_name', 'dependence_degree']]
grau_dependencia.head(20)
# %%
# Filtra apenas as linhas que existam dados de grau_dependencia
grau_dependencia_gruped = grau_dependencia[grau_dependencia['dependence_degree'].notna()].astype({'dependence_degree':'int64'})
grau_dependencia_gruped.head(20)
# %%
# Cria tabela Grau Dependencia para o data lake

grau_dependencia_residente = df[['institution_name', 'cpf', 'dependence_degree']]
grau_dependencia_residente = (grau_dependencia_residente[grau_dependencia_residente['dependence_degree']
                                                         .notna()]
                                                         .astype({'dependence_degree': 'int64'})
)

# Salva a tabela
grau_dependencia_residente.to_csv('../../../../data/SMSAp/Lake/GrauDependencia.csv')

#%%
# Agrupa por 'dependence_degree', usa .size() para contar quantas vezes cada grau_dependencia aparece e
# renomeia a coluna de contagem para 'total'
grau_dependencia_gruped = grau_dependencia.groupby('dependence_degree').size().reset_index(name='total')
grau_dependencia_gruped
# %%
# Calcula proporção de cada grau de dependencia
grau_dependencia_gruped['proporcao'] = grau_dependencia_gruped['total'] / grau_dependencia_gruped['total'].sum()
grau_dependencia_gruped['proporcao'] = (grau_dependencia_gruped['proporcao']).round(2)
grau_dependencia_gruped
# %%
# Define um dicionário para mapear os códigos grau de dependencia para strings
grau_dependencia_gruped['dependence_degree'] = grau_dependencia_gruped['dependence_degree'].replace({ 
    1: 'Independente',
    2: 'Parcialmente dependente',
    3: 'Totalmente dependente',
})

grau_dependencia_gruped.rename(columns={'dependence_degree' : 'grau_dependencia'}, inplace=True)
grau_dependencia_gruped
# %%
# Salva a tabela geral de grau_dependencia 
salvar_tabela_como_imagem(
    grau_dependencia_gruped,
    '../tables/07_tabela_grau_dependencia_geral.png',
    largura_max_coluna=25,

)
# %%
# Gráfico Geral grau_dependencia absoluto
plot_bar_flex_unificado(
    grau_dependencia_gruped,
    title='Frequência do Grau de Dependência dos Residentes',
    xlabel='', ylabel='Número de residentes',
    filename='../plots/07_grafico_grau_dependencia_absoluto.png',
    orientation='v',
    value_format='absolute',
    show_values=True,
    show_text=False,
    col_categoria='grau_dependencia',
    col_valor='total',
)
# %%
# Agrupa por 'institutuin_name' e 'dependence_degree', usa .size() para contar quantas vezes cada suporte aparece e
# renomeia a coluna de contagem para 'total'
grau_dependencia_inst = grau_dependencia.groupby(['institution_name', 'dependence_degree']).size().reset_index(name='total')
grau_dependencia_inst
# %%
# Calcula proporçao de cada grau_dependencia dentro de cada ILPI
grau_dependencia_inst['proporcao'] = grau_dependencia_inst['total'] / grau_dependencia_inst.groupby('institution_name')['total'].transform('sum')
grau_dependencia_inst['proporcao'] = (grau_dependencia_inst['proporcao']).round(2)
grau_dependencia_inst
# %%
# Define um dicionário para mapear os códigos de raça para strings
grau_dependencia_inst['dependence_degree'] = grau_dependencia_inst['dependence_degree'].replace({ 
    1: 'Sim',
    2: 'Não',
    3: 'Não consta no prontuário',
})

grau_dependencia_inst.rename(columns={'institution_name':'ILPI', 'dependence_degree' : 'grau_dependencia'}, inplace=True)
grau_dependencia_inst
# %%
# Salvando a tabela de grau_dependencia familiar por ILPI
salvar_tabela_como_imagem(
    grau_dependencia_inst,
    '../tables/07_tabela_grau_dependencia_por_ILPI.png',
    largura_max_coluna=25,
)
# %%
# Gráfico grau_dependencia familiar por ILPI absoluto
plot_bar_flex_unificado(
    grau_dependencia_inst,
    title='Frequência do Grau de Dependência dos Residentes por ILPI',
    xlabel='', ylabel='Número de residentes',
    filename='../plots/07_grafico_grau_dependencia_por_ILPI.png',
    orientation='v',
    value_format='percent',
    show_values=True,
    show_text=False,
    col_categoria='ILPI',
    col_valor='total',
)
# %%
## --------------------
## ----- 8 - Tipo de Vínculo
## --------------------

# Define um dicionário para mapear os códigos tipos de vinculo para strings
vinculo_cols = { 
    'link_type___1': 'Privado',
    'link_type___2': 'Filantrópico',
    'link_type___3': 'Convênio com a Prefeitura',
}
# %%
# Cria um DF com vínculo com ILPI
vinculo_instit = processa_multiresposta(df, vinculo_cols, 'Vínculo com a ILPI')
vinculo_instit.head(20)
# %%
# Agrupa por 'link_type', usa .size() para contar quantas vezes cada vinculo_instit aparece e
# renomeia a coluna de contagem para 'total'
vinculo_instit_gruped = vinculo_instit.groupby('Vínculo com a ILPI').size().reset_index(name='total')
vinculo_instit_gruped.head()
# %%
# Calcula proporção de cada vinculo
vinculo_instit_gruped['proporcao'] = vinculo_instit_gruped['total'] / vinculo_instit_gruped['total'].sum()
vinculo_instit_gruped['proporcao'] = (vinculo_instit_gruped['proporcao']).round(2)
vinculo_instit_gruped
# %%
# Salva a tabela geral de vinculo_instit 
salvar_tabela_como_imagem(
    vinculo_instit_gruped,
    '../tables/08_tabela_vinculo_instit_geral.png',
    largura_max_coluna=25,

)
# %%
# Gráfico Geral tipo de vinculo absoluto
plot_bar_flex_unificado(
    vinculo_instit_gruped,
    title='Frequência do Vinculo dos Residentes',
    xlabel='Tipo de vínculo', ylabel='Número de residentes',
    filename='../plots/08_grafico_tipos_vinculo_absoluto.png',
    orientation='v',
    value_format='absolute',
    show_values=True,
    show_text=False,
    col_categoria='Vínculo com a ILPI',
    col_valor='total',
)
# %%
# Agrupa por 'institutuin_name' e 'link_type', usa .size() para contar quantas vezes cada suporte aparece e
# renomeia a coluna de contagem para 'total'
vinculo_inst = vinculo_instit.groupby(['ILPI', 'Vínculo com a ILPI']).size().reset_index(name='total')
vinculo_inst
# %%
# Calcula proporçao de cada vinculo dentro de cada ILPI
vinculo_inst['proporcao'] = vinculo_inst['total'] / vinculo_inst.groupby('ILPI')['total'].transform('sum')
vinculo_inst['proporcao'] = (vinculo_inst['proporcao']).round(2)
vinculo_inst
# %%
# Salvando a tabela de vinculo familiar por ILPI
salvar_tabela_como_imagem(
    vinculo_inst,
    '../tables/08_tabela_tipo_vinculo_por_ILPI.png',
    largura_max_coluna=25,
)
# %%
# Gráfico vinculo familiar por ILPI absoluto
plot_bar_flex_unificado(
    vinculo_inst,
    title='Frequência do Tipo de Vínculo dos Residentes com a ILPI',
    xlabel='', ylabel='Número de residentes',
    filename='../plots/08_grafico_tipo_vinculo_por_ILPI.png',
    orientation='v',
    value_format='absolute',
    show_values=True,
    show_text=False,
    col_categoria='ILPI',
    col_valor='total',
)
# %%
# Gráfico vinculo familiar por ILPI percentagem
plot_bar_flex_unificado(
    vinculo_inst,
    title='Frequência do vinculo Familiar dos Residentes por ILPI (%)',
    xlabel='', ylabel='Número de residentes',
    filename='../plots/08_grafico_tipo_vinculo_por_ILPI_percent.png',
    orientation='v',
    value_format='percent',
    show_values=True,
    show_text=False,
    col_categoria='ILPI',
    col_valor='total',
)
# %%
## --------------------
## ----- 9 - Fonte de Renda
## --------------------

# Cria um DF com fonte de renda 
fonte_renda = df[['institution_name', 'elder_income_source']]
fonte_renda.head(20)
# %%
# Filtra apenas as linhas que existam dados de fonte de renda 
fonte_renda_gruped = fonte_renda[fonte_renda['elder_income_source'].notna()].astype({'elder_income_source':'int64'})
fonte_renda_gruped.head(20)
#%%
# Agrupa por 'elder_income_source', usa .size() para contar quantas vezes cada fonte_renda_gruped aparece e
# renomeia a coluna de contagem para 'total'
fonte_renda_gruped = fonte_renda_gruped.groupby('elder_income_source').size().reset_index(name='total')
fonte_renda_gruped
# %%
# Calcula proporção de cada fonte de renda
fonte_renda_gruped['proporcao'] = fonte_renda_gruped['total'] / fonte_renda_gruped['total'].sum()
fonte_renda_gruped['proporcao'] = (fonte_renda_gruped['proporcao']).round(2)
fonte_renda_gruped
# %%
# Define um dicionário para mapear os códigos de fonte de renda para strings
fonte_renda_gruped['elder_income_source'] = fonte_renda_gruped['elder_income_source'].replace({ 
    1: 'Aposentadoria/pensão',
    2: 'Benefíco de Prestação',
    3: 'Bolsa Família',
    4: 'Nenhum',
    5: 'Não sabe'
})

fonte_renda_gruped.rename(columns={'elder_income_source' :  'fonte_renda_residente'}, inplace=True)
fonte_renda_gruped
# %%
# Salva a tabela geral de fonte_renda_gruped
salvar_tabela_como_imagem(
    fonte_renda_gruped,
    '../tables/09_tabela_fonte_renda_geral.png',
    largura_max_coluna=25,

)
# %%
# Gráfico Geral Fonte de Renda absoluto
plot_bar_flex_unificado(
    fonte_renda_gruped,
    title='Frequência Fonte de Renda dos Residentes',
    xlabel='', ylabel='Número de residentes',
    filename='../plots/09_grafico_fonte_renda_absoluto.png',
    orientation='v',
    value_format='absolute',
    show_values=True,
    show_text=False,
    col_categoria='fonte_renda_residente',
    col_valor='total',
)
# %%
# Agrupa por 'institutuin_name' e 'lelder_income_source', usa .size() para contar quantas vezes cada suporte aparece e
# renomeia a coluna de contagem para 'total'
fonte_renda_inst = fonte_renda.groupby(['institution_name', 'elder_income_source']).size().reset_index(name='total')
fonte_renda_inst
# %%
# Calcula proporçao de cada fonte_renda dentro de cada ILPI
fonte_renda_inst['proporcao'] = fonte_renda_inst['total'] / fonte_renda_inst.groupby('institution_name')['total'].transform('sum')
fonte_renda_inst['proporcao'] = (fonte_renda_inst['proporcao']).round(2)
fonte_renda_inst
# %%
# Define um dicionário para mapear os códigos de fonte de renda para strings
fonte_renda_inst['elder_income_source'] = fonte_renda_inst['elder_income_source'].replace({ 
    1: 'Aposentadoria/pensão',
    2: 'Benefíco de Prestação',
    3: 'Bolsa Família',
    4: 'Nenhum',
    5: 'Não sabe'
})

fonte_renda_inst.rename(columns={'elder_income_source' : 'fonte_renda_residente'}, inplace=True)
fonte_renda_inst
# %%
# Salvando a tabela de fonte_renda familiar por ILPI
salvar_tabela_como_imagem(
    fonte_renda_inst,
    '../tables/09_tabela_fonte_renda_por_ILPI.png',
    largura_max_coluna=25,
)
# %%
# Gráfico fonte_renda familiar por ILPI absoluto
plot_bar_flex_unificado(
    fonte_renda_inst,
    title='Frequência da Fonte de Renda dos Residentes por ILPI',
    xlabel='', ylabel='Número de residentes',
    filename='../plots/09_grafico_fonte_renda_por_ILPI.png',
    orientation='v',
    value_format='absolute',
    show_values=True,
    show_text=False,
    col_categoria='institution_name',
    col_valor='total',
)
# %%
# Gráfico fonte_renda familiar por ILPI percentagem
plot_bar_flex_unificado(
    fonte_renda_inst,
    title='Frequência da Fonte de Renda dos Residentes por ILPI',
    xlabel='', ylabel='Número de residentes',
    filename='../plots/09_grafico_fonte_renda_familiar_por_ILPI_percent.png',
    orientation='v',
    value_format='percent',
    show_values=True,
    show_text=False,
    col_categoria='institution_name',
    col_valor='total',
)
# %%
## --------------------
## ----- 10 - Medicamentos
## --------------------

# Criar um DF para registro de medicamentos

medic_registro = df[['institution_name', 'recorded']]
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
medic_registro_instit = medic_registro.groupby(['institution_name', 'recorded']).size().reset_index(name='total')
medic_registro_instit
# %%
# Calcula a proporção de cada recorded para cada ILPI
medic_registro_instit['proporcao'] = medic_registro_instit['total'] / medic_registro_instit.groupby('institution_name')['total'].transform('sum')
medic_registro_instit['proporcao'] = medic_registro_instit['proporcao'].round(2)
medic_registro_instit
# %%
# Mapeia a coluna recorded e atribui valor "sim e não"
medic_registro_instit['recorded'] = medic_registro_instit['recorded'].map({1: 'Sim', 0: 'Não'})
medic_registro_instit.rename(columns={'institution_name':'ILPI', 'recorded':'Registro medicamentos'}, inplace=True)
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
contagem_medic_por_residente = medic_por_residente.groupby(['ILPI','CPF','Nome Completo']).size().reset_index(name='Qtde Medicamentos')
contagem_medic_por_residente.head(20)
# %%
# Cria a tabela Contagem Medicamentos para o data lake

contagem_medicamento_residente = contagem_medic_por_residente[['ILPI', 'CPF', 'Qtde Medicamentos']]
contagem_medicamento_residente = (contagem_medicamento_residente
                                  .rename(columns={'ILPI': 'institution_name', 'CPF': 'cpf', 'Qtde Medicamentos': 'tot_medicin'})
)

# Salva a tabela
contagem_medicamento_residente.to_csv('../../../../data/SMSAp/lake/QtdeMedicamentos.csv')

# %%
## --------------------
## ----- 11 - Morbidades
## --------------------
# Definindo um dicionário para morbidades binárias
morb_dict = {
    "morbidities___1" : "Hipertensão Arterial",
    "morbidities___2" : "Diabetes Mellitus",
    "morbidities___3" : "Hipercolesterolemia",
    "morbidities___4" : "Doença na coluna",
    "morbidities___5" : "Insuficiência cardíaco",
    "morbidities___6" : "Infarto",
    "morbidities___7" : "Insuficiência renal",
    "morbidities___8" : "Câncer",
    "morbidities___9" : "Enfisema pulmonar",
    "morbidities___10":	"Asma",
    "morbidities___11":	"Bronquite",
    "morbidities___12":	"Transtorno Mental",
    "morbidities___13":	"Osteoporose",
    "morbidities___14":	"Artrite",
    "morbidities___15":	"Demência",
    "morbidities___16":	"Alzheimer",
    "morbidities___17":	"Parkinson",
    "morbidities___18":	"Etilismo",
    "morbidities___19":	"Tabagismo",
    "morbidities___20":	"Usuário de drogas",
}

# %%

########

def extrair_morbidades(df, morbidade_dict, nome_coluna_soma=None):
    """
    Filtra e retorna os dados de morbidades legíveis, agrupados por institution_name, full_name, cpf.
    A coluna 'other_morbidities' é normalizada (minúsculas, sem espaços),
    separando múltiplas entradas por vírgula, ponto e vírgula ou barra vertical.
    Soma final inclui morbidades binárias + textuais distintas.

    Parâmetros:
    - df: DataFrame.
    - morbidade_dict: dict, mapeamento de código -> texto.
    - nome_coluna_soma: str, nome da coluna soma (Se None, usa 'soma_morbidities').

    Retorna:
    - DataFrame com as morbidades processadas, incluindo:
      - 'Morbidades': lista de morbidades binárias e textuais.
      - 'other_morbidities': morbidades textuais normalizadas.
      - 'soma_morbidities': soma total de morbidades (binárias + textuais).
    """
    
    morbidities_cols = list(morbidade_dict.keys())
    campos_para_propagacao = ['institution_name', 'full_name', 'cpf', 'elder_age']  # Incluir 'elder_age'
    
    # Propaga os campos chave
    for campo in campos_para_propagacao:
        df[campo] = df[campo].ffill()

    # Inclui linhas que tenham morbidades binárias OU outras textuais
    df_filtrado = df[df[morbidities_cols].eq(1).any(axis=1) | df['other_morbidities'].notna()].copy()

    if nome_coluna_soma is None:
        nome_coluna_soma = 'soma_morbidities'

    # Soma das morbidades binárias
    df_filtrado['soma_binarias'] = df_filtrado[morbidities_cols].sum(axis=1, numeric_only=True)

    def nomes_morbidades(row):
        return ', '.join([morbidade_dict[col] for col in morbidities_cols if row.get(col) == 1])

    df_filtrado['Morbidades'] = df_filtrado.apply(nomes_morbidades, axis=1)

    # Padroniza a coluna 'other_morbidities' (primeira letra maiúscula)
    df_filtrado['other_morbidities'] = (
        df_filtrado['other_morbidities']
        .astype(str)  # Garante que todos os valores sejam strings
        .str.lower()  # Coloca em minúsculas
        .replace('nan', '')  # Remove 'nan' (caso existam valores inválidos)
        .str.strip()  # Remove espaços extras
        .str.capitalize()  # Coloca a primeira letra maiúscula
    )
    
    # Remove qualquer vírgula extra no início ou no final
    df_filtrado['other_morbidities'] = df_filtrado['other_morbidities'].str.lstrip(', ').str.rstrip(', ')

    # Função para contar morbidades textuais
    def contar_textuais(texto):
        if not texto:
            return 0
        
        # Substitui " e " (com espaços) por vírgula para separar corretamente as palavras
        texto = re.sub(r'\s+e\s+', ', ', texto)
        
        # Substitui ponto e vírgula por vírgula
        texto = texto.replace(';', ',')
        
        # Divide a string usando vírgula, ponto e vírgula ou barra vertical como separadores
        itens = re.split(r'[;,|]', texto)
        
        # Remove espaços extras e conta as palavras
        itens = [item.strip() for item in itens if item.strip()]
        
        return len(itens)

    # Aplica a função para contar as morbidades textuais
    df_filtrado['soma_other'] = df_filtrado['other_morbidities'].apply(contar_textuais)
    
    # Soma final das morbidades (binárias + textuais)
    df_filtrado[nome_coluna_soma] = df_filtrado['soma_binarias'] + df_filtrado['soma_other']
    
    # Converte para int64 para garantir que a coluna soma seja do tipo inteiro
    df_filtrado[nome_coluna_soma] = df_filtrado[nome_coluna_soma].fillna(0).astype('int64')

    # Limpa colunas auxiliares
    df_filtrado = df_filtrado.drop(columns=['soma_binarias', 'soma_other'])

    # Agrupamento
    df_resultado = df_filtrado.groupby(['institution_name', 'full_name', 'cpf'], as_index=False).agg({
        'Morbidades': lambda x: ', '.join(sorted(set(', '.join(x).split(', ')))),
        'other_morbidities': lambda x: ', '.join(sorted(set(filter(None, map(str.strip, x))))),
        nome_coluna_soma: 'sum',  # Usando a soma do campo 'soma_morbidities' customizado
        'elder_age': 'first'  # Garantir que 'elder_age' seja agregada
    })

    # Converte 'elder_age' para int64
    df_resultado['elder_age'] = df_resultado['elder_age'].fillna(0).astype('int64')

    # Ordena as colunas conforme solicitado
    df_resultado = df_resultado[['institution_name', 'full_name', 'elder_age', 'cpf', 'Morbidades', 'other_morbidities', nome_coluna_soma]]

    # Organiza as linhas
    df_resultado = df_resultado.sort_values(by=['institution_name', 'full_name', 'cpf'])

    return df_resultado





# Extraindo morbidades, outras morbidades e soma
df_morbidades = extrair_morbidades(df, morb_dict)

df_morbidades
# %%
# Cria a tabela Morbidade Residentes para data lake
morbidades_residentes = df_morbidades[['institution_name', 'cpf', 'Morbidades', 'other_morbidities', 'soma_morbidities']]

# Salva tabela
morbidades_residentes.to_csv('../../../../data/SMSAp/Lake/Morbidades.csv')

# %%
## ------------------------
## ----- 12 - Estado de Saúde 
## ------------------------
# Cria um DataFrame para a estado_saude dos residentes
estado_saude = df[['institution_name', 'health_condition']]
estado_saude.head()
# %%
# Filtra apenas as linhas com estado_saude dos residentes
estado_saude = estado_saude[estado_saude['health_condition'].notna()].astype({'health_condition': 'int64'})
estado_saude.head()
# %%
# Cria a tabela Estado Saúde para data lake
estado_saude_residente = df[['institution_name', 'cpf', 'health_condition']]
estado_saude_residente = (estado_saude_residente[estado_saude_residente['health_condition']
                                                 .notna()]
                                                 .astype({'health_condition': 'int64'})
)

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
estado_saude_instit = estado_saude.groupby(['institution_name', 'health_condition']).size().reset_index(name='total')
estado_saude_instit
# %%
# Calcula a proporção de cada health_condition para cada ILPI
estado_saude_instit['proporcao'] = estado_saude_instit['total'] / estado_saude_instit.groupby('institution_name')['total'].transform('sum')
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
estado_saude_instit.rename(columns={'institution_name':'ILPI', 'health_condition' : 'estado_saude'}, inplace=True)
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
## --------------------
##  - COMPONENTES DE FRAGILIDADE
## --------------------

fragilidade_dic = {
    'amount_weight_loss':'Perda de Peso',
    'elder_strenght':(lambda x: x == 2),
    'elder_hospitalized':(lambda x: x ==1),
    'elder_difficulties':(lambda x: x == 1),
    'elder_mobility':(lambda x: x == 2),
    'basic_activities_diffic':(lambda x: x ==1),
    'falls_number':(lambda x: x ==1)
}

#amount_weight_loss_dict ={1: "de 1 a 3 kg",2: "mais de 3 kg",}
#elder_strenght_dict = {1:"Sim",2:"Não"}	
#elder_hospitalized_dict = {1: "nenhuma", 2: "1 a 2 vezes", 3: "3 vezes", 4: "4 ou mais",}
#elder_difficulties_dict = {1:"nenhuma", 2: "alguma",3: "não consegue",}
#elder_mobility_dict = {1: "Sim",2: "Não"}	
#basic_activities_diffic_dict = 	{1:	"Sim",2: "Não"}	
#falls_number_dict = {1: " nenhuma", 2: "1 a 3 quedas", 3: "4 e mais",}

# %%

def extrair_comp_fragilidade(df, nome_coluna_soma='soma_fragilidades'):
    """
    Filtra e retorna os dados de componentes de fragilidade,
    agrupados por institution_name, full_name, cpf.

    Parâmetros:
    - df: DataFrame.
    - fragilidade_dict: dict, mapeamento de código -> texto.
    - nome_coluna_soma: str, nome da coluna soma (Se None, usa 'soma_morbidities').

    Retorna:
    - DataFrame com as morbidades processadas, incluindo:
      - 'Componentes de Fragilidade': lista de morbidades binárias e textuais.
      - 'soma_morbidities': soma total de morbidades (binárias + textuais).
    """
    
    # # Preenche valores ausentes nas colunas-chave com o valor anterior (forward fill)
    campos_para_propagacao = ['institution_name', 'full_name', 'cpf']
    for campo in campos_para_propagacao:
        if campo in df.columns:
            df[campo] = df[campo].ffill()

    # Cria colunas de fragilidade binárias com base na lógica de interpretação de cada item
    df['frag_dependence_degree'] = df['dependence_degree'].apply(lambda x: 1 if x >= 2 else 0)
    df['frag_amount_weight_loss'] = df['amount_weight_loss'].apply(lambda x: 1 if x == 2 else 0)
    df['frag_elder_strenght'] = df['elder_strenght'].apply(lambda x: 1 if x == 1 else 0)
    df['frag_elder_hospitalized'] = df['elder_hospitalized'].apply(lambda x: 1 if x >= 2 else 0)
    df['frag_elder_difficulties'] = df['elder_difficulties'].apply(lambda x: 1 if x >= 2 else 0)
    df['frag_elder_mobility'] = df['elder_mobility'].apply(lambda x: 1 if x == 1 else 0)
    df['frag_basic_activities_diffic'] = df['basic_activities_diffic'].apply(lambda x: 1 if x == 1 else 0)
    df['frag_falls_number'] = df['falls_number'].apply(lambda x: 1 if x >= 2 else 0)

    # Lista das colunas binárias de fragilidade
    frag_cols = [
        'frag_dependence_degree',
        'frag_amount_weight_loss',
        'frag_elder_strenght',
        'frag_elder_hospitalized',
        'frag_elder_difficulties',
        'frag_elder_mobility',
        'frag_basic_activities_diffic',
        'frag_falls_number'
    ]

    # Mapeia nomes legíveis dos componentes de fragilidade
    descricao_frag = {
        'frag_dependence_degree': 'Grau dependência 2 ou 3',
        'frag_amount_weight_loss': 'Perda de peso > 3kg',
        'frag_elder_strenght': 'Fraqueza percebida',
        'frag_elder_hospitalized': 'Internação recente',
        'frag_elder_difficulties': 'Dificuldade ou incapacidade para levantar',
        'frag_elder_mobility': 'Caminhada mais lenta',
        'frag_basic_activities_diffic': 'Dificuldades em atividades diárias',
        'frag_falls_number': 'Quedas frequentes'
    }


    # Soma o total de fragilidades identificadas por linha
    df['soma_frag'] = df[frag_cols].sum(axis=1)

    # Gera uma descrição textual dos componentes de fragilidade presentes em cada linha
    def listar_componentes(row):
        return ', '.join([descricao_frag[col] for col in frag_cols if row[col] == 1])
    # Aplica a função acima a cada linha do DataFrame
    df['Componentes de Fragilidade'] = df.apply(listar_componentes, axis=1)

    # Função remove espaços extras e divide corretamente, evitando vírgulas sobrando
    def agrupar_componentes(lista):
        componentes = set()  # cria um conjunto vazio
        for item in lista:
            # Divide a string por vírgula, remove espaços e ignora valores vazios
            partes = [s.strip() for s in item.split(',') if s.strip()]
            # adiciona cada pedaço no conjunto
            for parte in partes:
                componentes.add(parte) 
        # converte o conjunto para lista e junta numa string separada por vírgula
        return ', '.join(sorted(componentes))

    # Agrupa os dados por indivíduo e instituição e resume os componentes e a soma
    resultado = df.groupby(['institution_name', 'full_name', 'cpf'], as_index=False).agg({
        'Componentes de Fragilidade': agrupar_componentes,
        'soma_frag': 'sum'
    })

    # Renomeia a coluna de soma, se for fornecido um nome alternativo
    resultado = resultado.rename(columns={
        'soma_frag': nome_coluna_soma
    })

    # Ordena os resultados por instituição, nome e CPF
    resultado = resultado.sort_values(by=['institution_name', 'full_name', 'cpf'])

    return resultado

# %%

# Extrai os componentes de fragilidade dos residentes
comp_fragilidade = extrair_comp_fragilidade(df)
comp_fragilidade

# %%
# Fazendo o merge tabelas
# *****************.   PRECISA VERIFICAR AS TABELAS MERGE *************************
# Agrupar tabelas de interesse 

#df_score = df_morbidades(contagem_medic_por_residente, how='rigth')
# %%
df_score = df_morbidades.merge(comp_fragilidade, how='right')
df_score

# %%
#amount_weight_loss_dict ={1: "de 1 a 3 kg",2: "mais de 3 kg",}
#elder_strenght_dict = {1:"Sim",2:"Não"}	
#elder_hospitalized_dict = {1: "nenhuma", 2: "1 a 2 vezes", 3: "3 vezes", 4: "4 ou mais",}
#elder_difficulties_dict = {1:"nenhuma", 2: "alguma",3: "não consegue",}
#elder_mobility_dict = {1: "Sim",2: "Não"}	
#basic_activities_diffic_dict = 	{1:	"Sim",2: "Não"}	
#falls_number_dict = {1: " nenhuma", 2: "1 a 3 quedas", 3: "4 e mais",}

##*********************. EXEMPLO NECESSITA DEFINIR OS PARAMETROS  ************************
condicao_atencao = {
    'amount_weight_loss':(lambda x: x == 1),
    'elder_strenght':(lambda x: x == 2),
    'elder_hospitalized':(lambda x: x ==1),
    'elder_difficulties':(lambda x: x == 1),
    'elder_mobility':(lambda x: x == 2),
    'basic_activities_diffic':(lambda x: x ==1),
    'falls_number':(lambda x: x ==1)
}

condicao_alerta = {
    'amount_weight_loss':(lambda x: x == 1),
    'elder_strenght':(lambda x: x == 1),
    'elder_hospitalized':(lambda x: x in [2, 3] ),
    'elder_difficulties':(lambda x: x == 2),
    'elder_mobility':(lambda x: x == 1),
    'basic_activities_diffic':(lambda x: x == 1),
    'falls_number':(lambda x: x == 2)
}

condicao_critica = {
    'amount_weight_loss':(lambda x: x == 2),
    'elder_strenght':(lambda x: x == 1),
    'elder_hospitalized':(lambda x: x in [3, 4]),
    'elder_difficulties':(lambda x: x == 1),
    'elder_mobility':(lambda x: x == 1),
    'basic_activities_diffic':(lambda x: x ==1),
    'falls_number':(lambda x: x == 3)
}

# %%


# %%

#condicao_atencao = {
#    'elder_age': (lambda x: x < 70),
#    'soma_morbidities': (lambda x: x <= 3),
#    'soma_fragilidades': (lambda x: x in [2, 3]),
#
#}
#
#condicao_alerta = {
#    'elder_age': (lambda x: x > 70 & x < 80),
#    'soma_morbidities': (lambda x: x in [4, 5] ),
#    'soma_fragilidades': (lambda x: x in [3, 4]),
#    
#}
#
#condicao_critica = {
#    'elder_age': (lambda x: x >= 81),
#    'soma_morbidities': (lambda x: x >= 6),
#    'soma_fragilidades': (lambda x: x>= 4),
#    
#}

# %%
resultado, resumo = classificar_risco(df, condicao_critica, condicao_alerta, condicao_atencao)

# %%
from IPython.display import display, HTML

# Exibe o resultado com cores
display(HTML(resultado.to_html(escape=False)))

# Mostra o resumo correto
display(HTML(resumo.to_html(escape=False)))

# %%
salvar_tabela_como_imagem(
    resumo,
    '../tables/13_tabela_resumo_score_fragilidade.png',
    titulo='Score de Fragilidade do Residente por ILPI',
    largura_max_coluna=25
)
# %%
df.head()
# %%


