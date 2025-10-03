import pandas as pd
import numpy as np
import os
import re

# ------------------------------
# Funções processamento
# ------------------------------

def processa_binario(df, coluna, legenda, rename_dict):
    """
    Processa variáveis binárias para análise.

    Parâmetros:
    - df: Data Frame
    - coluna: coluna da variável
    - legenda: str, nome da nova coluna de saída
    - rename_dict: dict, ex: {1: 'Sim', 0: 'Não'}
    
    Exemplo de uso:
    tabela_camas = processa_binario(
        df,
        'residents_bedroom',
        'Camas segundo a Norma',
        rename_dict)
    """
    temp = (df[['id_institution', coluna]]
                # Cria uma coluna cujo nome é o valor da variável legenda 
                # populacionando com o mapeamento
                .assign(**{legenda: df[coluna].map(rename_dict)}) 
                .rename(columns={'id_institution': 'ILPI'})
                .drop(columns=coluna)
                )
    return temp

# ----------------------------------------

def processa_uma_variavel_com_opcoes(df, coluna_original, nome_saida, mapa_valores):
    """
    Processa códigos inteiros para uma string descritiva (concatenada) com base em um dicionário de mapeamento.

    Parâmetros:
    - df: DataFrame original.
    - coluna_original: str, nome da coluna com códigos.
    - nome_saida: str, nome da nova coluna de saída.
    - mapa_valores: dict, mapeamento de código -> texto.

    Retorna:
    - DataFrame com 'ILPI' e a nova coluna.
    """
    temp = df[["id_institution", coluna_original]].copy()
    
    # Concatena textos com base nos valores
    def construir_texto(valor):
        partes = [txt for cod, txt in mapa_valores.items() if valor == cod]
        return ', '.join(partes) if partes else 'Não informado'
    
    temp[nome_saida] = temp[coluna_original].map(construir_texto)
    temp = temp.rename(columns={"id_institution": "ILPI"})[["ILPI", nome_saida]]
    
    return temp

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
    resultado = df[['id_institution', legenda]].rename(columns={'id_institution': 'ILPI'})

    # Remove linhas onde a nova coluna é NaN
    resultado = resultado.dropna(subset=[legenda])

    return resultado

# ----------------------------------------

def criar_df_com_soma_por_prefixo(df, prefixo, nome_coluna_soma=None):
    """
    Retorna um novo DataFrame com as colunas que começam com o prefixo e uma coluna de soma.

    Parâmetros:
    - df: DataFrame original.
    - prefixo: Prefixo das colunas a incluir.
    - nome_coluna_soma: Nome da nova coluna de soma. Se None, será 'soma_' + prefixo.

    Retorna:
    - Novo DataFrame com as colunas selecionadas + coluna de soma.
    """
    # Filtra colunas com o prefixo
    colunas = [col for col in df.columns if col.startswith(prefixo)]

    # Garante que os dados sejam numéricos
    df_filtrado = df[colunas].apply(pd.to_numeric, errors='coerce')

    # Nome da nova coluna de soma
    if nome_coluna_soma is None:
        nome_coluna_soma = f'soma_{prefixo.rstrip("_")}'

    # Adiciona a soma por linha
    df_filtrado[nome_coluna_soma] = df_filtrado.sum(axis=1, numeric_only=True)

    return df_filtrado


# ---------------------------------------


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
    campos_para_propagacao = ['id_institution', 'uuidv5','full_name', 'elder_age']  # Incluir 'elder_age'
    
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
    df_resultado = df_filtrado.groupby(['id_institution', 'uuidv5', 'full_name'], as_index=False).agg({
        'Morbidades': lambda x: ', '.join(sorted(set(', '.join(x).split(', ')))),
        'other_morbidities': lambda x: ', '.join(sorted(set(filter(None, map(str.strip, x))))),
        nome_coluna_soma: 'sum',  # Usando a soma do campo 'soma_morbidities' customizado
        'elder_age': 'first'  # Garantir que 'elder_age' seja agregada
    })

    # Converte 'elder_age' para int64
    df_resultado['elder_age'] = df_resultado['elder_age'].fillna(0).astype('int64')

    # Ordena as colunas conforme solicitado
    df_resultado = df_resultado[['id_institution', 'uuidv5', 'full_name', 'elder_age', 'Morbidades', 'other_morbidities', nome_coluna_soma]]

    # Organiza as linhas
    df_resultado = df_resultado.sort_values(by=['id_institution', 'uuidv5', 'full_name'])

    return df_resultado


# ----------------------------------------


