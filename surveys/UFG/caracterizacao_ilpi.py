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
import os

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
# NUMERO DE RESIDENTES
# ---------------------
qtde_residentes = (
    df[['id_institution', 'residents_number']]
    .rename(columns={'id_institution': 'ILPI', 'residents_number': 'Número de residentes'})
    .sort_values(by='Número de residentes', ascending=False)
)

qtde_residentes
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    qtde_residentes,
    '../../UFG/tables/01_qtde_residentes.png'
)
# %%
plot_barh(
    qtde_residentes,
    'Distribuição Residentes por ILPI',
    'ILPIs',
    'Qtde Residentes',
    '../../UFG/plots/01_residentes_ILPI.png',
    obs=5
)
# %%
# ---------------------
# DISPOSIÇÃO DAS CAMAS DOS RESIDENTES DE ACORDO COM A NORMA
# ---------------------
# Criando e mapeando as colunas diretamente, com renomeação incluída para camas segundo norma
camas = (df[['id_institution', 'residents_bedroom']]
                        .assign(df_filtered=df['residents_bedroom'].map({1: 'Sim', 2: 'Não'}))  # Mapeando 'residents_bedroom'
                        [['id_institution', 'df_filtered']]  # Selecionando as colunas necessárias
                        .rename(columns={'id_institution': 'ILPI', 'df_filtered': 'Camas segundo a Norma?'})  # Renomeando as colunas
) 

camas
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    camas,
    '../../UFG/tables/02_camas.png'
)
# %%
def plot_barh(data, title, xlabel, ylabel, filename, obs=2, show_text=True, show_values=True):
    """
    Gera um gráfico de barras horizontal com valores percentuais centralizados nas barras
    e o eixo X em valores absolutos.

    Parâmetros:
    - data: DataFrame OU Series (pandas).
    - title: string com o título do gráfico.
    - xlabel: string com o rótulo do eixo X.
    - ylabel: string com o rótulo do eixo Y.
    - filename: string com o caminho e nome do arquivo (ex: 'plots/exemplo.png')
    - obs: número de observações (define quantas cores usar).
    - show_text: se True, exibe observação adicional no gráfico.
    - show_values: se True, exibe os percentuais nas barras.
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

# 🛠️ Se for Series, converte para DataFrame de 1 linha com as categorias como colunas
    if isinstance(data, pd.Series):
        data = data.to_frame().T
        data.index = ['']  # Remove o índice numérico (evita aparecer "0" ou "count" no eixo Y)

    # Paleta de cores personalizada
    all_colors = ["#4E5EA7", '#F28E2B', "#AF3739", '#76B7B2', '#59A14F', '#EDC948']
    color = all_colors[:obs] if isinstance(all_colors, list) else all_colors

    # Cálculo dos percentuais por linha
    percent_df = data.div(data.sum(axis=1), axis=0) * 100

    # Plot
    ax = data.plot(kind='barh', color=color, figsize=(10, 6))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Inserção dos percentuais nas barras
    if show_values:
        for col_idx, container in enumerate(ax.containers):
            col_name = data.columns[col_idx]
            for bar, (idx, percent) in zip(container, percent_df[col_name].items()):
                width = bar.get_width()
                if pd.notna(percent) and width > 0:
                    x = width / 2
                    y = bar.get_y() + bar.get_height() / 2
                    font_size = max(8, min(12, width * 0.25))
                    ax.text(x, y,
                            f'{percent:.1f}%',
                            ha='center',
                            va='center',
                            color='white',
                            fontweight='bold',
                            fontsize=font_size)

    # Observação adicional opcional
    if show_text:
        plt.text(0.075, 0.25, '* Uma das instituições é composta por unidades de moradia',
                 color='red', ha='left', va='bottom', transform=plt.gcf().transFigure, wrap=True)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()
# %%
# ---------------------
# Gráfico 1 - Camas segundo a Norma
# Contando os valores de 'Camas segundo a Norma?' (Sim e Não)
camas_count= camas['Camas segundo a Norma?'].value_counts()

plot_barh(
    camas_count,
    'Distribuição de Camas segundo a Norma',
    'ILPIs',
    'Camas de acordo com a norma',
    '../../UFG/plots/02_camas_norma.png',
    obs=2
)
# %%
# ---------------------
# VEÍCULOS
# ---------------------
# Criando e mapeando as colunas diretamente, com renomeação incluída para veículos
veiculo = (df[['id_institution', 'vehicle']]
                        .assign(df_filtered=df['vehicle'].map({1: 'Sim', 2: 'Não'}))  # Mapeando 'residents_bedroom'
                        [['id_institution', 'df_filtered']]  # Selecionando as colunas necessárias
                        .rename(columns={'id_institution': 'ILPI', 'df_filtered': 'Existe veículo à disposição?'})  # Renomeando as colunas
)

veiculo
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    qtde_residentes,
    '../../UFG/tables/03_veiculos.png'
)
# %%
#----------------------
# Gráfico 2 - Veículos à disposição da ILPI
# Contando os valores (Sim e Não)
veiculo_counts = veiculo['Existe veículo à disposição?'].value_counts()

plot_barh(
    veiculo_counts,
    'Existe veículo à disposição nas ILPIs',
    'ILPIs',
    'veiculos',
    '../../UFG/plots/03_veiculo.png',
    obs=2
)
# %%
