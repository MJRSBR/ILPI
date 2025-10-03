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
from funcoes.f_plot import plot_config, salvar_tabela_como_imagem
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
df.rename(columns={'institution_name':'id_institution'}, inplace=True)
df
# %%
# Regulação
# UBS que o residente é encaminhado quando necessário
# -----------------------------

ubs = (df[["id_institution", "ubs", "ubs_1", "ubs_2"]]
       .rename(columns={
           "id_institution": "ILPI",
           "ubs": "UBS",
           "ubs_1": "UBS_1",
           "ubs_2": "UBS_2"})
       .fillna(" - ")
)

ubs
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    ubs,
    '../../UFG/tables/53_ubs.png'
)

# %%
# -----------------------------
# UPA que o residente é encaminhado quando necessário
upa = (df[["id_institution", "upa", "upa_1", "upa_2"]]
       .rename(columns={
           "id_institution": "ILPI",
           'upa': 'UPA', 
           'upa_1': 'UPA_1', 
           'upa_2': 'UPA_2'})
           .fillna(" - ")
)
upa
# %%
# Tratar os dados UPA
# ---------------------------

# Função para dividir a coluna `upa` em partes com base nos delimitadores
def split_upa(value):
    import re
    if pd.isna(value):
        return []
    # Dividir o valor da coluna usando os delimitadores "/" e ";"
    parts = [part.strip() for part in re.split(r"[;/]", value)]
    return parts

# Aplicar a função para dividir a coluna `upa` em múltiplas colunas
upa_split = upa['UPA'].apply(split_upa)

# Expandir a lista resultante em novas colunas
max_splits = upa_split.map(len).max()  # Número máximo de partes para ajustar o número de colunas
upa_cols = pd.DataFrame(upa_split.tolist(), columns=[f"upa_{i}" for i in range(max_splits)])

# Concatenar com o DataFrame original
df_upa = pd.concat([upa[['ILPI']], upa_cols], axis=1).fillna(" - ")

# Exibir o resultado
df_upa
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    df_upa,
    '../../UFG/tables/54_upa.png'
)
# %%

# Criando tabela única para regulaçao

quadro_geral_regulacao = pd.merge(ubs, df_upa, how='inner', on="ILPI").fillna(" - ")
quadro_geral_regulacao
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    quadro_geral_regulacao,
    '../../UFG/tables/55_quadro_geral_regulacao.png',
    largura_total_max=120

)
# %%

# ILPI é campo de estágio
# -------------------------
estagio = (df[["id_institution", "internship"]]
           .assign(df_filtered=df["internship"].map({1:"Sim", 2:"Não"}))
           [["id_institution", "df_filtered"]]
           .rename(columns={"id_institution": "ILPI", "df_filtered" : "campo_estágio"})
)
estagio
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    estagio,
    '../../UFG/tables/56_estagio.png'
)
# %%
# Gráfico 45 - ILPI é campo de estágio
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
plt.xlabel('Numero de ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/56_estagio.png")
plt.show()
# %%
# Quais são as instituíções de ensino e cursos
# -------------------------
inst_curso = (df[["id_institution", "internship_institution", "internship_institution_2", "internship_institution_3",
                "internship_institution_4","internship_course","internship_course_2","internship_course_3","internship_course_4"]]
                .rename(columns={"id_institution": "ILPI", "internship_institution" : "Instituíção A", "internship_institution_2" : "Instituíção B",
                                 "internship_institution_3": "Instituíção C", "internship_institution_4":"Instituíção D","internship_course":"Curso A",
                                 "internship_course_2": "Curso B","internship_course_3": "Curso C","internship_course_4": "Curso D"})
)

inst_curso
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    inst_curso,
    '../../UFG/tables/57_inst_ensino_curso.png'
)
# %%

