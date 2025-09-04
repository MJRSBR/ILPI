# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')

import pandas as pd
# %%
# ---------------------
# Leitura dos dados
# ---------------------

df = pd.read_excel('../../../data/SMSAp/Internacao/superutilizados_internacoes.xlsx', sheet_name = 'BANCO DE DADOS SIHD GERAL 2024')
df
# %%
# ---------------------
# Verificação tipo de variáveis e valores faltantes
# ---------------------
df.info()

# %%
# ---------------------
# Alterando variáveis em datas para futuros cálculos
# ---------------------
df_date = df.copy()
df_date['COMPET.'] = pd.to_datetime(df_date['COMPET.'], format='%Y%m')
df_date['DT. EMISSÃO'] = pd.to_datetime(df_date['DT. EMISSÃO'], format='%Y%m%d')
df_date['DT INTERN'] = pd.to_datetime(df_date['DT INTERN'], format='%Y%m%d')
df_date['DT. SAIDE'] = pd.to_datetime(df_date['DT. SAIDE'], format='%Y%m%d')
df_date['DT. NASC.'] = pd.to_datetime(df_date['DT. NASC.'], format='%Y%m%d')
df_date
# %%
# ---------------------
# Filtrando pacientes com mais de 60 anos
# ---------------------
df_60= df_date[df_date['IDADE'] >= 60] 
df_60
# %%
# ---------------------
# Gerando arquivo .csv para futuras análises
# ---------------------

df_60.to_csv('../../../data/SMSAp/Internacao/dados_internacoes_60+.csv')
# %%
