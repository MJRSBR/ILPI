import os
import re
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import textwrap # serve para formatar textos, ajustando-os para caber em uma largura específica, com a possibilidade de quebrar linhas e aplicar recuo.
from matplotlib.ticker import MaxNLocator
# ----------------------------------------

def salvar_tabela_como_imagem(df, caminho_arquivo, titulo=None, largura_max_coluna=30):
    """ Salva a tabela gerada em .png.
        Parâmetros:
        - df: DataFrame do pandas.
        - caminho_arquivo: define o caminho onde será gravada a imagem (Ex: '../tables/nome_arquivo.png')
        - title: string com o título da tabela (opcional)
        - largura_max_coluna=30: define a largura das colunas da tabela
    """

    # Copiar DataFrame e aplicar quebra de linha
    df_wrapped = df.copy()
    for col in df_wrapped.columns:
        df_wrapped[col] = df_wrapped[col].astype(str).apply(
            lambda x: "\n".join(textwrap.wrap(x, largura_max_coluna)) if len(x) > largura_max_coluna else x
        )

    # Calcular largura ideal por coluna com base no maior item (linha ou cabeçalho)
    col_widths = [
        max(
            df_wrapped[col].apply(lambda x: len(max(str(x).split("\n"), key=len))).max(),
            len(str(col))
        ) * 0.12
        for col in df_wrapped.columns
    ]
    total_width = sum(col_widths) + 1

    # Altura baseada no número de linhas
    row_height = 0.6
    fig_height = df.shape[0] * row_height + (1.5 if titulo else 1)

    fig, ax = plt.subplots(figsize=(total_width, fig_height))
    ax.axis('off')

    tabela = ax.table(
        cellText=df_wrapped.values,
        colLabels=df_wrapped.columns,
        cellLoc='center',
        loc='center'
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1, 1.5)

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

# ----------------------------------------

def plot_barh(data, title, xlabel, ylabel, filename, obs=2, show_text=True, show_values=True):
    """
    Gera um gráfico de barras horizontal com valores percentuais centralizados nas barras
    e o eixo X em valores absolutos.

    Parâmetros:
    - data: DataFrame do pandas (colunas devem corresponder às categorias).
    - title: string com o título do gráfico.
    - xlabel: string com o rótulo do eixo X.
    - ylabel: string com o rótulo do eixo Y.
    - filename: string com o caminho e nome do arquivo (ex: 'plots/exemplo.png')
    - obs: número de observações (define quantas cores usar).
    - show_text: se True, exibe observação adicional no gráfico.
    - show_values: se True, exibe os percentuais nas barras.
    """
    # Paleta de cores personalizada
    all_colors = ["#4E5EA7", '#F28E2B', "#AF3739", '#76B7B2', '#59A14F', '#EDC948']
    color = all_colors[:obs] if isinstance(all_colors, list) else all_colors

    # Cálculo dos percentuais por linha (ILPI)
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
        plt.text(0.075, 0.3, '* Uma das instituições é composta por unidades de moradia',
                 color='red', ha='left', va='bottom', transform=plt.gcf().transFigure, wrap=True)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

# ----------------------------------------

