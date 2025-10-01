# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')
# %%
# --------------------
# Bibliotecas
# --------------------
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

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
# SEGURANÇA E MEIO AMBIENTE
# Serviço/sistema de segurança para sua proteção e dos idosos

sist_seg = (df[['id_institution', 'secutiry_system']]
                        .assign(df_filtered=df['secutiry_system'].map({1: 'Sim', 2: 'Não'}))  # Mapeando 'residents_bedroom'
                        [['id_institution', 'df_filtered']]  # Selecionando as colunas necessárias
                        .rename(columns={'id_institution': 'ILPI', 'df_filtered': 'Sistemas_segurança'})  # Renomeando as colunas
)

# Exibindo o resultado
sist_seg
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    sist_seg,
    '../../UFG/tables/08_sist_seg.png'
)
# %%
# ---------------------
# Gráfico 8 - Sistema de Segurança
sist_counts = sist_seg['Sistemas_segurança'].value_counts()

plot_barh(
    sist_counts,
    'Existe Sistema de Segurança na ILPI?',
    'ILPIs',
    '',
    '../../UFG/plots/08_sistema_seguranca.png'
)
# %%
# ---------------------
# Tipos de Serviço/sistema de segurança para sua proteção e dos idosos

# Ajustar a exibição do pandas para mostrar mais caracteres
pd.set_option('display.max_colwidth', None)  # Permite exibir a coluna inteira

tipos_sist_seg = (
    df[["id_institution", "security_device_type___1", "security_device_type___2", "security_device_type___3", "security_device_type___4", "security_device_type___5"]]
    .assign(
        tipos_sist_seguranca= (
            df["security_device_type___1"].map(lambda x: 'Alarme (incêndio/violação)' if x == 1 else ', Não tem alarmes') +
            df["security_device_type___2"].map(lambda x: ', Cameras interno' if x == 1 else ', Não tem cameras internas') +
            df["security_device_type___3"].map(lambda x: ', Cameras externo' if x == 1 else ', Não tem cameras externas') +
            df["security_device_type___4"].map(lambda x: ', Segurança (individuo)' if x == 1 else ', Não tem seguraça (indivíduo)') +
            df["security_device_type___5"].map(lambda x: ', Segurança armada (indivíduo)' if x == 1 else ', Não tem segurança armada (indivíduo)') 
        )
    )
    .assign(tipos_sist_seguranca=lambda x: x['tipos_sist_seguranca'].str.lstrip(', '))  # Limpar vírgula no início da string
    .rename(columns={"id_institution": "ILPI"})  # Renomeando a coluna
    [["ILPI", "tipos_sist_seguranca"]]  # Selecionando apenas as colunas finais
)

tipos_sist_seg
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    tipos_sist_seg,
    '../../UFG/tables/09_tipos_sist_seg.png'
)
# %%
# ---------------------
# Gráfico 10 - Tipos de Sistema de Segurança

# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
tipos_sist_seg.groupby('tipos_sist_seguranca').size().plot(
    kind='barh',
    color=sns.palettes.mpl_palette('Dark2')
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Contagem por Tipo de Sistema de Segurança')
plt.text(-2.5, 2.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIS')
plt.ylabel('Tipo de Sistema de Segurança')

# Exibir gráfico
plt.savefig("../../UFG/plots/09_tipos_sist_seg.png")
plt.show()

#tipos_sist_seg_counts = tipos_sist_seg['tipos_sist_seguranca'].value_counts()

#plot_barh(
#    tipos_sist_seg,
#    'Tipos de Sistemas de Segurança',
#    'ILPIs',
#    'tipos_sist_seg.png'
#)
# %%
# ----------------------------
# Dispositivo/mecanismo (digital/analógico) de chamada que o 
# residente/acolhido na cama possa chamar em caso de necessidade
# de atendimento

disp_chamada = (df[["id_institution", "safety_device_availability"]]
                .assign(df_filtered=df["safety_device_availability"].map({1 :"Sim", 2 :"Não"})) # Mapeando safety_device_availability
                [["id_institution", "df_filtered"]]  # Selecionando colunas necessárias
                .rename(columns={'id_institution': 'ILPI', 'df_filtered': 'Disponibilidade_dispositivo_chamada'})  # Renomeando as colunas
)

disp_chamada
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    disp_chamada,
    '../../UFG/tables/10_disp_chamada.png'
)
# %%
# Gráfico 9 Dispositivo/mecanismo (digital/analógico) de chamada
#disp_counts = disp_chamada["Disponibilidade_dispositivo_chamada"].value_counts()
#
#plot_barh(
#    disp_chamada,
#    'Dispositivo/mecanismo (digital/analógico) de chamada pelo residente',
#    'ILPIs',
#    '09_disp_chamada.png'
#)
# %%
# Contando os valores
counts = disp_chamada["Disponibilidade_dispositivo_chamada"].value_counts()

# Criando o gráfico de barras horizontais
counts.plot(kind='barh', color=['#4E79A7', '#F28E2B'])

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Adicionando título e rótulos
plt.title('Disponibilidade de dispositivo de chamada pelo residente')
plt.xlabel('ILPIS')
plt.ylabel('')

# Exibindo o gráfico
plt.savefig('../../UFG/plots/10_disp_chamada.png')
plt.show()
# -------------------
# %%
# Iluminação adequada

iluminacao = (df[["id_institution", "lighting"]]
              .assign(df_filtered=df["lighting"].map({1 : "Sim", 2 : "Não"})) # Mapeando lighting
              [["id_institution", "df_filtered"]] # Selecionando colunas
              .rename(columns={"id_institution": "ILPI", "df_filtered": "Iluminacao_adequada"})
)

iluminacao
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    iluminacao,
    '../../UFG/tables/11_iluminacao.png'
)
# %%
# -------------------
# Gráfico 12 - iluminação adequada

#iluminacao_counts = iluminacao['Iluminacao_adequada'].value_counts()

#plot_barh(
#   iluminacao,
#   'A iluminição é adequada?',
#   'ILPIs',
#   '10_ilumincacao.png'
#

# %%
# Contando os valores
counts = iluminacao["Iluminacao_adequada"].value_counts()

# Criando o gráfico de barras horizontais
counts.plot(kind='barh', color=['#4E79A7', '#F28E2B'])

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Adicionando título e rótulos
plt.title('A iluminação é adequada?')
plt.text(0.02, 1.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIS')
plt.ylabel('')

# Exibindo o gráfico
plt.savefig('../../UFG/plots/11_ilumincacao.png')
plt.show()
# %%
# --------------------

# Ventilação adequada

ventilacao = (df[["id_institution", "ventilation"]]
             .assign(df_filtered=df["ventilation"].map({1:"Sim", 2:"Não"}))
             [["id_institution", "df_filtered"]]
             .rename(columns={"id_institution": "ILPI", "df_filtered": "Ventilacao_adequada"})

)

ventilacao
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    ventilacao,
    '../../UFG/tables/12_ventilacao.png'
)
# %%
# ------------------
# Gráfico 12 - Ventilação Adequada
# Tamanho da figura
plt.figure(figsize=(10,6))

# Agrupar e plotar o g'rafico de barras horizontais
ventilacao.groupby("Ventilacao_adequada").size().plot(
    kind="barh",
    color=['#4E79A7', '#F28E2B']
)

# Ajustar as bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo x seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Títulos e rótulos
plt.title("A ventilação é adequada?")
plt.text(0.02, 1.3, '* Uma das institíções é composta por unidades de moradia',
         color='red', ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir o gráfico
plt.savefig("../../UFG/plots/12_ventilacao.png")
plt.show()

# %%
# -----------------------
# Pintura do quarto tons pastéis

pintura_quartos = (df[["id_institution", "painting_color"]]
                   .assign(df_filtered=df["painting_color"].map({1: "Sim", 2: "Não"}))
                   [["id_institution", "df_filtered"]]
                   .rename(columns={"id_institution": "ILPI", "df_filtered": "Pintura_tons_pasteis"})
)

pintura_quartos
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    pintura_quartos,
    '../../UFG/tables/13_pintura_quarto.png'
)
# %%
# ---------------------
# Gráfico 13 - Pintura quartos tons pastéis
#  -------------------
# Tamanho da figura
plt.figure(figsize=(10,6))