def extrair_medicamentos(df):
    """
    Extrai os medicamentos usados por residentes, com base no instrumento repetido 'medicamentos_em_uso'.
    Retorna um DataFrame com colunas: id_institution, full_name, uuidv5, med_name, dosage, taken_daily.

    Regras:
    - Mantém medicamentos principais (med_name) e combinações (combination_1 a combination_6).
    - Ignora entradas vazias ou inválidas.
    - Propaga corretamente os campos-chave com ordenação antes do ffill.
    """

    # Mapeamento de códigos para frequências
    tomadas_dia = {
        "1": "1 x ao dia",
        "2": "2 x ao dia",
        "3": "3 x ao dia",
        "4": "4 x ao dia",
        "5": "semanalmente",
        "6": "mensalmente",
        "7": "quinzenalmente"
    }

    # 1. Filtra apenas o instrumento de medicamentos
    df_meds = df[df['redcap_repeat_instrument'] == 'medicamentos_em_uso'].copy()

    # 2. Ordena por record_id e instância para garantir consistência no ffill
    df_meds = df_meds.sort_values(by=['record_id', 'redcap_repeat_instance'])

    # 3. Propaga campos-chave corretamente
    campos_chave = ['id_institution', 'uuidv5', 'full_name']
    for campo in campos_chave:
        if df_meds[campo].dtype == object:
            df_meds[campo] = df_meds[campo].ffill().str.upper()
        else:
            df_meds[campo] = df_meds[campo].ffill()

    # Lista para armazenar os registros extraídos
    registros = []

    # Set para rastrear os record_ids encontrados
    record_ids_extraidos = set()

    # 4. Loop por linha
    for _, row in df_meds.iterrows():
        base_info = {
            'id_institution': row['id_institution'],
            'uuidv5': row['uuidv5'],
            'full_name': row['full_name'],
            
        }

        record_id = row['record_id']
        has_valid_med = False  # Flag para rastrear se pelo menos 1 med foi extraído

        # --- Medicamento principal ---
        raw_med_name = row.get('med_name')
        if pd.notnull(raw_med_name):
            med_name = str(raw_med_name).strip().lower()
            if med_name and med_name != 'nan':
                # Extrai frequência
                raw_freq = row.get('taken_daily')
                taken_daily = None
                if pd.notnull(raw_freq):
                    chave = str(int(raw_freq)) if not isinstance(raw_freq, str) else raw_freq.strip()
                    taken_daily = tomadas_dia.get(chave)

                registros.append({
                    **base_info,
                    'med_name': med_name,
                    'dosage': row.get('dosage'),
                    'taken_daily': taken_daily
                })
                has_valid_med = True

        # --- Combinações ---
        for i in range(1, 7):
            comb_col = f'combination_{i}'
            dose_col = f'combination_dosage_{i}'
            comb_value = row.get(comb_col)

            if pd.notnull(comb_value) and str(comb_value).strip().lower() not in ['', 'nan']:
                registros.append({
                    **base_info,
                    'med_name': str(comb_value).strip().lower(),
                    'dosage': row.get(dose_col),
                    'taken_daily': None  # sem frequência para combinações
                })
                has_valid_med = True

        # Marca o record_id apenas se encontrou algum medicamento
        if has_valid_med:
            record_ids_extraidos.add(record_id)

    # 5. Cria DataFrame final
    df_resultado = pd.DataFrame(registros)

    # Ordena para melhor leitura
    df_resultado = df_resultado.sort_values(by=['id_institution', 'uuidv5', 'full_name'])
    df_resultado['uuidv5'] = df_resultado['uuidv5'].str.lower()
    # 6. Log final
    print("🔍 Estatísticas da extração:")
    total_record_ids = df[df['redcap_repeat_instrument'] == 'medicamentos_em_uso']['record_id'].nunique()
    print(f"Total de record_id com instrumento: {total_record_ids}")
    print(f"Total de record_id com medicamentos extraídos: {len(record_ids_extraidos)}")
    print(f"Record_ids ausentes: {set(df['record_id'].unique()) - record_ids_extraidos}")

    return df_resultado

