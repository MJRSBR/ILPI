# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')

import pandas as pd
from datetime import datetime 
# %%
# ---------------------
# Leitura dos dados
# ---------------------

df = pd.read_excel('../../../data/SMSAp/UPA/atendimento_upa_3x+.xlsx', sheet_name = 'tabela principal')
df

# %%
# ---------------------
# Extraindo variáveis de interesse
# ---------------------

columns = [['nm_cnes', 'dt_atend', 'cd_pac', 'nm_pac', 'tp_sexo_pac', 'dt_nasc_pac',
            'cd_munic', 'cd_cid', 'ds_cid']]

df_extr = df[columns[0]]
df_extr

# %%
# ---------------------
# Verificação tipo de variáveis e valores faltantes
# ---------------------
df_extr.info()
# %%

# ---------------------
# Alterando variáveis em datas para futuros cálculos
# ---------------------
df_date = df_extr.copy()
df_date['dt_atend'] = pd.to_datetime(df_date['dt_atend'], format='%Y%m%d')
df_date['dt_nasc_pac'] = pd.to_datetime(df_date['dt_nasc_pac'], format='%Y%m%d')
df_date

# %%
#from datetime import datetime
#from dateutil.relativedelta import relativedelta
#
## Data atual
#data_atual = datetime.today()
#
## Cálculo da idade
#df_date['idade'] = df_date['dt_nasc_pac'].apply(
#    lambda nasc: relativedelta(data_atual, nasc).years if pd.notnull(nasc) else None
#)
#df_date

# %%
# ---------------------
# Criando e calculando a coluna idade 
# ---------------------

# Data de hoje
hoje = datetime.today()

# Função para calcular idade
def calcular_idade(data_nasc):
    if pd.isnull(data_nasc):
        return None
    return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

# Aplica a função
df_date['idade'] = df_date['dt_nasc_pac'].apply(calcular_idade)
    
# %%
# Filtrar pacientes 60+

df_date =df_date[['nm_cnes', 'dt_atend', 'cd_pac', 'nm_pac', 'tp_sexo_pac', 
                  'idade', 'dt_nasc_pac','cd_munic', 'cd_cid', 'ds_cid']]
df_date
# %%
# Filtra pacientes 60+
maiores_60 = df_date[df_date['idade'] >= 60]

# Agrupa e conta atendimentos
emergencias_paciente = (
    maiores_60
    .groupby(['nm_cnes', 'dt_atend', 'nm_pac', 'idade', 'cd_munic', 'cd_cid'])
    .size()
    .reset_index(name='Numero atendimento')
    .sort_values(by='Numero atendimento', ascending=False)
)

emergencias_paciente

# %%
