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
from funcoes.f_process import processa_multiresposta, processa_uma_variavel_com_opcoes
from funcoes.f_process import criar_df_com_soma_por_prefixo, processa_binario
from funcoes.f_plot import plot_config, salvar_tabela_como_imagem
# %%
def processa_uma_variavel_com_opcoes(df, coluna_original, nome_saida, mapa_valores):
    """
    Processa códigos inteiros para uma string descritiva (concatenada) com base em um dicionário de mapeamento.

    Parâmetros:
    - df: DataFrame original.
    - coluna_original: str, nome da coluna com códigos.
    - nome_saida: str, nome da nova coluna de saída.
    - mapa_valores: dict, mapeamento de código -> texto.

    Retorna:
    - DataFrame com 'ILPI' e a nova coluna.
    """
    temp = df[["id_institution", coluna_original]].copy()
    
    # Concatena textos com base nos valores
    def construir_texto(valor):
        partes = [txt for cod, txt in mapa_valores.items() if valor == cod]
        return ', '.join(partes) if partes else 'Dados não coletados'
    
    temp[nome_saida] = temp[coluna_original].map(construir_texto)
    temp = temp.rename(columns={"id_institution": "ILPI"})[["ILPI", nome_saida]]
    
    return temp
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
banho_sol = processa_binario(df, 
                             'sunbathing', 
                             'Area_banho_sol', 
                             {1: 'Sim', 2:'Não'}
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
banho_sol.groupby('Area_banho_sol').size().plot(
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
plt.xlabel('Número de ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/35_banho_sol.png")
plt.show()
# %%
# Área recebimento de visitas e familiares
# ----------------------
area_vis_familia = processa_binario(df, 
                                    'visiting_area', 
                                    'Area_visitacao_familia', 
                                    {1: 'Sim', 2:'Não'}
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
area_vis_familia.groupby('Area_visitacao_familia').size().plot(
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
plt.xlabel('Número de ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/36_area_vis_familia.png")
plt.show()
# %%

# Área de atividades sociais
# ---------------------
area_ativ_social = processa_binario(df, 
                                    'social_area', 
                                    'Area_ativ_social', 
                                    {1: 'Sim', 2:'Não'}
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
area_ativ_social.groupby('Area_ativ_social').size().plot(
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
plt.xlabel('Número de ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/37_area_ativ_social.png")
plt.show()
# %%
# Música ambiente na ILPI
# ---------------------------
musica_ambiente = processa_binario(df, 
                                   'ambient_music', 
                                   'Musica_ambiente', 
                                   {1: 'Sim', 2:'Não'}
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
musica_ambiente.groupby('Musica_ambiente').size().plot(
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
plt.xlabel('Número de ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/38_musica_ambiente.png")
plt.show()
# %%
# Cardápio visível para consulta
# ---------------------------
cardapio_visivel = processa_binario(df, 
                                    'menu', 
                                    'Cardapio_visivel', 
                                    {1: 'Sim', 2:'Não'}
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
cardapio_visivel.groupby('Cardapio_visivel').size().plot(
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
plt.xlabel('Número de ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/39_cardapio_visivel.png")
plt.show()
# %%
# Frequência que o cardápio é atualizado
# ----------------------------------
mapa = {
    1: 'diário',
    2: 'semanal',
    3: 'quinzenal',
    4: 'mensal'
}

freq_atualiz_cardapio = processa_uma_variavel_com_opcoes(
    df,
    'semanal_menu',
    'freq_atualiz_cadapio_list',
    mapa
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
freq_atualiz_cardapio.groupby('freq_atualiz_cadapio_list').size().plot(
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
plt.xlabel('Número de ILPIs')
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
# %%
oficinas_atividades_cols = {
    "recreation_type___1" : 'Oficina de jardinagem',
    "recreation_type___2" : 'Oficina de costura', 
    "recreation_type___3" : 'Oficina de artesanato',
    "recreation_type___4" : 'Oficina de marcenaria', 
    "recreation_type___5" : 'Dança de salão', 
    "recreation_type___6" : 'Datas comemorativas', 
    "recreation_type___7" : 'Missas/Cultos Ecumênicos'
}

oficinas_atividades = processa_multiresposta(df, oficinas_atividades_cols, 'Oficinas_ atividades')

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
oficinas_atividades.groupby('Oficinas_ atividades').size().plot(
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
plt.xlabel('Número de ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/41_oficinas_atividades.png")
plt.show()
# %%

# %%
## - Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem

verif_reg = df[[
    'id_institution', 'medical_record___1', 'medical_record___2',	'medical_record___3', 'medical_record___4',
    'medical_record___5', 'medical_record___6',	'admission_file_signed___1', 'admission_file_signed___2', 
    'admission_file_signed___3', 'admission_file_signed___4', 'admission_file_signed___5', 'admission_file_signed___6',
    'patient_bath___1', 'patient_bath___2',	'patient_bath___3',	'patient_bath___4','patient_bath___5', 'patient_bath___6',
    'imc_index___1','imc_index___2', 'imc_index___3', 'imc_index___4', 'imc_index___5', 'imc_index___6', 
    'physical_cont_record___1',	'physical_cont_record___2',	'physical_cont_record___3',	'physical_cont_record___4',
    'physical_cont_record___5', 'physical_cont_record___6',	'mem_scale___1', 'mem_scale___2', 'mem_scale___3', 
    'mem_scale___4', 'mem_scale___5', 'mem_scale___6', 'mem_prev_actions___1', 'mem_prev_actions___2', 'mem_prev_actions___3',
    'mem_prev_actions___4',	'mem_prev_actions___5',	'mem_prev_actions___6',	'pain_register___1', 'pain_register___2',	
    'pain_register___3', 'pain_register___4', 'pain_register___5', 'pain_register___6',	'meem_care_actions___1',
    'meem_care_actions___2', 'meem_care_actions___3', 'meem_care_actions___4', 'meem_care_actions___5',	'meem_care_actions___6',
    'rehab_activities_register___1', 'rehab_activities_register___2', 'rehab_activities_register___3', 'rehab_activities_register___4',
    'rehab_activities_register___5', 'rehab_activities_register___6', 'rehab_activities___1', 'rehab_activities___2', 
    'rehab_activities___3',	'rehab_activities___4',	'rehab_activities___5',	'rehab_activities___6']]

verif_reg
# %%

dic_renomear_med_rec = {
    'id_institution': 'ILPI',
    'medical_record___1': 'Não se aplica'
}

df_medical_record = verif_reg[['id_institution']].copy()
df_medical_record = (df_medical_record.join(criar_df_com_soma_por_prefixo(verif_reg, "medical_record___"))
                     .rename(columns=dic_renomear_med_rec))

df_medical_record

salvar_tabela_como_imagem(
    df_medical_record,
    '../../UFG/tables/42_tab_verif_reg_medic.png',
    'Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem'
)
# %%

dic_renomear_admiss_file = {
    'id_institution': 'ILPI',
    'admission_file_signed___1': 'Não se aplica'
}

df_admiss_file = verif_reg[['id_institution']].copy()
df_admiss_file = (df_admiss_file.join(criar_df_com_soma_por_prefixo(verif_reg, 'admission_file_signed___'))
                  .rename(columns=dic_renomear_admiss_file))

salvar_tabela_como_imagem(
    df_admiss_file,
    '../../UFG/tables/43_tab_verif_ficha_admissao.png',
    'Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem'
)
# %%

dic_renomear_banho = {
    'id_institution': 'ILPI',
    'patient_bath___1': 'Não se aplica'
}

df_banho = verif_reg[['id_institution']].copy()
df_banho = (df_banho.join(criar_df_com_soma_por_prefixo(verif_reg, "patient_bath___"))
            .rename(columns=dic_renomear_banho))

salvar_tabela_como_imagem(
    df_banho,
    '../../UFG/tables/44_tab_verif_banho_resid.png',
    'Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem'
)
# %%
dic_renomear_imc_index = {
    'id_institution': 'ILPI',
    'imc_index___1': 'Não se aplica'
}

df_imc_index = verif_reg[['id_institution']].copy()
df_imc_index = (df_imc_index.join(criar_df_com_soma_por_prefixo(verif_reg, "imc_index___"))
            .rename(columns=dic_renomear_imc_index))

salvar_tabela_como_imagem(
    df_imc_index,
    '../../UFG/tables/45_tab_verif_imc_index_resid.png',
    'Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem'
)
# %%
dic_renomear_reg_fisico = {
    'id_institution': 'ILPI',
    'physical_cont_record___1': 'Não se aplica'
}

df_reg_fisico = verif_reg[['id_institution']].copy()
df_reg_fisico = (df_reg_fisico.join(criar_df_com_soma_por_prefixo(verif_reg, "physical_cont_record___"))
            .rename(columns=dic_renomear_reg_fisico))

salvar_tabela_como_imagem(
    df_reg_fisico,
    '../../UFG/tables/46_tab_verif_reg_fisico_resid.png',
    'Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem'
)
# %%
dic_renomear_escala_mem = {
    'id_institution': 'ILPI',
    'mem_scale___1': 'Não se aplica'
}

df_escala_mem = verif_reg[['id_institution']].copy()
df_escala_mem = (df_escala_mem.join(criar_df_com_soma_por_prefixo(verif_reg, "mem_scale___"))
            .rename(columns=dic_renomear_escala_mem))

salvar_tabela_como_imagem(
    df_escala_mem,
    '../../UFG/tables/47_tab_verif_escala_mem.png',
    'Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem'
)
# %%
dic_renomear__mem_ac_prev = {
    'id_institution': 'ILPI',
    'mem_prev_actions___1': 'Não se aplica'
}

df_mem_ac_prev = verif_reg[['id_institution']].copy()
df_mem_ac_prev = (df_mem_ac_prev.join(criar_df_com_soma_por_prefixo(verif_reg, "mem_prev_actions___"))
            .rename(columns=dic_renomear__mem_ac_prev))

salvar_tabela_como_imagem(
    df_mem_ac_prev,
    '../../UFG/tables/48_tab_verif__mem_ac_prev.png',
    'Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem'
)
# %%
dic_renomear_reg_dor = {
    'id_institution': 'ILPI',
    'pain_register___1': 'Não se aplica'
}

df_reg_dor = verif_reg[['id_institution']].copy()
df_reg_dor = (df_reg_dor.join(criar_df_com_soma_por_prefixo(verif_reg, "pain_register___"))
            .rename(columns=dic_renomear_reg_dor))

salvar_tabela_como_imagem(
    df_reg_dor,
    '../../UFG/tables/49_tab_verif_reg_dor.png',
    'Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem'
)
# %%

dic_renomear_mem_acao_cuid = {
    'id_institution': 'ILPI',
    'meem_care_actions___1': 'Não se aplica'
}

df_mem_acao_cuid = verif_reg[['id_institution']].copy()
df_mem_acao_cuid = (df_mem_acao_cuid.join(criar_df_com_soma_por_prefixo(verif_reg, "meem_care_actions___"))
            .rename(columns=dic_renomear_mem_acao_cuid))

salvar_tabela_como_imagem(
    df_mem_acao_cuid,
    '../../UFG/tables/50_tab_verif_mem_acao_cuid.png',
    'Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem'
)
# %%

dic_renomear_reg_ativ_reab = {
    'id_institution': 'ILPI',
    'rehab_activities_register___1': 'Não se aplica'
}

df_reg_ativ_reab = verif_reg[['id_institution']].copy()
df_reg_ativ_reab = (df_reg_ativ_reab.join(criar_df_com_soma_por_prefixo(verif_reg, "rehab_activities_register___"))
            .rename(columns=dic_renomear_reg_ativ_reab))

salvar_tabela_como_imagem(
    df_reg_ativ_reab,
    '../../UFG/tables/51_tab_verif_reg_ativ_reab.png',
    'Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem'
)
# %%

dic_renomeaf_ativ_reab = {
    'id_institution': 'ILPI',
    'rehab_activities___1': 'Não se aplica'
}

df_ativ_reab = verif_reg[['id_institution']].copy()
df_ativ_reab = (df_ativ_reab.join(criar_df_com_soma_por_prefixo(verif_reg, "rehab_activities___"))
            .rename(columns=dic_renomeaf_ativ_reab))

salvar_tabela_como_imagem(
    df_ativ_reab,
    '../../UFG/tables/52_tab_verif_ativ_reab.png',
    'Verificação aleatória de pelo menos 5 prontuários/fichas e/ou documentação de saúde e enfermagem'
)
# %%
