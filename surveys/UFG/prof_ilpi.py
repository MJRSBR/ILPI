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
        .assign(Dias_por_mes=lambda x: x['Dias_por_mes'].round(1))  
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

vinculo_cols = {
    'employment_relatioship___1': 'CLT',
    'employment_relatioship___2': 'Contrato',
    'employment_relatioship___3': 'Voluntário'
}
vinculo_empreg = processa_multiresposta(df, vinculo_cols, 'Vinculo_empregaticio')
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
plt.xlabel('Número de ILPIs')
plt.ylabel('Tipo de Vínculo')

# Exibir gráfico
plt.savefig("../../UFG/plots/05_vinculo_empreg.png")
plt.show()
# %%
## --- Plano de Reabilitação
plano_cols = {
    'physio_program___1': 'Melhoria do tônus muscular',
    'physio_program___2': 'Equilíbrio funcionalidade motora',
    'physio_program___3': 'Bem-estar geral com indicação do destinatário',
    'physio_program___4': 'Não existe plano'
}
plano_reab = processa_multiresposta(df, plano_cols, 'Plano_Reabilitacao')
plano_reab
# %%
# Salvando tabela em /tables
salvar_tabela_como_imagem(
    plano_reab,
    '../../UFG/tables/06_plano_reabilit.png'
)
# %%
# ----------------------
# Gráfico 6 - Plano Reabilitação

plano_counts = plano_reab['Plano_Reabilitacao'].value_counts()

plot_barh(
    plano_counts,
    'Plano/programa semanal de atividade física e reabilitação funcional',
    'Número de ILPIs',
    'planos',
    '../../UFG/plots/06_plano_terapeutico.png',
    obs=5

)
# %%
# ---------------------
# Criando e mapeando as colunas diretamente, com renomeação incluída para 
# Instruções do fisioterapeuta ao cuidador está documentada

instr_fisio = processa_binario(
    df, 
    'physio_instructions', 
    'Instrucao_fisioterapeuta', 
    {1: 'Sim', 2: 'Não'}
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
    'Número de ILPIs',
    'instr',
    '../../UFG/plots/07_instrucao_fisioterapeuta.png'
)
# %%
