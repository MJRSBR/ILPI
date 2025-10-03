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

from funcoes.f_process import processa_binario, processa_multiresposta
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

sist_seg = processa_binario(df, 
                            'secutiry_system', 
                            'Sistemas_segurança', 
                            {1: 'Sim', 2: 'Não'}
)

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
    'Número de ILPIs',
    '',
    '../../UFG/plots/08_sistema_seguranca.png'
)
# %%
# ---------------------
# Tipos de Serviço/sistema de segurança para sua proteção e dos idosos

# Ajustar a exibição do pandas para mostrar mais caracteres
pd.set_option('display.max_colwidth', None)  # Permite exibir a coluna inteira

tipos_sist_cols = {
    'security_device_type___1': 'Alarme (incêndio/violação)',
    'security_device_type___2': 'Câmeras internas',
    'security_device_type___3': 'Câmeras externas',
    'security_device_type___4': 'Segurança (indivíduo)',
    'security_device_type___5': 'Segurança armada (indivíduo)'
}
tipos_sist_seg = processa_multiresposta(df, tipos_sist_cols, 'Tipos_Sist_Seguranca')

tipos_sist_seg
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    tipos_sist_seg,
    '../../UFG/tables/09_tipos_sist_seg.png'
)
# %%
# ---------------------
# Gráfico 09 - Tipos de Sistema de Segurança

tipos_counts = tipos_sist_seg['Tipos_Sist_Seguranca'].value_counts()
plot_barh(tipos_counts, 
          'Tipo de Sistema de Segurança', 
          'Número de ILPIs', 
          'Percentual Tipo de Sistema Segurança', 
          '../../UFG/plots/09_tipos_sist_seg.png'
)

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
disp_chamada = processa_binario(df, 
                                'safety_device_availability', 
                                'Disponibilidade_disp_chamada', 
                                {1: 'Sim', 2: 'Não'}
)
disp_chamada
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    disp_chamada,
    '../../UFG/tables/10_disp_chamada.png'
)
# %%
# Gráfico 10 Dispositivo/mecanismo (digital/analógico) de chamada
disp_chamada_counts = disp_chamada['Disponibilidade_disp_chamada'].value_counts()
plot_barh(disp_chamada_counts, 
          'Dispositivo/mecanismo (digital/analógico) de chamada', 
          'Número de ILPIs',
           '',
           '../../UFG/plots/10_disp_chamada.png'
)  
# -------------------
# %%
# Iluminação adequada
## - Iluminação
iluminacao = processa_binario(df, 
                              'lighting', 
                              'Iluminacao_adequada', 
                              {1: 'Sim', 2: 'Não'}
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

iluminacao_counts = iluminacao['Iluminacao_adequada'].value_counts()

plot_barh(iluminacao_counts, 
          'A iluminação é adequada?', 
          'Número de ILPIs', '',
          '../../UFG/plots/11_iluminacao.png')

# %%
# --------------------

# Ventilação adequada

ventilacao = processa_binario(df, 
                              'ventilation', 
                              'ventilacao_adequada', 
                              {1: 'Sim', 2: 'Não'}
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


ventilacao_counts = ventilacao['ventilacao_adequada'].value_counts()
plot_barh(ventilacao_counts, 
          'A ventilação é adequada?', 
          'Número de ILPIs', '',
          '../plots/11_ventilacao.png'
)
# %%
# -----------------------
# Pintura do quarto tons pastéis

pintura_quartos=processa_binario(df, 
                                 'painting_color', 
                                 'Pintura_tons_pastel', 
                                 {1: 'Sim', 2: 'Não'}
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
pintura_quartos_counts = pintura_quartos['Pintura_tons_pastel'].value_counts()

plot_barh(pintura_quartos_counts, 
          "Quartos pintados em tons pastel", 
          "ILPI", '',
          '../../UFG/plots/13_pintura_quarto.png'
)

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
# Gráfico 14 - Acessíbilidade do quarto
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
plt.xlabel('Número de ILPIs')
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
plt.xlabel('Número de ILPIs')
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
plt.xlabel('Número de ILPIs')
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
plt.xlabel('Número de ILPIs')
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
# %%
# -----------------------
# Os profissionais da ILPI utilizam qualquer tipo de EPI's, durante no cuidado com os idosos

uso_epi = (df[["id_institution", "epi_use"]]
           .assign(df_filtered= df["epi_use"].map({1: "Sim", 2: "Não"}))
           [["id_institution", "df_filtered"]]
           .rename(columns={"id_institution": "ILPI", "df_filtered": "Uso_equip_prot_individual"})
)
# %%
uso_epi =processa_binario(df, 'epi_use', "Uso_equip_seguranca", {1: 'Sim', 2:'Não'})

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
plt.xlabel('Número de ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/19_uso_epi.png")
plt.show()
# %%
 # CORRIGIR NAN
uso_epi_counts = uso_epi['Uso_equip_seguranca'].value_counts()
plot_barh(uso_epi_counts, 'Uso de Equipamentos de Segurança', 'Número de ILPIs','',
          '../../UFG/plots/19_uso_epi.png')
# %%