def plot_percentual_por_ilpi(pivot_df: pd.DataFrame, output_path: str, title=str, legend_title=str):
    """
    Gera um gráfico de barras empilhadas mostrando o percentual de faixas de tempo de instituição por ILPI.

    Parâmetros:
    - pivot_df: pd.DataFrame
        DataFrame com contagem de residentes por faixa de tempo e por ILPI (ILPIs como índices).
    - output_path: str
        Caminho do arquivo para salvar a imagem do gráfico (ex: '../plots/nome_do_arquivo.png').
    """

    # Calcula os percentuais por ILPI (linha)
    pivot_percent = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

    # Paleta de cores personalizada (1 cor por faixa etária — total 8 faixas)
    custom_colors = [
        '#4E79A7',  # Azul escuro
        "#092436",  # Azul claro
        "#A7794C",  # Laranja
        "#E6811C",  # Laranja claro
        "#24D20D",  # Verde
        '#8CD17D',  # Verde claro
        "#9D7E0E",  # Amarelo escuro
        "#B72A56"   # Rosa claro
    ]

    # Criação do gráfico empilhado
    ax = pivot_df.plot(
        kind='bar',
        stacked=True,
        figsize=(12, 6),
        color=custom_colors
    )

    # Adiciona rótulos nos segmentos de barra
    for bars, col in zip(ax.containers, pivot_df.columns):  # para cada faixa de tempo
        for bar, (ilpi, percent) in zip(bars, pivot_percent[col].items()):
            height = bar.get_height()
            if height > 0 and not pd.isna(percent):
                x = bar.get_x() + bar.get_width() / 2  # centraliza o texto no segmento.
                y = bar.get_y() + height / 2           # posiciona o texto no meio vertical.
                font_size = max(8, min(12, height * 0.25)) # Ajuste conforme necessário 
                ax.text(
                    x, y,
                    f'{percent: .1f}%', #  .1f para uma casa decimal
                    ha='center',
                    va='center',
                    color='white',
                    fontweight='bold',
                    fontsize=font_size
                )

    # Eixos e legenda
    plt.xlabel('ILPI')
    plt.ylabel('Número de Residentes')
    plt.title(title)
    plt.xticks(rotation=0)
    plt.legend(title=legend_title, bbox_to_anchor=(1.0, 1), loc='upper left')

    # Salvar e exibir
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico salvo como imagem: {output_path}")
    plt.show()     

# ----------------------------------------

#def plot_bar_flex_auto(data, title, xlabel, ylabel, filename,
#                       orientation='h', value_format='percent',
#                       show_values=True, show_text=True,
#                       col_categoria=None, col_valor=None, col_percent=None,
#                       xtick_rotation=0):
#    """
#    Gera gráfico de barras (horizontal ou vertical) com valor absoluto no eixo
#    e valor percentual ou absoluto no centro da barra.
#
#    A função detecta automaticamente se deve calcular o percentual ou usar uma coluna existente.
#
#    Parâmetros:
#    - data: DataFrame original (com ou sem percentuais)
#    - title: título do gráfico
#    - xlabel / ylabel: rótulos dos eixos
#    - filename: caminho para salvar o gráfico
#    - orientation: 'h' ou 'v'
#    - value_format: 'percent' ou 'absolute'
#    - show_values: exibe texto nas barras
#    - show_text: mostra anotação adicional
#    - col_categoria / col_valor / col_percent: nomes das colunas (ou None para auto)
#    - xtick_rotation: ângulo de rotação dos rótulos do eixo X (ex: 0, 45, 90)
#    """
#
#      # Paleta de cores personalizada (1 cor por faixa etária — total 8 faixas)
#    custom_colors = [
#        '#4E79A7',  # Azul escuro
#        "#092436",  # Azul claro
#        "#A7794C",  # Laranja
#        "#E6811C",  # Laranja claro
#        "#24D20D",  # Verde
#        '#8CD17D',  # Verde claro
#        "#9D7E0E",  # Amarelo escuro
#        "#B72A56"   # Rosa claro
#    ]
#
#    is_horizontal = orientation == 'h'
#    kind = 'barh' if is_horizontal else 'bar'
#    
#    df = data.copy()
#
#    # --- Autoidentificação das colunas numéricas ---
#    if col_valor is None:
#        col_valor = df.select_dtypes(include='number').columns[0]
#
#    if col_categoria is None:
#        if df.index.name is not None and df.index.name != col_valor:
#            col_categoria = df.index.name
#            df = df.reset_index()
#        else:
#            col_categoria = df.columns[0]
#
#    if col_percent is None:
#        percent_candidates = [c for c in df.columns if 'propor' in c.lower() or '%' in c]
#        if percent_candidates:
#            col_percent = percent_candidates[0]
#
#    # --- Base para plotagem ---
#    df_plot = df[[col_categoria, col_valor]].copy()
#    df_plot.set_index(col_categoria, inplace=True)
#
#    # --- Percentuais ---
#    if value_format == 'percent':
#        if col_percent and col_percent in df.columns:
#            df_plot['percent'] = df.set_index(col_categoria)[col_percent] * 100
#        else:
#            total = df_plot[col_valor].sum()
#            df_plot['percent'] = (df_plot[col_valor] / total) * 100
#
#    # --- Plot ---
#    ax = df_plot[col_valor].plot(kind=kind, figsize=(10, 6), color=custom_colors)
#    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
#    plt.title(title)
#    plt.xlabel(xlabel)
#    plt.ylabel(ylabel)
#
#    # --- Texto nas barras ---
#    if show_values:
#        for idx, bar in zip(df_plot.index, ax.containers[0]):
#            value = bar.get_width() if is_horizontal else bar.get_height()
#            text = f'{df_plot.loc[idx, "percent"]:.1f}%' if value_format == 'percent' else f'{int(value)}'
#            x = value / 2 if is_horizontal else bar.get_x() + bar.get_width() / 2
#            y = bar.get_y() + bar.get_height() / 2 if is_horizontal else value / 2
#            font_size = max(8, min(12, value * 0.25))
#            ax.text(x, y, text, ha='center', va='center', color='white', fontweight='bold', fontsize=font_size)
#
#    # --- Texto extra opcional ---
#    if show_text:
#        plt.text(0.02, 0.3, '* Uma das instituições é composta por unidades de moradia',
#                 color='red', ha='left', va='bottom', transform=plt.gcf().transFigure, wrap=True)
#
#    # --- Rotação dos rótulos do eixo X ---
#    if not is_horizontal:
#        plt.xticks(rotation=xtick_rotation)
#
#    plt.tight_layout()
#    plt.savefig(filename, dpi=300, bbox_inches='tight')
#    print(f"✅ Gráfico salvo como imagem: {filename}")
#    plt.show()

    
# ----------------------------------------

