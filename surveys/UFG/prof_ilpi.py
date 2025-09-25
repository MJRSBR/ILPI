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
df['institution_name'].rename('id_institution', inplace=True) 

# %%
# ---------------------
# PROFISSIONAIS
# ---------------------
# Lista de mapeamento dos profissionais e as colunas correspondentes
profissionais_mapping = [
    ('Aux.Enfermagem', 'nurse_aux', 'days_per_month_na'),
    ('Téc.Enfermagem', 'nurse_tech', 'days_per_month_nt'),
    ('Enfermeiro(a)', 'nurse', 'days_per_month_n'),
    ('Fisio', 'physiotherapist', 'days_per_month_physio'),
    ('Nutricionista', 'nutritionist', 'days_per_month_nutrit'),
    ('Psicologo(a)', 'psicologist', 'days_per_month_psicol'),
    ('Médico(a)', 'physician', 'days_per_month_physician'),
    ('Ter.Ocupacional', 'occup_therapist', 'days_per_month_occup'),
    ('Cuidador(a)', 'caregiver', 'days_per_month_caregiver'),
    ('Outros_prof_saúde', 'other_health_prof', 'd_p_month_oth_health_prof'),
    ('Serv.Gerais', 'housekeeping', 'days_per_month_housekeep'),
    ('Administrativo', 'staff', 'days_per_month_staff')
]

# Construir o DataFrame 
df_profissionais = pd.concat(
    [
        df[df[col] >= 1][['id_institution', days_col]]
        .assign(profissional=prof)
        .rename(columns={days_col: 'Dias_por_mes', 'id_institution': 'ILPI'})
        .assign(Dias_por_mes=lambda x: x['Dias_por_mes'].round(1))  # Corrigido aqui
        [['ILPI', 'profissional', 'Dias_por_mes']]
        for prof, col, days_col in profissionais_mapping
    ]
).dropna(subset=['Dias_por_mes']) # Remover valores nulos

# Ordenar os dados e resetar index
df_profissionais = df_profissionais.sort_values(by=['ILPI', 'profissional']).reset_index(drop=True)

# Visualizar o resultado
df_profissionais
# %%
# Salvando a tabela em /tables
salvar_tabela_como_imagem(
    df_profissionais,
    '../../UFG/tables/04_profissionais.png'
)

# %%
# Gráfico 04 - Profissionais nas ILPIs

