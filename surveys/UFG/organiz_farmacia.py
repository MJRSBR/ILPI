# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')
# %%
# --------------------
# Bibliotecas
# --------------------
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from matplotlib.ticker import MaxNLocator

from utils.utils import criar_diretorios
from funcoes.f_plot import plot_config, plot_barh
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
df['institution_name'].rename('id_institution', inplace=True) 
# %%
# -------------------
# Medicamentos
# dentro do prazo de validade

medic_prazo_val = (df[["institution_name", "medication_val_date"]]
                   .assign(df_filtered=df["medication_val_date"].map({1: "Sim", 2: "Não"}))
                   [["institution_name", "df_filtered"]]
                   .rename(columns={"institution_name": "ILPI", "df_filtered": "Medicacao_prazo_validade"})
)

medic_prazo_val
# %%
# -------------------
# Gráfico 18 - Medicamento dentro do prazo de validade

#medic_prazo_val_counts = medic_prazo_val["Medicacao_prazo_validade"].value_counts()
#
#plot_barh(
#    medic_prazo_val,
#    "Medicamento dentro do prazo de validade",
#    "ILPIs",
#    "18_medic_prazo.png"
#)
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
medic_prazo_val.groupby('Medicacao_prazo_validade').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Medicamento dentro do prazo de validade')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("18_medic_prazo")
plt.show()
# %%
# ---------------------
# Embalagem violada

emb_viol = (df[["institution_name", "violeted_pakage"]]
            .assign(df_filtered=df["violeted_pakage"].map({1: "Sim", 2:"Não"}))
            [["institution_name", "df_filtered"]]
            .rename(columns={"institution_name": "ILPI", "df_filtered": "Embalagem_violada"})
)
emb_viol
# %%
# -------------------
# Gráfico 19 - Medicamento com embalagem violada

#emb_viol_counts = emb_viol["Embalagem_violada"].value_counts()
#
#plot_barh(
#    emb_viol,
#    "Medicamento com embalagem violada",
#    "19_medic_emb_violada.png"
#)
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
emb_viol.groupby('Embalagem_violada').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Medicamento com embalagem violada')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("19_medic_emb_violada.png")
plt.show()
# %%
# ------------------
# Geladeira exclusiva ao armazenamento de medicamentos

geladeira_medic = (df[['institution_name', 'medicine_refrigerator']]
                   .assign(df_filtered=df["medicine_refrigerator"].map({1: "Sim", 2: "Não"}))
                   [["institution_name", "df_filtered"]]
                   .rename(columns={"institution_name": "ILPI", "df_filtered": "Geladeira_exclusiva_medicamentos"})
)

geladeira_medic
# %%
# ------------------
# Gráfico 20 - Geladeira exclusiva ao armazenamento de medicamentos

#geladeira_medic_counts = geladeira_medic["Geladeira_exclusiva_medicamentos"].value_counts#()
#
#plot_barh(
#    geladeira_medic,
#    "Geladeira exclusiva ao armazenamento de medicamentos",
#    "20_geladeira_medic.png"
#)
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
geladeira_medic.groupby('Geladeira_exclusiva_medicamentos').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Geladeira exclusiva ao armazenamento de medicamentos')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("20_geladeira_medic.png")
plt.show()
# %%
# ----------------------
# Registro temperatura da geladeira

reg_temp_geladeira = (df[["institution_name", "refrigerator_temp_log"]]
             .assign(df_filtered=df["refrigerator_temp_log"].map({1: "Sim", 2: "Não"}))
             [["institution_name", "df_filtered"]]
             .rename(columns={"institution_name": "ILPI", "df_filtered": "Registro_temperatura_geladeira"})
)

reg_temp_geladeira
# %%
# ---------------------
# Gráfico 21 - Registro temperatura da geladeira

#reg_temp_geladeira_counts = reg_temp_geladeira["Registro_temperatura_geladeira"].#value_counts()
#
#plot_barh(
#    reg_temp_geladeira,
#    "Registro temperatura da geladeira",
#    "21_reg_temp_geladeira.png"
#)
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
reg_temp_geladeira.groupby('Registro_temperatura_geladeira').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Registro temperatura da geladeira')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("21_reg_temp_geladeira.png")
plt.show()
# %%
# ----------------------
# Registro de utilização e frequência uso medicação

reg_medic = (df[["institution_name", "medication_register"]]
             .assign(df_filtered=df["medication_register"].map({1: "Sim", 2: "Não"}))
             [["institution_name", "df_filtered"]]
             .rename(columns={"institution_name": "ILPI", "df_filtered": "Registro_uso_medicacao"})
)

reg_medic
# %%
# ---------------------
# Gráfico 22 - Registro de utilização e frequência uso medicação

#reg_medic_counts = reg_medic["Registro_uso_medicacao"].value_counts()
#
#plot_barh(
#    reg_medic,
#    "Registro de utilização e frequência uso medicação",
#    "22_reg_uso_medicacao.png"
#)
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
reg_medic.groupby('Registro_uso_medicacao').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Registro de utilização e frequência uso medicação')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("22_reg_uso_medicacao.png")
plt.show()
# %%
# ---------------------
# Tipo de registro da medicação