def extrair_medicamentos_incluindo_vazios(df):
    """
    Extrai TODOS os medicamentos, incluindo registros com campos incompletos.
    Se med_name e combinações estiverem vazias, cria entrada com nome 'medicamento_não_informado'.
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

    df_meds = df[df['redcap_repeat_instrument'] == 'medicamentos_em_uso'].copy()
    df_meds = df_meds.sort_values(by=['record_id', 'redcap_repeat_instance'])

    campos_chave = ['id_institution', 'uuidv5', 'full_name']
    for campo in campos_chave:
        if df_meds[campo].dtype == object:
            df_meds[campo] = df_meds[campo].ffill().str.upper()
        else:
            df_meds[campo] = df_meds[campo].ffill()

    registros = []
    record_ids_extraidos = set()

    for _, row in df_meds.iterrows():
        base_info = {
            'id_institution': row['id_institution'],
            'uuidv5': row['uuidv5'],
            'full_name': row['full_name'],
            
        }

        record_id = row['record_id']
        instancia = row.get('redcap_repeat_instance', 1)

        adicionou_algum = False

        # Tentativa de extrair medicamento principal
        raw_med_name = row.get('med_name')
        if pd.notnull(raw_med_name):
            med_name = str(raw_med_name).strip().lower()
            if med_name and med_name != 'nan':
                freq = row.get('taken_daily')
                taken_daily = None
                if pd.notnull(freq):
                    chave = str(int(freq)) if not isinstance(freq, str) else freq.strip()
                    taken_daily = tomadas_dia.get(chave)

                registros.append({
                    **base_info,
                    'med_name': med_name,
                    'dosage': row.get('dosage'),
                    'taken_daily': taken_daily
                })
                adicionou_algum = True

        # Tentativa de extrair combinações
        for i in range(1, 7):
            comb = row.get(f'combination_{i}')
            if pd.notnull(comb) and str(comb).strip().lower() not in ['', 'nan']:
                registros.append({
                    **base_info,
                    'med_name': str(comb).strip().lower(),
                    'dosage': row.get(f'combination_dosage_{i}'),
                    'taken_daily': None
                })
                adicionou_algum = True

        # Caso nenhum medicamento tenha sido extraído, criar linha genérica
        if not adicionou_algum:
            registros.append({
                **base_info,
                'med_name': f"medicamento_não_informado_{record_id}_{instancia}",
                'dosage': row.get('dosage'),
                'taken_daily': tomadas_dia.get(str(int(row['taken_daily']))) if pd.notnull(row.get('taken_daily')) else None
            })

        record_ids_extraidos.add(record_id)

    df_resultado = pd.DataFrame(registros)
    df_resultado = df_resultado.sort_values(by=['id_institution', 'uuidv5', 'full_name'])
    df_resultado['uuidv5'] = df_resultado['uuidv5'].str.lower()

    print("🔍 Estatísticas da extração (incluindo registros vazios):")
    total_record_ids = df[df['redcap_repeat_instrument'] == 'medicamentos_em_uso']['record_id'].nunique()
    print(f"Total de record_id com instrumento: {total_record_ids}")
    print(f"Total de record_id com medicamentos extraídos: {len(record_ids_extraidos)}")
    print(f"Record_ids incluídos: {sorted(record_ids_extraidos)}")

    return df_resultado

# -----------------------------------------------

def classificar_risco(df_score, condicao_critico, condicao_alerta, condicao_atencao ):
    """
    Aplica condições de risco e retorna:
    - DataFrame agrupado por 'cpf' com colunas: id_institution, cpf, full_name, risco (colorido em HTML)
    - Resumo com contagem por nível de risco (rótulos limpos, sem HTML)
   
     Parâmetros:
    - df: DataFrame original
    - condicao_critico, condicao_alerta, condicao_atencao: dicionários de condições
    
    - incluir_sem_risco: se True, classifica como 'Sem Risco' os registros que não se encaixam em nenhuma categoria
    OBS: Para visualizar cores no Jupyter, usar `display(HTML(resultado.to_html(escape=False)))`
    """

    df_score_copia = df_score.copy()

    df_score_copia['risco'] = None

    cores_por_risco = {
        'Alto (MPI 3)': 'red',
        'Moderado (MPI 2)': 'orange',
        'Leve (MPI 1)': 'green'
    }

    def aplicar_classificacao(df_local, condicoes_dict, label):
        cond = pd.Series(True, index=df_local.index)
        for col, func in condicoes_dict.items():
            cond &= df_local[col].apply(func)
        return cond.replace({True: label, False: None})

    for condicoes, label in [
        (condicao_critico, 'Alto (MPI 3'),
        (condicao_alerta, 'Moderado (MPI 2)'),
        (condicao_atencao, 'Leve (MPI 1)')
    ]:
        mask = aplicar_classificacao(df_score_copia, condicoes, label)
        condicao_vazia = df_score_copia['risco'].isna()
        df_score_copia.loc[mask.notna() & condicao_vazia, 'risco'] = label

    # # Preencher com "Sem Risco", se solicitado
    # if incluir_sem_risco:
    #     df_copia.loc[df_copia['risco'].isna(), 'risco'] = 'Sem Risco'

    # Define a ordem de severidade
    ordem_prioridade = {'Alto (MPI 3)': 0, 'Moderado (MPI 2)': 1, 'Leve (MPI 1)': 2}
    df_score_copia['prioridade'] = df_score_copia['risk'].map(ordem_prioridade)

    agrupado = (
        df_score_copia
        .sort_values('prioridade')
        .groupby('uuidv5', as_index=False)
        .first()[['id_institution', 'uuidv5', 'full_name', 'risco']]
    )

    # Aplica cor HTML na coluna 'risco'
    def colorir(valor):
        cor = cores_por_risco.get(valor, 'black')
        return f'<span style="color: {cor}; font-weight: bold;">{valor}</span>'

    agrupado['Score_Fragilidade'] = agrupado['risco'].apply(colorir)

    # Resumo por grupo de risco
    resumo = (
        agrupado
        .groupby(['id_institution', 'risco'], as_index=False)
        .size()
        .rename(columns={'size': 'total'})
    )

    return agrupado.drop(columns=['risco']), resumo

# %%
