import pandas as pd
import numpy as np

def criar_diretorios():
    import os
    os.makedirs('../tables', exist_ok=True)
    os.makedirs('../plots', exist_ok=True)
    os.makedirs('../../../../data/SMSAp/Lake', exist_ok=True)


# ------------------------------
# Funções processamento
# ------------------------------

# ----------------------------------------
def processa_multiresposta(df, colunas_dict, legenda):
    
    """
    Processa variáveis de múltiplas respostas (checkbox), criando uma nova coluna com
    descrições combinadas, e remove linhas sem nenhuma seleção.

    Parâmetros:
    -----------
    df : pd.DataFrame
        O DataFrame contendo os dados originais com variáveis de múltiplas respostas.
    colunas_dict : dict
        Um dicionário onde as chaves são nomes de colunas de checkbox e os valores são
        as descrições associadas a cada resposta.
    legenda : str
        Nome da nova coluna que irá conter a descrição concatenada das respostas.

    Retorno:
    --------
    pd.DataFrame
        Um novo DataFrame com as colunas 'ILPI' e a nova coluna de legenda,
        sem linhas onde nenhuma resposta foi marcada (ou seja, todas eram 0).
    """

    # Cria nova coluna com as descrições concatenadas
    df[legenda] = df.apply(
        lambda row: ', '.join(
            [desc for col, desc in colunas_dict.items() if row.get(col) == 1]
        ) if any(row.get(col) == 1 for col in colunas_dict) else np.nan,
        axis=1
    )

    # Seleciona apenas as colunas relevantes
    resultado = df[['institution_name', legenda]].rename(columns={'institution_name': 'ILPI'})

    # Remove linhas onde a nova coluna é NaN
    resultado = resultado.dropna(subset=[legenda])

    return resultado

# ----------------------------------------

#def extrair_morbidades(df, morbidade_dict, nome_coluna_soma=None):
#    import re
#    import numpy as np
#    
#    """
#    Filtra e retorna os dados de morbidades legíveis,
#    agrupados por institution_name, full_name, cpf.
#    A coluna 'other_morbidities' é normalizada (minúsculas, sem espaços),
#    separando múltiplas entradas por vírgula, ponto e vírgula ou barra vertical.
#    Soma final inclui morbidades binárias + textuais distintas.#

#    Parâmetros:
#    - df: DataFrame.
#    - morbidade_dict: dict, mapeamento de código -> texto.
#    - nome_coluna_soma: str, nome da coluna soma (Se None, usa 'soma_morbidities').#

#    Retorna:
#    - DataFrame com as morbidades processadas, incluindo:
#      - 'Morbidades': lista de morbidades binárias e textuais.
#      - 'other_morbidities': morbidades textuais normalizadas.
#      - 'soma_morbidities': soma total de morbidades (binárias + textuais).
#    """#

#    morbidities_cols = list(morbidade_dict.keys())
#    #df[morbidities_cols] = df[morbidities_cols].apply(pd.to_numeric, errors='coerce')#

#    # Preenche campos chave para propagação de dados
#    campos_para_propagacao = ['institution_name', 'full_name', 'cpf', 'elder_age']  
#    for campo in campos_para_propagacao:
#        df[campo] = df[campo].ffill()#

#    # Inclui linhas que tenham morbidades binárias OU outras textuais
#    df_filtrado = df[df[morbidities_cols].eq(1).any(axis=1) | df['other_morbidities'].notna()].copy()#

#    if nome_coluna_soma is None:
#        nome_coluna_soma = 'soma_morbidities'#

#    # Soma das morbidades binárias
#    df_filtrado['soma_binarias'] = df_filtrado[morbidities_cols].sum(axis=1, numeric_only=True)#

#    def nomes_morbidades(row):
#        return ', '.join([morbidade_dict[col] for col in morbidities_cols if row.get(col) == 1])#

#    df_filtrado['Morbidades'] = df_filtrado.apply(nomes_morbidades, axis=1)#

