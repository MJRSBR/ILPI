# %%
import pandas as pd
# %%
# ---------------------
# Leitura dos dados
# ---------------------
df = pd.read_csv('../../../data/SMSAp/Internacao/dados_internacoes_60+.csv')
df
# %%
# ---------------------
# Extraindo variáveis de interesse
# ---------------------

columns = [['COMPET.', 'DT. EMISSÃO', 'DT INTERN', 'DT. SAIDE', 'DIAG PRINCIPAL', 'NOME DO PACIENTE', 
            'IDADE', 'SEXO', 'TIPO LOGRA.', 'LOGRADOURO PACIENTE', 'BAIRRO', 'IBGE PACIENTE', 'EST.', 
            'CEP', 'NUMEROS AIH', 'AIH_', 'MOT SAIDA', 'MEDICO SOLICITANTE']]

df_extr = df[columns[0]]
df_extr

# %%
# ---------------------
# Extraindo maiores prevalencias de diagnósticos
# ---------------------
# Agrupa por 'DIAG PRINCIPAL', usa .size() para contar quantas vezes cada raça aparece e
# renomeia a coluna de contagem para 'Total'
diag_geral = (df_extr
              .groupby(['DIAG PRINCIPAL'])
              .size()
              .reset_index(name='Total')
              .sort_values(ascending=False, by='Total')
)
diag_geral.head(20)
# %%
diag_geral.shape
# %%
# Priorizando os diagnósticos com mais de 20 pacientes
diag_geral.loc[diag_geral['Total'] >= 20]
# %%
# ---------------------
# Extraindo maiores prevalencias de diagnósticos por paciente 
# ---------------------

diag_pacient = (df_extr
                .groupby(['NOME DO PACIENTE', 'IDADE', 'DIAG PRINCIPAL'])
                .size()
                .reset_index(name='Total')
                .sort_values(ascending=False, by='Total')
)
diag_pacient.head(20)
# %%
diag_pacient.shape
# %%
# Priorizando os pacientes com mais de 3 internações
diag_pacient.loc[diag_pacient['Total'] >= 3].shape
# %%
