# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')

# %%

import re
import pandas as pd

from utils.utils import criar_diretorios
from funcoes.f_plot import plot_config 
from funcoes.f_process import criar_diretorios, extrair_morbidades
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
# ---------------------
df = pd.read_csv("../../../../data/SMSAp/ILPI/base_perfil_epidemiologico.csv",
                 sep=";")
df.head()
# %%
## --------------------
## ----- 11 - Morbidades
## --------------------
# Definindo um dicionário para morbidades binárias
morb_dict = {
    "morbidities___1" : "Hipertensão Arterial",
    "morbidities___2" : "Diabetes Mellitus",
    "morbidities___3" : "Hipercolesterolemia",
    "morbidities___4" : "Doença na coluna",
    "morbidities___5" : "Insuficiência cardíaco",
    "morbidities___6" : "Infarto",
    "morbidities___7" : "Insuficiência renal",
    "morbidities___8" : "Câncer",
    "morbidities___9" : "Enfisema pulmonar",
    "morbidities___10":	"Asma",
    "morbidities___11":	"Bronquite",
    "morbidities___12":	"Transtorno Mental",
    "morbidities___13":	"Osteoporose",
    "morbidities___14":	"Artrite",
    "morbidities___15":	"Demência",
    "morbidities___16":	"Alzheimer",
    "morbidities___17":	"Parkinson",
    "morbidities___18":	"Etilismo",
    "morbidities___19":	"Tabagismo",
    "morbidities___20":	"Usuário de drogas",
}

# %%

# ########

# def extrair_morbidades(df, morbidade_dict, nome_coluna_soma=None):
#     """
#     Filtra e retorna os dados de morbidades legíveis, agrupados por institution_name, full_name, cpf.
#     A coluna 'other_morbidities' é normalizada (minúsculas, sem espaços),
#     separando múltiplas entradas por vírgula, ponto e vírgula ou barra vertical.
#     Soma final inclui morbidades binárias + textuais distintas.

#     Parâmetros:
#     - df: DataFrame.
#     - morbidade_dict: dict, mapeamento de código -> texto.
#     - nome_coluna_soma: str, nome da coluna soma (Se None, usa 'soma_morbidities').

#     Retorna:
#     - DataFrame com as morbidades processadas, incluindo:
#       - 'Morbidades': lista de morbidades binárias e textuais.
#       - 'other_morbidities': morbidades textuais normalizadas.
#       - 'soma_morbidities': soma total de morbidades (binárias + textuais).
#     """
    
#     morbidities_cols = list(morbidade_dict.keys())
#     campos_para_propagacao = ['id_institution', 'uuidv5','full_name', 'elder_age']  # Incluir 'elder_age'
    
#     # Propaga os campos chave
#     for campo in campos_para_propagacao:
#         df[campo] = df[campo].ffill()

#     # Inclui linhas que tenham morbidades binárias OU outras textuais
#     df_filtrado = df[df[morbidities_cols].eq(1).any(axis=1) | df['other_morbidities'].notna()].copy()

#     if nome_coluna_soma is None:
#         nome_coluna_soma = 'soma_morbidities'

#     # Soma das morbidades binárias
#     df_filtrado['soma_binarias'] = df_filtrado[morbidities_cols].sum(axis=1, numeric_only=True)

#     def nomes_morbidades(row):
#         return ', '.join([morbidade_dict[col] for col in morbidities_cols if row.get(col) == 1])

#     df_filtrado['Morbidades'] = df_filtrado.apply(nomes_morbidades, axis=1)

#     # Padroniza a coluna 'other_morbidities' (primeira letra maiúscula)
#     df_filtrado['other_morbidities'] = (
#         df_filtrado['other_morbidities']
#         .astype(str)  # Garante que todos os valores sejam strings
#         .str.lower()  # Coloca em minúsculas
#         .replace('nan', '')  # Remove 'nan' (caso existam valores inválidos)
#         .str.strip()  # Remove espaços extras
#         .str.capitalize()  # Coloca a primeira letra maiúscula
#     )
    
#     # Remove qualquer vírgula extra no início ou no final
#     df_filtrado['other_morbidities'] = df_filtrado['other_morbidities'].str.lstrip(', ').str.rstrip(', ')

#     # Função para contar morbidades textuais
#     def contar_textuais(texto):
#         if not texto:
#             return 0
        
#         # Substitui " e " (com espaços) por vírgula para separar corretamente as palavras
#         texto = re.sub(r'\s+e\s+', ', ', texto)
        
#         # Substitui ponto e vírgula por vírgula
#         texto = texto.replace(';', ',')
        
#         # Divide a string usando vírgula, ponto e vírgula ou barra vertical como separadores
#         itens = re.split(r'[;,|]', texto)
        
#         # Remove espaços extras e conta as palavras
#         itens = [item.strip() for item in itens if item.strip()]
        
#         return len(itens)

#     # Aplica a função para contar as morbidades textuais
#     df_filtrado['soma_other'] = df_filtrado['other_morbidities'].apply(contar_textuais)
    
#     # Soma final das morbidades (binárias + textuais)
#     df_filtrado[nome_coluna_soma] = df_filtrado['soma_binarias'] + df_filtrado['soma_other']
    
#     # Converte para int64 para garantir que a coluna soma seja do tipo inteiro
#     df_filtrado[nome_coluna_soma] = df_filtrado[nome_coluna_soma].fillna(0).astype('int64')

#     # Limpa colunas auxiliares
#     df_filtrado = df_filtrado.drop(columns=['soma_binarias', 'soma_other'])

#     # Agrupamento
#     df_resultado = df_filtrado.groupby(['id_institution', 'uuidv5', 'full_name'], as_index=False).agg({
#         'Morbidades': lambda x: ', '.join(sorted(set(', '.join(x).split(', ')))),
#         'other_morbidities': lambda x: ', '.join(sorted(set(filter(None, map(str.strip, x))))),
#         nome_coluna_soma: 'sum',  # Usando a soma do campo 'soma_morbidities' customizado
#         'elder_age': 'first'  # Garantir que 'elder_age' seja agregada
#     })

#     # Converte 'elder_age' para int64
#     df_resultado['elder_age'] = df_resultado['elder_age'].fillna(0).astype('int64')

#     # Ordena as colunas conforme solicitado
#     df_resultado = df_resultado[['id_institution', 'uuidv5', 'full_name', 'elder_age', 'Morbidades', 'other_morbidities', nome_coluna_soma]]

#     # Organiza as linhas
#     df_resultado = df_resultado.sort_values(by=['id_institution', 'uuidv5', 'full_name'])

#     return df_resultado


# Extraindo morbidades, outras morbidades e soma
df_morbidades = extrair_morbidades(df, morb_dict)

df_morbidades
# %%

### VERIFICAR NECESSIDADE
# Cria a tabela Morbidade Residentes para data lake
morbidades_residentes = df_morbidades[['institution_name', 'cpf', 'Morbidades', 'other_morbidities', 'soma_morbidities']]

# Salva tabela
morbidades_residentes.to_csv('../../../../data/SMSAp/Lake/Morbidades.csv')