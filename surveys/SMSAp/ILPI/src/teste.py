def extrair_comp_fragilidade(df, nome_coluna_soma='soma_fragilidades'):
    """
    Filtra e retorna os dados de componentes de fragilidade,
    agrupados por institution_name, full_name, cpf.

    Parâmetros:
    - df: DataFrame.
    - fragilidade_dict: dict, mapeamento de código -> texto.
    - nome_coluna_soma: str, nome da coluna soma (Se None, usa 'soma_morbidities').

    Retorna:
    - DataFrame com as morbidades processadas, incluindo:
      - 'Componentes de Fragilidade': lista de morbidades binárias e textuais.
      - 'soma_morbidities': soma total de morbidades (binárias + textuais).
    """
    
    # # Preenche valores ausentes nas colunas-chave com o valor anterior (forward fill)
    campos_para_propagacao = ['institution_name', 'uuidv5', 'full_name']
    for campo in campos_para_propagacao:
        if campo in df.columns:
            df[campo] = df[campo].ffill()
        

    # Cria colunas de fragilidade binárias com base na lógica de interpretação de cada item
    df['frag_dependence_degree'] = df['dependence_degree'].apply(lambda x: 1 if x >= 2 else 0)
    df['frag_amount_weight_loss'] = df['amount_weight_loss'].apply(lambda x: 1 if x == 2 else 0)
    df['frag_elder_strenght'] = df['elder_strenght'].apply(lambda x: 1 if x == 1 else 0)
    df['frag_elder_hospitalized'] = df['elder_hospitalized'].apply(lambda x: 1 if x >= 2 else 0)
    df['frag_elder_difficulties'] = df['elder_difficulties'].apply(lambda x: 1 if x >= 2 else 0)
    df['frag_elder_mobility'] = df['elder_mobility'].apply(lambda x: 1 if x == 1 else 0)
    df['frag_basic_activities_diffic'] = df['basic_activities_diffic'].apply(lambda x: 1 if x == 1 else 0)
    df['frag_falls_number'] = df['falls_number'].apply(lambda x: 1 if x >= 2 else 0)

    # Lista das colunas binárias de fragilidade
    frag_cols = [
        'frag_dependence_degree',
        'frag_amount_weight_loss',
        'frag_elder_strenght',
        'frag_elder_hospitalized',
        'frag_elder_difficulties',
        'frag_elder_mobility',
        'frag_basic_activities_diffic',
        'frag_falls_number'
    ]

    # Mapeia nomes legíveis dos componentes de fragilidade
    descricao_frag = {
        'frag_dependence_degree': 'Grau dependência 2 ou 3',
        'frag_amount_weight_loss': 'Perda de peso > 3kg',
        'frag_elder_strenght': 'Fraqueza percebida',
        'frag_elder_hospitalized': 'Internação recente',
        'frag_elder_difficulties': 'Dificuldade ou incapacidade para levantar',
        'frag_elder_mobility': 'Caminhada mais lenta',
        'frag_basic_activities_diffic': 'Dificuldades em atividades diárias',
        'frag_falls_number': 'Quedas frequentes'
    }


    # Soma o total de fragilidades identificadas por linha
    df['soma_frag'] = df[frag_cols].sum(axis=1)

    # Gera uma descrição textual dos componentes de fragilidade presentes em cada linha
    def listar_componentes(row):
        return ', '.join([descricao_frag[col] for col in frag_cols if row[col] == 1])
    # Aplica a função acima a cada linha do DataFrame
    df['Componentes de Fragilidade'] = df.apply(listar_componentes, axis=1)

    # Função remove espaços extras e divide corretamente, evitando vírgulas sobrando
    def agrupar_componentes(lista):
        componentes = set()  # cria um conjunto vazio
        for item in lista:
            # Divide a string por vírgula, remove espaços e ignora valores vazios
            partes = [s.strip() for s in item.split(',') if s.strip()]
            # adiciona cada pedaço no conjunto
            for parte in partes:
                componentes.add(parte) 
        # converte o conjunto para lista e junta numa string separada por vírgula
        return ', '.join(sorted(componentes))

    # Agrupa os dados por indivíduo e instituição e resume os componentes e a soma
    resultado = df.groupby(['institution_name', 'full_name', 'cpf'], as_index=False).agg({
        'Componentes de Fragilidade': agrupar_componentes,
        'soma_frag': 'sum'
    })

    # Renomeia a coluna de soma, se for fornecido um nome alternativo
    resultado = resultado.rename(columns={
        'soma_frag': nome_coluna_soma
    })

    # Ordena os resultados por instituição, nome e CPF
    resultado = resultado.sort_values(by=['institution_name', 'full_name', 'cpf'])

    return resultado

# %%

# Extrai os componentes de fragilidade dos residentes
comp_fragilidade = extrair_comp_fragilidade(df)
comp_fragilidade


# %%

import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')

# %%

import pandas as pd


# %%
# ---------------------
# Leitura dos dados
# ---------------------
df = pd.read_csv("../../../../data/SMSAp/ILPI/base_perfil_epidemiologico.csv",
                 sep=";")
df.head()

def combinar_colunas_dict(df, combinacoes):
    """
    Cria novas colunas combinadas mantendo os valores originais das colunas de referência.
    Cada nova célula será um dicionário {coluna: valor}.
    """
    df_resultado = df.copy()

    for nova_col, cols in combinacoes.items():
        df_resultado[nova_col] = df_resultado[cols].apply(lambda row: row.to_dict(), axis=1)

    return df_resultado

combinacoes = {
    "mobilidade": [
        "elder_strenght",
        "elder_difficulties",
        "elder_mobility",
        "basic_activities_diffic",
        "falls_number"
    ]
}

df_novo = combinar_colunas_dict(df, combinacoes)

# %%
df_novo

# %%
def combinar_colunas_prefixo(df, combinacoes):
    """
    Cria colunas novas com prefixo da combinação, mantendo valores originais.
    Ex: mobilidade_elder_strenght, mobilidade_elder_difficulties, ...
    """
    df_resultado = df.copy()

    for nova_col, cols in combinacoes.items():
        for col in cols:
            df_resultado[f"{nova_col}_{col}"] = df_resultado[col]

    return df_resultado

df_novo = combinar_colunas_prefixo(df, combinacoes)
df_novo
# %%
