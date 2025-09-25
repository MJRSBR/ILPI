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
# Regulação
# UBS que o residente é encaminhado quando necessário
# -----------------------------

ubs = (df[["institution_name", "ubs", "ubs_1", "ubs_2"]]
       .rename(columns={"institution_name": "ILPI"})
)

ubs
# %%
# --------------------
# Gráfico 40 - UBS que o residente é encaminhado quando necessário

plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
ubs.groupby('ubs_list').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('UBS que o residente é encaminhado quando necessário')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("40_ubs.png")
plt.show()
# %%
# -----------------------------
# UPA que o residente é encaminhado quando necessário
upa = (df[["institution_name", "upa", "upa_1", "upa_2"]]
       .rename(columns={"institution_name": "ILPI"})
)
upa
# %%
# Tratar os dados UPA
# ---------------------------

# Função para dividir a coluna `upa` em partes com base nos delimitadores
def split_upa(value):
    if pd.isna(value):
        return []
    # Dividir o valor da coluna usando os delimitadores "/" e ";"
    parts = [part.strip() for part in re.split(r"[;/]", value)]
    return parts

# Aplicar a função para dividir a coluna `upa` em múltiplas colunas
upa_split = upa['upa'].apply(split_upa)

# Expandir a lista resultante em novas colunas
max_splits = upa_split.map(len).max()  # Número máximo de partes para ajustar o número de colunas
upa_cols = pd.DataFrame(upa_split.tolist(), columns=[f"upa_{i}" for i in range(max_splits)])

# Concatenar com o DataFrame original
df_upa = pd.concat([upa[['institution_name']], upa_cols], axis=1)

# Exibir o resultado
df_upa
# %%
# Gráfico 41 - UPA que o residente é encaminhado quando necessário
# --------------------
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
upa.groupby('upa_list').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('UPA que o residente é encaminhado quando necessário')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("41_upa.png")
plt.show()
# %%
# ILPI é campo de estágio
# -------------------------
estagio = (df[["institution_name", "internship"]]
           .assign(df_filtered=df["internship"].map({1:"Sim", 2:"Não"}))
           [["institution_name", "df_filtered"]]
           .rename(columns={"institution_name": "ILPI", "internship" : "campo_estágio"})
)
# %%
# Gráfico 42 - ILPI é campo de estágio
# -------------------------
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
estagio.groupby('campo_estágio').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('ILPI é campo de estágio')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("42_estagio.png")
plt.show()
# %%
# Quais são as instituíções de ensino e cursos
# -------------------------
inst_curso = (df[["institution_name", "internship_institution", "internship_institution_2", "internship_institution_3",
                "internship_institution_4","internship_course","internship_course_2","internship_course_3","internship_course_4"]]
                .rename(columns={"institution_name": "ILPI", "internship_institution" : "Instituíção A", "internship_institution_2" : "Instituíção B",
                                 "internship_institution_3": "Instituíção C", "internship_institution_4":"Instituíção D","internship_course":"Curso A",
                                 "internship_course_2": "Curso B","internship_course_3": "Curso C","internship_course_4": "Curso C"})
)

inst_curso
# %%
# Gráfico 43 - Quais são as instituíções de ensino e cursos
# -------------------------
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
inst_curso.groupby('ILPI').size().plot(
    kind='barh',
    color=['#4E79A7', '#F28E2B']
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Quais são as instituíções de ensino e cursos')
plt.text(0.02, 0.3,'* Uma das instituíções é composta por unidades de moradia',
        color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("43_inst_curso.png")
plt.show()