def plot_bar_flex_unificado(data, title, xlabel, ylabel, filename,
                            orientation='h', value_format='percent',
                            show_values=True, show_text=True,
                            col_categoria=None, col_valor=None,
                            col_percent=None, col_grupo=None,
                            xtick_rotation=0):
    """
    Gera gráfico de barras (horizontal/vertical), simples ou empilhado, com suporte a percentuais ou absolutos.

    Parâmetros:
    - data: DataFrame
    - title, xlabel, ylabel: Títulos e rótulos dos eixos
    - filename: caminho para salvar o gráfico
    - orientation: 'h' ou 'v'
    - value_format: 'percent' ou 'absolute'
    - show_values: mostra valores nas barras
    - show_text: insere anotação adicional
    - col_categoria: coluna de categorias (auto se None)
    - col_valor: coluna de valores numéricos (auto se None)
    - col_percent: coluna com percentuais (auto se None)
    - col_grupo: coluna de agrupamento (para gráfico empilhado)
    - xtick_rotation: rotação dos rótulos no eixo X
    """

    custom_colors = [
        '#4E79A7', "#092436", "#A7794C", "#E6811C",
        "#24D20D", '#8CD17D', "#9D7E0E", "#B72A56"
    ]

    df = data.copy()
    # Define o tipo do gráfico com base na orientação ('h' para horizontal, 'v' para vertical).
    is_horizontal = orientation == 'h'
    kind = 'barh' if is_horizontal else 'bar'

    # --- Autoidentificação das colunas ---
    # Numéricas
    # Seleciona a última coluna numérica do DataFrame como valor se não for passada explicitamente.
    if col_valor is None:
        col_valor = df.select_dtypes(include='number').columns[-1]

    # Categóricas
    # Procura a primeira coluna com número de categorias menor que o número de linhas (boa heurística para identificar categorias).
    if col_categoria is None:
        for c in df.columns:
            if c != col_valor and df[c].nunique() < len(df):
                col_categoria = c
                break
    # Para empilhamento das colunas        
    # Tenta encontrar uma coluna extra para servir como agrupador (como "raça", "sexo" etc.)
    if col_grupo is None:
        possible_groups = [c for c in df.columns if c not in [col_valor, col_categoria]]
        if possible_groups:
            col_grupo = possible_groups[0]
        else:
            col_grupo = None

    # --- Preparar dados ---
    # Se houver agrupamento (col_grupo): gráfico empilhado
    if col_grupo:
        # reorganiza os dados em formato de tabela dinâmica (linhas = categorias, colunas = grupos).
        df_pivot = df.pivot_table(index=col_categoria, columns=col_grupo, values=col_valor, aggfunc='sum').fillna(0)
        df_plot = df_pivot.copy()

        # Para mostrar percentuais no centro das barras
        # divide cada linha pelo total da linha para obter percentuais (100% por categoria).
        percent_df = df_plot.div(df_plot.sum(axis=1), axis=0) * 100
    else:
        # Se não houver agrupamento: gráfico de barras simples
        # Define df_plot com a categoria no índice.
        df_plot = df[[col_categoria, col_valor]].copy()
        df_plot.set_index(col_categoria, inplace=True)

        # Se value_format == 'percent', calcula os percentuais a serem exibidos.
        if value_format == 'percent':
            if col_percent and col_percent in df.columns:
                df_plot['display_value'] = df.set_index(col_categoria)[col_percent] * 100
            else:
                total = df_plot[col_valor].sum()
                df_plot['display_value'] = (df_plot[col_valor] / total) * 100
        else:
            df_plot['display_value'] = df_plot[col_valor]

    # --- Plotagem ---
    ax = df_plot.plot(kind=kind, figsize=(10, 6),
                      stacked=bool(col_grupo),
                      color=custom_colors[:len(df_plot.columns)])
    
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # --- Inserção de valores ---
    if show_values:
        # Para gráfico empilhado
        if col_grupo:
            # Percorre cada "grupo" dentro do empilhamento:
            for bars, col in zip(ax.containers, df_plot.columns): # ax.containers: grupos de barras no gráfico
                for bar, (idx, abs_val) in zip(bars, df_plot[col].items()):
                    if is_horizontal:
                        width = bar.get_width()
                        y = bar.get_y() + bar.get_height() / 2
                        x = bar.get_x() + width / 2
                    else:
                        height = bar.get_height() # bar.get_height(): altura da barra (valor absoluto)
                        x = bar.get_x() + bar.get_width() / 2
                        y = bar.get_y() + height / 2

                    if value_format == 'percent':
                        percent_val = percent_df.loc[idx, col] # percent_df.loc[idx, col]: valor percentual daquela parte da barra
                        if percent_val > 0:
                            ax.text(x, y, f'{percent_val:.1f}%', ha='center', va='center',
                                    color='white', fontweight='bold', fontsize=9)
                    else:
                        if abs_val > 0:
                            ax.text(x, y, f'{int(abs_val)}', ha='center', va='center',
                                    color='white', fontweight='bold', fontsize=9)
        else:
            # Para gráfico simples
            for idx, bar in zip(df_plot.index, ax.containers[0]):
                value = bar.get_width() if is_horizontal else bar.get_height()
                display_value = df_plot.loc[idx, 'display_value']

                if value_format == 'percent':
                    text = f'{display_value:.1f}%'
                else:
                    text = f'{int(display_value)}'

                x = value / 2 if is_horizontal else bar.get_x() + bar.get_width() / 2
                y = bar.get_y() + bar.get_height() / 2 if is_horizontal else value / 2

                ax.text(x, y, text, ha='center', va='center',
                        color='white', fontweight='bold', fontsize=9)

    # --- Texto adicional opcional ---
    if show_text:
        plt.text(0.02, 0.3, '* Uma das instituições é composta por unidades de moradia',
                 color='red', ha='left', va='bottom',
                 transform=plt.gcf().transFigure, wrap=True)

    # --- Rotação dos rótulos ---
    if not is_horizontal:
        plt.xticks(rotation=xtick_rotation)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico salvo como imagem: {filename}")
    plt.show()