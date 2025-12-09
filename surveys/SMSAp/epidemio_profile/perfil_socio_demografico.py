# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')

# %%

import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

from utils.utils import criar_diretorios
from funcoes.f_plot import plot_config, salvar_tabela_como_imagem, plot_barh, plot_bar_flex_unificado, plot_percentual_por_ilpi
from funcoes.f_process import processa_multiresposta

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
gender = df_filtered.groupby(['id_institution', 'sex']).size().unstack(fill_value=0).reset_index()

# Remove o nome do eixo de colunas
gender.columns.name = None
gender
# %%
# Calcula a porcentagem de cada sexo por instituição
gender_prop = (round(gender[['Feminino', 'Masculino']]
                        .div(gender[['Feminino', 'Masculino']]
                        .sum(axis=1), axis=0), 2))

# Adiciona a coluna de nome da instituição
gender_prop.insert(0, 'id_institution', gender['id_institution'])
gender_prop = gender_prop.rename(columns={'Feminino':'Feminino(prop)', 'Masculino':'Masculino(prop)'})
gender_prop
# %%
# Agrupando as tabelas
gender_join = gender.merge(gender_prop)
gender_join = gender_join[[
    'id_institution', 
    'Feminino', 'Feminino(prop)', 
    'Masculino', 'Feminino(prop)', 
    'Masculino(prop)']]
gender_join.rename(columns={'id_institution':'ILPI'}, inplace=True)
gender_join
# %%
# Salvando como imagem
salvar_tabela_como_imagem(
    gender_join,
    '../tables/01_tabela_genero_abs_prop.png',
    largura_max_coluna=15
)
print("✅ Tabela Proporção Gênero salva com sucesso!")
 
# %%
# Gráfico 01 -- Gênero dos Residentes da ILPI