#    # Padroniza a coluna 'other_morbidities' 
#    df_filtrado['other_morbidities'] = (
#        df_filtrado['other_morbidities']
#        .astype(str)  # Garante que todos os valores sejam strings
#        .str.lower()  # Coloca em minúsculas
#        .replace('nan', '')  # Remove 'nan' (caso existam valores inválidos)
#        .str.strip()  # Remove espaços extras
#        .str.capitalize()  # Coloca a primeira letra maiúscula
#    )#

#    # Agrupamento
#    df_resultado = df_filtrado.groupby(['institution_name', 'full_name', 'cpf'], as_index=False).agg({
#        'Morbidades': lambda x: ', '.join(sorted(set(', '.join(x).split(', ')))),
#        'other_morbidities': lambda x: ', '.join(sorted(set(filter(None, map(str.strip, x))))),
#        'soma_binarias': 'sum',
#        'elder_age': 'first'  # Garantir que 'elder_age' seja agregada
#    })#

#    # Conta as morbidades textuais, com separadores: , ; |
#    def contar_textuais(texto):
#        if not texto:
#            return 0
#        # Remove qualquer vírgula extra no início ou no final do texto pela função lstrip(', ') 
#        texto = texto.lstrip(', ').rstrip(', ')
#        # Divide o texto por vírgula, ponto e vírgula ou barra vertical
#        itens = re.split(r'[;,|]', texto)
#        return len([item.strip() for item in itens if item.strip()])#

#    df_resultado['soma_other'] = df_resultado['other_morbidities'].apply(contar_textuais)
#    df_resultado[nome_coluna_soma] = df_resultado['soma_binarias'] + df_resultado['soma_other']#

#    # Limpa colunas auxiliares
#    df_resultado = df_resultado.drop(columns=['soma_binarias', 'soma_other'])#

#    # Adiciona a coluna idade
#    df_resultado = df_resultado[['institution_name', 'full_name', 'elder_age', 'cpf', 'Morbidades', 'other_morbidities', nome_coluna_soma]]#

#    # Organiza as linhas
#    df_resultado = df_resultado.sort_values(by=['institution_name', 'full_name', 'cpf'])#

#    return df_resultado