plt.figure(figsize=(10, 6))
sns.barplot(x='profissional', y='Dias_por_mes', data=df_profissionais)
plt.xticks(rotation=45, ha='right') # Rotate x-axis labels for better readability
plt.text(0.02, 24.0,'* Uma das instituíções é composta por unidades de moradia',
         color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('Profissão')
plt.ylabel('Dias por Mês')
plt.title('Dias Trabalhados por Mês por Profissão')
plt.tight_layout()

plt.savefig('../../UFG/plots/04_profissionais.png')
plt.show()

# %%
#-------------------------------------------------------------
# VINCULO
# Criando e mapeando as colunas diretamente, com renomeação incluída para vinculo empregaticio

vinculo_empreg = (
    df[['id_institution', 'employment_relatioship___1', 'employment_relatioship___2', 'employment_relatioship___3']]
    .assign(
        Vinculo_empregaticio= (
            df['employment_relatioship___1'].map(lambda x: 'CLT' if x == 1 else '') +
            df['employment_relatioship___2'].map(lambda x: ', Contrato' if x == 1 else '') +
            df['employment_relatioship___3'].map(lambda x: ', Voluntário' if x == 1 else '')
        )
    )
    .assign(Vinculo_empregaticio=lambda x: x['Vinculo_empregaticio'].str.lstrip(', '))  # Limpa a vírgula extra no começo
    .rename(columns={'id_institution': 'ILPI'})  # Renomeando a coluna id_institution para ILPI
    [['ILPI', 'Vinculo_empregaticio']]  # Selecionando apenas as colunas desejadas
)

# Visualizando o DataFrame resultante
vinculo_empreg
# %%
# Salvando tabela em /tables
salvar_tabela_como_imagem(
    vinculo_empreg,
    '../../UFG/tables/05_vinculo_empreg.png'
)
# %%
# ---------------------
# Gráfico 05 - Vínculo Empregatício
# Tamanho da figura
plt.figure(figsize=(10, 6))

# Agrupar e plotar o gráfico de barras horizontais
vinculo_empreg.groupby('Vinculo_empregaticio').size().plot(
    kind='barh',
    color=sns.palettes.mpl_palette('Dark2')
)

# Ajustar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Garantir que o eixo X seja inteiro
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Título e rótulos
plt.title('Vínculo Empregatício dos Profissionais das ILPIs')
plt.text(1.4, 2.3,'* Uma das instituíções é composta por unidades de moradia',
         color='red',ha='left', va='bottom', wrap=True)
plt.xlabel('ILPIS')
plt.ylabel('Tipo de Vínculo')

# Exibir gráfico
plt.savefig("../../UFG/plots/05_vinculo_empreg.png")
plt.show()
# %%
# -------------
# Criando e mapeando as colunas diretamente, com renomeação incluída para 
# Plano/programa semanal de atividade física e reabilitação funcional

# Ajustar a exibição do pandas para mostrar mais caracteres
pd.set_option('display.max_colwidth', None)  # Permite exibir a coluna inteira

plano_reab = (
    df[["id_institution", "physio_program___1", "physio_program___2", "physio_program___3", "physio_program___4"]]
    .assign(
        plano_reabilitacao= (
            df["physio_program___1"].map(lambda x: 'melhoria do tônus muscular' if x == 1 else '') +
            df["physio_program___2"].map(lambda x: ', equilíbrio funcionalidade motora' if x == 1 else '') +
            df["physio_program___3"].map(lambda x: ', bem-estar geral com indicação do destinatário' if x == 1 else '') +
            df["physio_program___4"].map(lambda x: ', não existe plano' if x == 1 else '')
        )
    )
    .assign(plano_reabilitacao=lambda x: x['plano_reabilitacao'].str.lstrip(', '))  # Limpar vírgula no início da string
    .rename(columns={"id_institution": "ILPI"})  # Renomeando a coluna
    [["ILPI", "plano_reabilitacao"]]  # Selecionando apenas as colunas finais
)

# Visualizando o resultado
plano_reab
# %%
# Salvando tabela em /tables
salvar_tabela_como_imagem(
    plano_reab,
    '../../UFG/tables/06_plano_reabilit.png'
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
# ----------------------
# Gráfico 5 - Plano Reabilitação

plano_counts = plano_reab['plano_reabilitacao'].value_counts()

plot_barh(
    plano_counts,
    'Plano/programa semanal de atividade física e reabilitação funcional',
    'ILPIs',
    'planos',
    '../../UFG/plots/06_plano_terapeutico.png',
    obs=5

)
# %%
# ---------------------
# Criando e mapeando as colunas diretamente, com renomeação incluída para 
# Instruções do fisioterapeuta ao cuidador está documentada

instr_fisio = (df[['id_institution', 'physio_instructions']]
                        .assign(df_filtered=df['physio_instructions'].map({1: 'Sim', 2: 'Não'}))  # Mapeando 'residents_bedroom'
                        [['id_institution', 'df_filtered']]  # Selecionando as colunas necessárias
                        .rename(columns={'id_institution': 'ILPI', 'df_filtered': 'Instrucao_fisioterapeuta'})  # Renomeando as colunas
)

# Exibindo o resultado
instr_fisio
# %%
# Salvando tabela em /tables
salvar_tabela_como_imagem(
    instr_fisio,
    '../../UFG/tables/07_instr_fisio.png'
)
# %%
# ---------------------
# Gráfico 7 - Instruções do Fisioterapeuta
instr_counts = instr_fisio['Instrucao_fisioterapeuta'].value_counts()

plot_barh(
    instr_counts,
    'Instruções do fisioterapeuta ao cuidador está documentada?',
    'ILPIs',
    'instr',
    '../../UFG/plots/07_instrucao_fisioterapeuta.png'
)
# %%