plot_barh(gender.set_index('id_institution'), 
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
df_idade = df[['id_institution', 'elder_age']]

# Filtra apenas as linhas com idade dos residentes
df_idade = df_idade[df_idade['elder_age'].notna()].astype({'elder_age': 'int64'})
df_idade.head()

# %%

df_idade_60_mais = df_idade[df_idade['elder_age']>=60].reset_index()
df_idade_60_mais
# %%
df_idade_60_menos = df_idade[df_idade['elder_age']<=60].reset_index()
df_idade_60_menos

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
    '51 a 55 anos': (50, 55),
    '56 a 60 anos': (55, 60),
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
bins = [50] + [v[1] for v in elder_age_bins.values()]
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
idade_count = idade_count.rename(columns={'id_institution': 'ILPI', 'elder_age_bin': 'Faixa Etária', 'count': 'Número de Residentes'}) 
idade_count

# %%
# Salvando a tabela de idades
salvar_tabela_como_imagem(
    idade_count,
    '../tables/02_tabela_faixa_idade.png',

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
df_raca = df[['id_institution', 'race']]
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
df_raca_inst = df_raca.groupby(['id_institution', 'race']).size().reset_index(name='total')
df_raca_inst
# %%
# Calcula proporção dentro de cada instituição com .transform()
# Para cada grupo (cada id_institution), ele calcula a soma dos valores na coluna total.
# mas ao invés de reduzir o grupo a um único valor (como o .sum() padrão faria), ele replica 
# esse valor para cada linha do grupo.
df_raca_inst['proporcao'] = df_raca_inst['total'] / df_raca_inst.groupby('id_institution')['total'].transform('sum')
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

df_raca_inst.rename(columns={'id_institution':'ILPI', 'race':'Raça/Cor'}, inplace=True)
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
df_escolaridade = df[['id_institution', 'education']]
df_escolaridade.head()
# %%
# Filtra apenas as linhas com escolaridade dos residentes
df_escolaridade = df_escolaridade[df_escolaridade['education'].notna()].astype({'education': 'int64'})
df_escolaridade.head()
# %%
# Agrupa por 'education', usa .size() para contar quantas vezes cada escolaridade aparece e
# renomeia a coluna de contagem para 'total'
df_escolaridade_grouped = df_escolaridade.groupby('education').size().reset_index(name='total')
df_escolaridade_grouped.head()
# %%
# Calcula proporção dentro de cada instituição com .transform()
# Para cada grupo (cada id_institution), ele calcula a soma dos valores na coluna total.
# mas ao invés de reduzir o grupo a um único valor (como o .sum() padrão faria), ele replica 
# esse valor para cada linha do grupo.
df_escolaridade_grouped['proporcao'] = df_escolaridade_grouped['total'] / df_escolaridade_grouped['total'].sum()
df_escolaridade_grouped['proporcao'] = (df_escolaridade_grouped['proporcao']).round(2)
df_escolaridade_grouped
# %%
# Define um dicionário para mapear os códigos de escolaridade para strings
df_escolaridade_grouped['education'] = df_escolaridade_grouped['education'].replace({ 
    1: 'nenhuma',
    2: '1 a 3 anos',
    3: '4 a 7 anos',
    4: '8 anos ou mais',
    5: 'não há registro',
})
df_escolaridade_grouped.rename(columns={'education': 'escolaridade'}, inplace=True)
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
df_escolar_inst = df_escolaridade.groupby(['id_institution', 'education']).size().reset_index(name='total')
df_escolar_inst
# %%

# Calcula proporção de cada escolaridade
df_escolar_inst['proporcao'] = df_escolar_inst['total'] / df_escolar_inst.groupby('id_institution')['total'].transform('sum')
df_escolar_inst['proporcao'] = (df_escolar_inst['proporcao']).round(2)
df_escolar_inst
# %%
# Define um dicionário para mapear os códigos de escolaridade para strings
df_escolar_inst['education'] = df_escolar_inst['education'].replace({ 
    1: 'nenhuma',
    2: '1 a 3 anos',
    3: '4 a 7 anos',
    4: '8 anos ou mais',
    5: 'não há registro',
})

df_escolar_inst.rename(columns={'id_institution': 'ILPI', 'education': 'escolaridade'}, inplace=True)
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
temp_instit = df[['id_institution', 'institut_time_years']]
temp_instit.head()
# %%
# Filtra apenas as linhas com tempo de institucionalização
temp_instit = temp_instit[temp_instit['institut_time_years'].notna()].astype({'institut_time_years':'int64'})
temp_instit.head()
# %%
# Cria tabela Tempo Institucionalizado
tempo_instit_residentes = df[['id_institution', 'uuidv5', 'institut_time_years']]
tempo_instit_residentes = (tempo_instit_residentes[tempo_instit_residentes['institut_time_years']
                                                   .notna()]
                                                   .astype({'institut_time_years': 'int64'}))
# Salva a tabela para uso no data lake
##CHECAR SE É NECESSÁRIO
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
    '../tables/05_tabela_tempo_institucionalização_GERAL.png',
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
temp_instit = temp_instit.rename(columns={'id_institution': 'ILPI', 'inst_time_bin': 'Faixa Tempo Instituíção', 'count': 'Número de Residentes'}) 
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
                        filename='../plots/05_grafico_faixa_tempo_instit_por_ILPI.png',
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
suporte = df[['id_institution', 'family_support']]
suporte.head(20)
# %%
# Filtra apenas as linhas que existam dados de suporte familiar
suporte_gruped = suporte[suporte['family_support'].notna()].astype({'family_support':'int64'})
suporte_gruped.head(20)
# %%
# Cria tabela Suporte Familiar para data lake
suporte_familiar_residente = df[['id_institution', 'uuidv5', 'family_support']]
suporte_familiar_residente = (suporte_familiar_residente[suporte_familiar_residente['family_support']
                                                         .notna()]
                                                         .astype({'family_support': 'int64'})
)

# Salva a tabela para data lake
#suporte_familiar_residente.to_csv('../../../../data/SMSAp/lake/SuporteFamiliar.csv')

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
suporte_inst = suporte.groupby(['id_institution', 'family_support']).size().reset_index(name='total')
suporte_inst
# %%
# Calcula proporçao de cada suporte dentro de cada ILPI
suporte_inst['proporcao'] = suporte_inst['total'] / suporte_inst.groupby('id_institution')['total'].transform('sum')
suporte_inst['proporcao'] = (suporte_inst['proporcao']).round(2)
suporte_inst
# %%
# Define um dicionário para mapear os códigos de raça para strings
suporte_inst['family_support'] = suporte_inst['family_support'].replace({ 
    1: 'Sim',
    2: 'Não',
    3: 'Não consta no prontuário',
})

suporte_inst.rename(columns={'id_institution':'ILPI', 'family_support': 'Suporte Familiar'}, inplace=True)
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
grau_dependencia = df[['id_institution', 'dependence_degree']]
grau_dependencia.head(20)
# %%
# Filtra apenas as linhas que existam dados de grau_dependencia
grau_dependencia_gruped = grau_dependencia[grau_dependencia['dependence_degree'].notna()].astype({'dependence_degree':'int64'})
grau_dependencia_gruped.head(20)
# %%
# Cria tabela Grau Dependencia para o data lake

grau_dependencia_residente = df[['id_institution', 'uuidv5', 'dependence_degree']]
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
grau_dependencia_inst = grau_dependencia.groupby(['id_institution', 'dependence_degree']).size().reset_index(name='total')
grau_dependencia_inst
# %%
# Calcula proporçao de cada grau_dependencia dentro de cada ILPI
grau_dependencia_inst['proporcao'] = grau_dependencia_inst['total'] / grau_dependencia_inst.groupby('id_institution')['total'].transform('sum')
grau_dependencia_inst['proporcao'] = (grau_dependencia_inst['proporcao']).round(2)
grau_dependencia_inst
# %%
# Define um dicionário para mapear os códigos de raça para strings
grau_dependencia_inst['dependence_degree'] = grau_dependencia_inst['dependence_degree'].replace({ 
    1: 'Sim',
    2: 'Não',
    3: 'Não consta no prontuário',
})

grau_dependencia_inst.rename(columns={'id_institution':'ILPI', 'dependence_degree' : 'grau_dependencia'}, inplace=True)
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
fonte_renda = df[['id_institution', 'elder_income_source']]
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
fonte_renda_inst = fonte_renda.groupby(['id_institution', 'elder_income_source']).size().reset_index(name='total')
fonte_renda_inst
# %%
# Calcula proporçao de cada fonte_renda dentro de cada ILPI
fonte_renda_inst['proporcao'] = fonte_renda_inst['total'] / fonte_renda_inst.groupby('id_institution')['total'].transform('sum')
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
    col_categoria='id_institution',
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
    col_categoria='id_institution',
    col_valor='total',
)
# %%
