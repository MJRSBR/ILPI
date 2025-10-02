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
       .rename(columns={"id_institution": "ILPI"})
       .fillna(" - ")
)

ubs
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    ubs,
    '../../UFG/tables/42_ubs.png'
)
# %%
# --------------------
# Gráfico 42 - UBS que o residente é encaminhado quando necessário

plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
ubs.groupby('ubs').size().plot(
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
plt.xlabel('Número de ILPIs')
plt.ylabel('')

# Exibir gráfico
plt.savefig("../../UFG/plots/42_ubs.png")
plt.show()
# %%
# -----------------------------
# UPA que o residente é encaminhado quando necessário
upa = (df[["id_institution", "upa", "upa_1", "upa_2"]]
       .rename(columns={"id_institution": "ILPI"})
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
upa_split = upa['upa'].apply(split_upa)

# Expandir a lista resultante em novas colunas
max_splits = upa_split.map(len).max()  # Número máximo de partes para ajustar o número de colunas
upa_cols = pd.DataFrame(upa_split.tolist(), columns=[f"upa_{i}" for i in range(max_splits)])

# Concatenar com o DataFrame original
df_upa = pd.concat([upa[['ILPI']], upa_cols], axis=1)

# Exibir o resultado
df_upa
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    df_upa,
    '../../UFG/tables/43_upa.png'
)
# %%


# Gráfico 41 - UPA que o residente é encaminhado quando necessário
# --------------------
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
upa.groupby(['upa', 'upa_1', 'upa_2']).size().plot(
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
# Criando tabela única para regulaçao

quadro_geral_regulacao = pd.merge(ubs, df_upa, how='inner', on="ILPI").fillna(" - ")
quadro_geral_regulacao
# %%

# def salvar_tabela_como_imagem(df, caminho_arquivo, titulo=None, largura_total_max=100):
#     import textwrap
#     import matplotlib.pyplot as plt
#     import numpy as np

#     df_str = df.astype(str)

#     # Calcular comprimento máximo de texto por coluna (incluindo cabeçalho)
#     max_lens = {
#         col: max(df_str[col].apply(len).max(), len(str(col)))
#         for col in df.columns
#     }

#     coluna_principal = max(max_lens, key=max_lens.get)

#     total_chars = sum(max_lens.values())
#     proporcoes = {
#         col: max_lens[col] / total_chars for col in df.columns
#     }

#     largura_por_coluna = {}
#     for col in df.columns:
#         if col == coluna_principal:
#             largura_por_coluna[col] = int(largura_total_max * 0.40)
#         elif df_str[col].nunique() == 1 and df_str[col].unique()[0] == '-':
#             largura_por_coluna[col] = 10
#         else:
#             largura_por_coluna[col] = max(10, int(proporcoes[col] * largura_total_max * 0.60))

#     df_wrapped = df_str.copy()
#     for col in df.columns:
#         largura = largura_por_coluna[col]
#         largura_wrap = max(10, largura // 2)
#         df_wrapped[col] = df_wrapped[col].apply(
#             lambda x: "\n".join(textwrap.wrap(x, width=largura_wrap)) if len(x) > largura else x
#         )

#     largura_em_polegadas = [
#         largura_por_coluna[col] * 0.12
#         for col in df.columns
#     ]
#     total_width = sum(largura_em_polegadas) + 1

#     # Altura dinâmica: calcular média de linhas por célula para ajustar a altura total
#     def contar_linhas(texto):
#         return texto.count('\n') + 1

#     linhas_por_linha = df_wrapped.apply(lambda col: col.map(contar_linhas)).mean(axis=1) # média de linhas por célula na linha
#     fator_altura = linhas_por_linha.mean()

#     row_height = 0.6
#     fig_height = df.shape[0] * row_height * fator_altura + (1.5 if titulo else 1)

#     fig, ax = plt.subplots(figsize=(total_width, fig_height))
#     ax.axis('off')

#     tabela = ax.table(
#         cellText=df_wrapped.values,
#         colLabels=df.columns,
#         cellLoc='center',
#         loc='center'
#     )

#     tabela.auto_set_font_size(False)
#     tabela.set_fontsize(10)
#     tabela.scale(1, 2 * fator_altura)  # escala vertical proporcional ao fator

#     for (row, col), cell in tabela.get_celld().items():
#         if row == 0:
#             cell.set_text_props(weight='bold', color='white')
#             cell.set_facecolor('#40466e')
#         else:
#             cell.set_facecolor('#f1f1f2')
#         cell.set_edgecolor('gray')

#     if titulo:
#         plt.title(titulo, fontsize=14, weight='bold', pad=20)

#     plt.tight_layout()
#     plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
#     plt.close()

#     print(f"✅ Tabela salva como imagem em {caminho_arquivo}")

def salvar_tabela_como_imagem(df, caminho_arquivo, titulo=None, largura_total_max=100):
    import matplotlib.pyplot as plt
    import textwrap
    import pandas as pd

    # 1. Garantir que todos os dados são strings (substituindo applymap por apply+map)
    df_str = df.copy().apply(lambda col: col.map(lambda x: '-' if pd.isna(x) else str(x)))

    # 2. Calcular tamanho do conteúdo por coluna
    max_lens = {
        col: max(df_str[col].apply(len).max(), len(str(col)))
        for col in df.columns
    }

    # 3. Identificar a coluna com maior conteúdo
    coluna_principal = max(max_lens, key=max_lens.get)

    # 4. Calcular proporções
    total_chars = sum(max_lens.values())
    proporcoes = {
        col: max_lens[col] / total_chars for col in df.columns
    }

    # 5. Definir largura das colunas
    largura_por_coluna = {}
    for col in df.columns:
        col_data = df_str[col]
        valores_unicos = col_data.dropna().unique()

        if col == coluna_principal:
            largura_por_coluna[col] = int(largura_total_max * 0.40)

        elif len(valores_unicos) == 1 and valores_unicos[0].strip().lower() in ['-', 'não se aplica']:
            largura_por_coluna[col] = 10  # largura mínima

        else:
            largura_por_coluna[col] = max(10, int(proporcoes[col] * largura_total_max * 0.60))

    # 6. Aplicar quebras de linha
    df_wrapped = df_str.copy()
    for col in df.columns:
        largura = largura_por_coluna[col]
        wrap_limit = max(10, largura // 2)
        df_wrapped[col] = df_wrapped[col].apply(
            lambda x: "\n".join(textwrap.wrap(x, width=wrap_limit)) if len(x) > largura else x
        )

    # 7. Largura total da imagem
    largura_em_polegadas = [largura_por_coluna[col] * 0.12 for col in df.columns]
    total_width = sum(largura_em_polegadas) + 1

    # 8. Altura dinâmica
    def contar_linhas(texto):
        return texto.count('\n') + 1

    # Substituindo applymap por apply+map para evitar FutureWarning
    linhas_por_linha = df_wrapped.apply(lambda col: col.map(contar_linhas)).mean(axis=1)
    fator_altura = linhas_por_linha.mean()

    row_height = 0.6
    fig_height = df.shape[0] * row_height * fator_altura + (1.5 if titulo else 1)

    # 9. Plotagem
    fig, ax = plt.subplots(figsize=(total_width, fig_height))
    ax.axis('off')

    tabela = ax.table(
        cellText=df_wrapped.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1, 2 * fator_altura)

    # 10. Estilo das células
    for (row, col), cell in tabela.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#40466e')
        else:
            cell.set_facecolor('#f1f1f2')
        cell.set_edgecolor('gray')

    if titulo:
        plt.title(titulo, fontsize=14, weight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✅ Tabela salva como imagem em {caminho_arquivo}")







    # %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    quadro_geral_regulacao,
    '../../UFG/tables/44_quadro_geral_regulacao.png',
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
    '../../UFG/tables/45_estagio.png'
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
plt.savefig("../../UFG/plots/45_estagio.png")
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
    '../../UFG/tables/46_inst_ensino_curso.png'
)
# %%