tipo_reg_medic = (df[["institution_name", "medication_register_type___1", "medication_register_type___2", "medication_register_type___3"]]
                  .assign(
                        tipo_reg_medic_list=(
                              df["medication_register_type___1"].map(lambda x: 'livro ata' if x == 1 else '') +
                              df["medication_register_type___2"].map(lambda x: ',  registro individual em papel' if x == 1 else '') +
                              df["medication_register_type___3"].map(lambda x: ', registro individual digital' if x == 1 else '')
                        )
                  )
                  .assign(tipo_reg_medic_list=lambda x: x['tipo_reg_medic_list'].str.lstrip(', '))  # Limpar vírgula no início da string
                  .rename(columns={"institution_name": "ILPI"})  # Renomeando a coluna
                  [["ILPI", "tipo_reg_medic_list"]]  # Selecionando apenas as colunas finais
)

tipo_reg_medic
# %%
# --------------------
# Gráfico 23 - Tipo de registro da medicação
# ---------------------
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
tipo_reg_medic.groupby('tipo_reg_medic_list').size().plot(
    kind='barh',
    color=sns.palettes.mpl_palette('Dark2')
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Tipo de registro da medicação')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
         color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('Tipo de Registro')

# Exibir gráfico
plt.savefig("23_tipo_reg_medic.png")
plt.show()
# %%
# -------------------------
# Substâncias Psicoativas/Psicotrópicas estão guardadas separadamente

med_psico_separado = (df[["institution_name", "psico_drugs_segregation"]]
             .assign(df_filtered=df["psico_drugs_segregation"].map({1: "Sim", 2: "Não"}))
             [["institution_name", "df_filtered"]]
             .rename(columns={"institution_name": "ILPI", "df_filtered": "Subst_psico_segregada"})
)

med_psico_separado
# %%
# ---------------------
# Gráfico 24 - Substâncias Psicoativas/Psicotrópicas estão guardadas separadamente

#med_psico_separado_counts = med_psico_separado["Subst_psico_segregada"].value_counts()
#
#plot_barh(
#    med_psico_separado,
#    "Substâncias Psicoativas/Psicotrópicas estão guardadas separadamente",
#    "22_subst_psico_segregada.png"
#)
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
med_psico_separado.groupby('Subst_psico_segregada').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Substâncias Psicoativas/Psicotrópicas estão guardadas separadamente')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("24_subst_psico_segregada.png")
plt.show()
# %%
# ------------------------
# Como são armazenadas as substâncias psicoativas

psico_armaz = (df[["institution_name", "psico_drugs_storage"]]
               .rename(columns={"institution_name": "ILPI", "psico_drugs_storage": "Onde_sao_armazenados_psicoativos"})
)

psico_armaz
# %%
# -------------------------
# Gráfico 25 - Como são armazenadas as substâncias psicoativas

#plot_barh(
#    psico_armaz,
#    "Como são armazenadas as substâncias psicoativas",
#    "25_psico_armazenamento.png"
#)
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
psico_armaz.groupby('Onde_sao_armazenados_psicoativos').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Como são armazenadas as substâncias psicoativas')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("25_psico_armazenamento.png")
plt.show()
# %%
# ------------------------
# Profissional que faz a separação da medicação a ser tomada pelos idosos

prof_manip_medic = (df[["institution_name", "medication_manipulation___1", "medication_manipulation___2", "medication_manipulation___3",
                         "medication_manipulation___4", "medication_manipulation___5", "medication_manipulation___6", "medication_manipulation___7"]]
                  .assign(
                        prof_manip_medic_list=(
                              df["medication_manipulation___1"].map(lambda x: 'técnico da farmácia' if x == 1 else '') +
                              df["medication_manipulation___2"].map(lambda x: ', farmacêutico(a)' if x == 1 else '') +
                              df["medication_manipulation___3"].map(lambda x: ', auxiliar de enfermagem' if x == 1 else '') +
                              df["medication_manipulation___4"].map(lambda x: ', técnico de enfermagem' if x == 1 else '') +
                              df["medication_manipulation___5"].map(lambda x: ', enfermeiro(a)' if x == 1 else '') +
                              df["medication_manipulation___6"].map(lambda x: ', cuidador(a)' if x == 1 else '') +
                              df["medication_manipulation___7"].map(lambda x: ', outro' if x == 1 else '') 
                        )
                  )
                  .assign(prof_manip_medic_list=lambda x: x['prof_manip_medic_list'].str.lstrip(', '))  # Limpar vírgula no início da string
                  .rename(columns={"institution_name": "ILPI"})  # Renomeando a coluna
                  [["ILPI", "prof_manip_medic_list"]]  # Selecionando apenas as colunas finais
)
prof_manip_medic
# %%
# ---------------------
# Gráfico 26 - Profissional que faz a separação da medicação a ser tomada pelos idosos
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
prof_manip_medic.groupby('prof_manip_medic_list').size().plot(
    kind='barh',
    color=sns.palettes.mpl_palette('Dark2')
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Profissional que faz a separação da medicação a ser tomada pelos idosos')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
         color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('Profissional')

# Exibir gráfico
plt.savefig("26_prof_manipula_medic.png")
plt.show()
# %%
# ----------------------
# Qual é o outro profissional?
outro_profis = (df[["institution_name", "other_meditation_manip"]]
               .rename(columns={"institution_name": "ILPI", "other_meditation_manip": "Outro_prof_dispensa"})
)

outro_profis
# %%
# -------------------------
# Gráfico 27 - Outro profissional dispensa medicamento

plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
outro_profis.groupby('Outro_prof_dispensa').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Qual é o outro profissional?')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("27_outro_prof_dispensa.png")
plt.show()
# %%
# -------------------
# Quadro geral dispensação medicação

quadro_geral_disp = (prof_manip_medic.merge(outro_profis, on="ILPI", how="right"))
quadro_geral_disp