# Agrupar e plotar o g'rafico de barras horizontais
pintura_quartos.groupby("Pintura_tons_pasteis").size().plot(
    kind="barh",
    color=['#4E79A7', '#F28E2B']
)

# Ajustar as bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo x seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Títulos e rótulos
plt.title("A pintura do quarto é adequada?")
plt.text(0.02, 0.3, '* Uma das instituíções é composta por unidades de moradia',
         color='red', ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir o gráfico
plt.savefig("../../UFG/plots/13_pintura_quarto.png")
plt.show()

# %%
# -------------------
# Acessibilidade para o residente
# Quarto

acessib_quarto = (df[["id_institution", "room_access___1", "room_access___2", "room_access___3"]]
                  .assign(
                        acessib_quarto_list=(
                              df["room_access___1"].map(lambda x: 'Portas largas para cadeirante' if x == 1 else '') +
                              df["room_access___2"].map(lambda x: ', Rampas' if x == 1 else '') +
                              df["room_access___3"].map(lambda x: ', Corrimão para apoio' if x == 1 else '')
                        )
                  )
                  .assign(acessib_quarto_list=lambda x: x['acessib_quarto_list'].str.lstrip(', '))  # Limpar vírgula no início da string
                  .rename(columns={"id_institution": "ILPI"})  # Renomeando a coluna
                  [["ILPI", "acessib_quarto_list"]]  # Selecionando apenas as colunas finais
)

acessib_quarto
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    acessib_quarto,
    '../../UFG/tables/14_acess_quarto.png'
)
# %%
# -------------------
# Gráfico 13 - Acessíbilidade do quarto
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
acessib_quarto.groupby('acessib_quarto_list').size().plot(
    kind='barh',
    color=sns.palettes.mpl_palette('Dark2')
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Tipo de acessibilidade ao quarto do residente')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/14_acessib_quarto.png")
plt.show()
# %%
# --------------------
# Banheiro

acessib_banheiro = (df[["id_institution", "bathroom_access___1", "bathroom_access___2", "bathroom_access___3"]]
                  .assign(
                        acessib_banheiro_list=(
                              df["bathroom_access___1"].map(lambda x: 'Portas largas para cadeirante' if x == 1 else '') +
                              df["bathroom_access___2"].map(lambda x: ', Rampas' if x == 1 else '') +
                              df["bathroom_access___3"].map(lambda x: ', Corrimão para apoio' if x == 1 else '')
                        )
                  )
                  .assign(acessib_banheiro_list=lambda x: x['acessib_banheiro_list'].str.lstrip(', '))  # Limpar vírgula no início da string
                  .rename(columns={"id_institution": "ILPI"})  # Renomeando a coluna
                  [["ILPI", "acessib_banheiro_list"]]  # Selecionando apenas as colunas finais
)

acessib_banheiro
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    acessib_banheiro,
    '../../UFG/tables/15_acess_banheiro.png'
)
# %%
# -------------------
# Gráfico 15 - Acessíbilidade do banheiro
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
acessib_banheiro.groupby('acessib_banheiro_list').size().plot(
    kind='barh',
    color=sns.palettes.mpl_palette('Dark2')
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Tipo de acessibilidade ao banheiro do residente')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/15_acessib_banheiro.png")
plt.show()
# %%
# Refeitório

acessib_refeitorio = (df[["id_institution", "cafeteria___1", "cafeteria___2", "cafeteria___3"]]
                  .assign(
                        acessib_refeitorio_list=(
                              df["cafeteria___1"].map(lambda x: 'Portas largas para cadeirante' if x == 1 else '') +
                              df["cafeteria___2"].map(lambda x: ', Rampas' if x == 1 else '') +
                              df["cafeteria___3"].map(lambda x: ', Corrimão para apoio' if x == 1 else '')
                        )
                  )
                  .assign(acessib_refeitorio_list=lambda x: x['acessib_refeitorio_list'].str.lstrip(', '))  # Limpar vírgula no início da string
                  .rename(columns={"id_institution": "ILPI"})  # Renomeando a coluna
                  [["ILPI", "acessib_refeitorio_list"]]  # Selecionando apenas as colunas finais
)

acessib_refeitorio
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    acessib_refeitorio,
    '../../UFG/tables/16_acess_refeitorio.png'
)
# %%
# -------------------
# Gráfico 16 - Acessíbilidade do refeitório
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
acessib_refeitorio.groupby('acessib_refeitorio_list').size().plot(
    kind='barh',
    color=sns.palettes.mpl_palette('Dark2')
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Tipo de acessibilidade ao refeitorio do residente')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/16_acessib_refeitorio.png")
plt.show()
# %%
# Outras áreas

acessib_outras_areas = (df[["id_institution", "other_areas___1", "other_areas___2", "other_areas___3"]]
                  .assign(
                        acessib_outras_areas_list=(
                              df["other_areas___1"].map(lambda x: 'Portas largas para cadeirante' if x == 1 else '') +
                              df["other_areas___2"].map(lambda x: ', Rampas' if x == 1 else '') +
                              df["other_areas___3"].map(lambda x: ', Corrimão para apoio' if x == 1 else '')
                        )
                  )
                  .assign(acessib_outras_areas_list=lambda x: x['acessib_outras_areas_list'].str.lstrip(', '))  # Limpar vírgula no início da string
                  .rename(columns={"id_institution": "ILPI"})  # Renomeando a coluna
                  [["ILPI", "acessib_outras_areas_list"]]  # Selecionando apenas as colunas finais
)

acessib_outras_areas
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    acessib_outras_areas,
    '../../UFG/tables/17_acess_outras_areas.png'
)
# %%
# -------------------
# Gráfico 17 - Acessíbilidade de outras áreas
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
acessib_outras_areas.groupby('acessib_outras_areas_list').size().plot(
    kind='barh',
    color=sns.palettes.mpl_palette('Dark2')
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Tipo de acessibilidade ao outras areas do residente')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/17_acessib_outras_areas.png")
plt.show()
# %%
# ------------------------
# Quadro geral acessibilidade

quadro_geral_acessib = (acessib_quarto.merge(acessib_banheiro, on="ILPI", how="right") \
                        .merge(acessib_refeitorio, on="ILPI", how="right")\
                        .merge(acessib_outras_areas, on="ILPI", how="right")
)
quadro_geral_acessib

# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    quadro_geral_acessib,
    '../../UFG/tables/18_quadro_geral_acess.png'
)
# -----------------------
# Os profissionais da ILPI utilizam qualquer tipo de EPI's, durante no cuidado com os idosos

uso_epi = (df[["id_institution", "epi_use"]]
           .assign(df_filtered= df["epi_use"].map({1: "Sim", 2: "Não"}))
           [["id_institution", "df_filtered"]]
           .rename(columns={"id_institution": "ILPI", "df_filtered": "Uso_equip_prot_individual"})
)

uso_epi
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    uso_epi,
    '../../UFG/tables/19_uso_epi.png'
)
# %%
# ----------------
# Gráfico 19 - Uso de Equipamento de Proteção Individual

#uso_epi_counts = uso_epi["Uso_equip_prot_individual"].value_counts()

#plot_barh(
#    uso_epi,
#    "Uso de Equipamento de Proteção Individual",
#    "ILPIs",
#    "17_uso_epi.png"
#)
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
uso_epi.groupby('Uso_equip_prot_individual').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Uso de Equipamento de Proteção Individual')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/19_uso_epi.png")
plt.show()
# %%