def extrair_morbidades(df, morbidade_dict, nome_coluna_soma=None):
    """
    Filtra e retorna os dados de morbidades legíveis, agrupados por institution_name, full_name, cpf.
    A coluna 'other_morbidities' é normalizada (minúsculas, sem espaços),
    separando múltiplas entradas por vírgula, ponto e vírgula ou barra vertical.
    Soma final inclui morbidades binárias + textuais distintas.

    Parâmetros:
    - df: DataFrame.
    - morbidade_dict: dict, mapeamento de código -> texto.
    - nome_coluna_soma: str, nome da coluna soma (Se None, usa 'soma_morbidities').

    Retorna:
    - DataFrame com as morbidades processadas, incluindo:
      - 'Morbidades': lista de morbidades binárias e textuais.
      - 'other_morbidities': morbidades textuais normalizadas.
      - 'soma_morbidities': soma total de morbidades (binárias + textuais).
    """
    
    morbidities_cols = list(morbidade_dict.keys())
    campos_para_propagacao = ['institution_name', 'full_name', 'cpf', 'elder_age']  # Incluir 'elder_age'
    
    # Propaga os campos chave
    for campo in campos_para_propagacao:
        df[campo] = df[campo].ffill()

    # Inclui linhas que tenham morbidades binárias OU outras textuais
    df_filtrado = df[df[morbidities_cols].eq(1).any(axis=1) | df['other_morbidities'].notna()].copy()

    if nome_coluna_soma is None:
        nome_coluna_soma = 'soma_morbidities'

    # Soma das morbidades binárias
    df_filtrado['soma_binarias'] = df_filtrado[morbidities_cols].sum(axis=1, numeric_only=True)

    def nomes_morbidades(row):
        return ', '.join([morbidade_dict[col] for col in morbidities_cols if row.get(col) == 1])

    df_filtrado['Morbidades'] = df_filtrado.apply(nomes_morbidades, axis=1)

    # Padroniza a coluna 'other_morbidities' (primeira letra maiúscula)
    df_filtrado['other_morbidities'] = (
        df_filtrado['other_morbidities']
        .astype(str)  # Garante que todos os valores sejam strings
        .str.lower()  # Coloca em minúsculas
        .replace('nan', '')  # Remove 'nan' (caso existam valores inválidos)
        .str.strip()  # Remove espaços extras
        .str.capitalize()  # Coloca a primeira letra maiúscula
    )
    
    # Remove qualquer vírgula extra no início ou no final
    df_filtrado['other_morbidities'] = df_filtrado['other_morbidities'].str.lstrip(', ').str.rstrip(', ')

    # Função para contar morbidades textuais
    def contar_textuais(texto):
        if not texto:
            return 0
        
        # Substitui " e " (com espaços) por vírgula para separar corretamente as palavras
        texto = re.sub(r'\s+e\s+', ', ', texto)
        
        # Substitui ponto e vírgula por vírgula
        texto = texto.replace(';', ',')
        
        # Divide a string usando vírgula, ponto e vírgula ou barra vertical como separadores
        itens = re.split(r'[;,|]', texto)
        
        # Remove espaços extras e conta as palavras
        itens = [item.strip() for item in itens if item.strip()]
        
        return len(itens)

    # Aplica a função para contar as morbidades textuais
    df_filtrado['soma_other'] = df_filtrado['other_morbidities'].apply(contar_textuais)
    
    # Soma final das morbidades (binárias + textuais)
    df_filtrado[nome_coluna_soma] = df_filtrado['soma_binarias'] + df_filtrado['soma_other']
    
    # Converte para int64 para garantir que a coluna soma seja do tipo inteiro
    df_filtrado[nome_coluna_soma] = df_filtrado[nome_coluna_soma].fillna(0).astype('int64')

    # Limpa colunas auxiliares
    df_filtrado = df_filtrado.drop(columns=['soma_binarias', 'soma_other'])

    # Agrupamento
    df_resultado = df_filtrado.groupby(['institution_name', 'full_name', 'cpf'], as_index=False).agg({
        'Morbidades': lambda x: ', '.join(sorted(set(', '.join(x).split(', ')))),
        'other_morbidities': lambda x: ', '.join(sorted(set(filter(None, map(str.strip, x))))),
        nome_coluna_soma: 'sum',  # Usando a soma do campo 'soma_morbidities' customizado
        'elder_age': 'first'  # Garantir que 'elder_age' seja agregada
    })

    # Converte 'elder_age' para int64
    df_resultado['elder_age'] = df_resultado['elder_age'].fillna(0).astype('int64')

    # Ordena as colunas conforme solicitado
    df_resultado = df_resultado[['institution_name', 'full_name', 'elder_age', 'cpf', 'Morbidades', 'other_morbidities', nome_coluna_soma]]

    # Organiza as linhas
    df_resultado = df_resultado.sort_values(by=['institution_name', 'full_name', 'cpf'])

    return df_resultado

# ----------------------------------------

def extrair_medicamentos(df):
    import pandas as pd
    """
    Extrai os medicamentos usados por residente, incluindo combinações, com colunas:
    med_name, dosage, taken_daily. Cada linha representa 1 medicamento.
    """
    tomadas_dia = {
        "1": "1 x ao dia",
        "2": "2 x ao dia",
        "3": "3 x ao dia",
        "4": "4 x ao dia",
        "5": "semanalmente",
        "6": "mensalmente",
        "7": "quinzenalmente"
    }

    # Filtra apenas registros do instrumento medicamentos_em_uso
    df_meds = df[df['redcap_repeat_instrument'] == 'medicamentos_em_uso'].copy()

    # Propaga os campos-chave
    campos_chave = ['institution_name', 'full_name', 'cpf']
    for campo in campos_chave:
        if df_meds[campo].dtype == object:
            df_meds[campo] = df_meds[campo].ffill().str.upper()
        else:
            df_meds[campo] = df_meds[campo].ffill()

    registros = []

    for _, row in df_meds.iterrows():
        base_info = {
            'institution_name': row['institution_name'],
            'full_name': row['full_name'],
            'cpf': row['cpf']
        }

        # Medicamento principal
        med_name = str(row.get('med_name')).strip().lower() if pd.notnull(row.get('med_name')) else None
        if med_name:
            valor_bruto = row.get('taken_daily')
            taken_daily = None
            if pd.notnull(valor_bruto):
                chave = str(int(valor_bruto)) if not isinstance(valor_bruto, str) else valor_bruto.strip()
                taken_daily = tomadas_dia.get(chave)

            registros.append({
                **base_info,
                'med_name': med_name,
                'dosage': row.get('dosage'),
                'taken_daily': taken_daily
            })

        # Combinações
        for i in range(1, 7):
            comb_col = f'combination_{i}'
            dose_col = f'combination_dosage_{i}'

            comb_value = row.get(comb_col)
            if pd.notnull(comb_value) and str(comb_value).strip():
                registros.append({
                    **base_info,
                    'med_name': str(comb_value).strip().lower(),
                    'dosage': row.get(dose_col),
                    'taken_daily': None
                })

    # Cria DataFrame final
    df_resultado = pd.DataFrame(registros)

    # Ordena para melhor leitura
    df_resultado = df_resultado.sort_values(by=['institution_name', 'full_name', 'cpf'])

    # Renomear colunas
    df_resultado = df_resultado.rename(columns={
        "institution_name": "ILPI",
        "full_name": "Nome Completo",	
        "cpf": "CPF",	
        "med_name": "Medicamento",	
        "dosage": "Dose",	
        "taken_daily": "Tomadas ao dia"
    })

    return df_resultado

# ----------------------------------------

def classificar_risco(df, condicoes_critico, condicoes_alerta, condicoes_atencao, incluir_sem_risco=True):
    """
    Aplica condições de risco e retorna:
    - DataFrame agrupado por 'cpf' com colunas: institution_name, cpf, full_name, risco (colorido em HTML)
    - Resumo com contagem por nível de risco (rótulos limpos, sem HTML)
   
     Parâmetros:
    - df: DataFrame original
    - condicoes_critico, condicoes_alerta, condicoes_atencao: dicionários de condições
    
    - incluir_sem_risco: se True, classifica como 'Sem Risco' os registros que não se encaixam em nenhuma categoria
    OBS: Para visualizar cores no Jupyter, usar `display(HTML(resultado.to_html(escape=False)))`
    """

    df_copia = df.copy()

    df_copia['risco'] = None

    cores_por_risco = {
        'Crítico': 'red',
        'Alerta': 'orange',
        'Atenção': 'yellow',
        'Sem Risco': 'green'
    }

    def aplicar_classificacao(df_local, condicoes_dict, label):
        cond = pd.Series(True, index=df_local.index)
        for col, func in condicoes_dict.items():
            cond &= df_local[col].apply(func)
        return cond.replace({True: label, False: None})

    for condicoes, label in [
        (condicoes_critico, 'Crítico'),
        (condicoes_alerta, 'Alerta'),
        (condicoes_atencao, 'Atenção')
    ]:
        mask = aplicar_classificacao(df_copia, condicoes, label)
        condicao_vazia = df_copia['risco'].isna()
        df_copia.loc[mask.notna() & condicao_vazia, 'risco'] = label

    # Preencher com "Sem Risco", se solicitado
    if incluir_sem_risco:
        df_copia.loc[df_copia['risco'].isna(), 'risco'] = 'Sem Risco'

    # Define a ordem de severidade
    ordem_prioridade = {'Crítico': 0, 'Alerta': 1, 'Atenção': 2, 'Sem Risco': 3}
    df_copia['prioridade'] = df_copia['risco'].map(ordem_prioridade)

    agrupado = (
        df_copia
        .sort_values('prioridade')
        .groupby('cpf', as_index=False)
        .first()[['institution_name', 'cpf', 'full_name', 'risco']]
    )

    # Aplica cor HTML na coluna 'risco'
    def colorir(valor):
        cor = cores_por_risco.get(valor, 'black')
        return f'<span style="color: {cor}; font-weight: bold;">{valor}</span>'

    agrupado['Score_Fragilidade'] = agrupado['risco'].apply(colorir)

    # Resumo por grupo de risco
    resumo = (
        agrupado
        .groupby(['institution_name', 'risco'], as_index=False)
        .size()
        .rename(columns={'size': 'total'})
    )

    return agrupado.drop(columns=['risco']), resumo
