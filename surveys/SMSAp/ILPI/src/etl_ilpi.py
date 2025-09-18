# %%
import pandas as pd
import uuid
import logging
# %%
## ----------------------
## Função para gerar UUIDv5 a partir do CPF
## ______________________

def gerar_uuid_v5(cpf):
    namespace = uuid.NAMESPACE_DNS # usando namespace padrão
    return uuid.uuid5(namespace, cpf)

## ----------------------
## Função para facilitar a análise baseada em CPF, considerando que o DF tem colunas vazias ou NA.
## ----------------------

def etl_df_redcap(df, campos_chave, campo_discriminador="institution_name"):
    """
    Executa o pré-processamento (ETL) no DataFrame exportado do REDCap para análise posterior.
    Propaga campos-chave (ex: cpf, full_name) a partir de linhas onde há valor no campo_discriminador 
    (ex: institution_name).
    Substitui as colunas originais pelas propagadas sem sufixo.

    Uso: 
    campos_para_propagar = ["cpf", "full_name", "institution_name"]
    df_corrigido = etl_df_redcap(df, campos_para_propagar)
    """
    # Copia o data frame para segurança
    df = df.copy()
    # Identifica início de novos grupos
    novo_grupo = df[campo_discriminador].notna() & (df[campo_discriminador] != 0)
    df["_grupo"] = novo_grupo.cumsum()

    for campo in campos_chave:
        # Cria coluna propagada
        coluna_propagada = df.groupby("_grupo")[campo].transform("first")

        ## Padroniza em caixa alta se for string
        #if pd.api.types.is_string_dtype(propagado):
        #    propagado = propagado.str.upper()
        
        # Remove coluna original e substitui pela propagada sem o sufixo
        df.drop(columns=[campo], inplace=True)
        df[campo] = coluna_propagada

    df.drop(columns=["_grupo"], inplace=True)
   
    return df


def preparar_dados_residentes(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    try:
        # --- Configurações iniciais ---
        colunas_necessarias = [
            "id_institution", "institution_name", "record_id", "uuidv5",
            "full_name", "date_of_birth", "elder_age", "sex", 
            "race", "education"
        ]
        colunas_numericas = [ "id_institution", "record_id", "elder_age", "sex", "race"]
        chave_duplicidade = ["uuidv5"]

        def validar_colunas(df: pd.DataFrame, colunas: list[str]) -> None:
            colunas_faltando = set(colunas) - set(df.columns)
            if colunas_faltando:
                raise ValueError(f"Colunas ausentes no DataFrame: {sorted(colunas_faltando)}")

        validar_colunas(df, colunas_necessarias)

        # --- Seleção e cópia dos dados relevantes ---
        residentes = df[colunas_necessarias].copy()
        logging.info(f"{residentes.shape[0]} registros carregados inicialmente.")

        # --- Padronização de campos ---
        residentes["uuidv5"] = residentes["uuidv5"].astype(str).str.strip().str.lower()

        # --- Limpeza e conversão de colunas numéricas ---
        for col in colunas_numericas:
            residentes = residentes[residentes[col].notna()]
            residentes[col] = residentes[col].astype(int)

        logging.info(f"{residentes.shape[0]} registros após limpeza e conversão de tipos.")

        # --- Identificação de duplicatas ---
        duplicados_mask = residentes.duplicated(subset=chave_duplicidade, keep=False)
        duplicados_df = residentes.loc[duplicados_mask].sort_values(by=chave_duplicidade)

        if not duplicados_df.empty:
            logging.warning(f"Encontrados {duplicados_df.shape[0]} registros com {chave_duplicidade} duplicado(s).")
            residentes = residentes.drop_duplicates(subset=chave_duplicidade, keep="first")
        else:
            logging.info("Nenhum registro duplicado encontrado.")
            duplicados_df = pd.DataFrame()

        logging.info(f"{residentes.shape[0]} registros finais após deduplicação.")

        return residentes, duplicados_df

    except Exception as e:
        logging.error(f"Erro ao preparar dados dos residentes: {str(e)}")
        return pd.DataFrame(), pd.DataFrame()
    


# --------------------
# Funções de processamento
# --------------------

# AJUSTAR#################################################

def limpar_e_converter_colunas(df: pd.DataFrame, colunas_tipos: dict) -> pd.DataFrame:
    """
    Limpa e converte colunas para os tipos especificados, com tratamento seguro de erros.

    Parâmetros:
    - df (pd.DataFrame): DataFrame original.
    - colunas_tipos (dict): Dicionário no formato {"coluna": tipo_desejado},
      onde tipo_desejado pode ser: int, float, str, 'datetime', etc.

    Retorna:
    - pd.DataFrame: DataFrame limpo e com colunas convertidas.
    """
    df = df.copy()  # Evita modificar o DataFrame original ou views

    for coluna, tipo in colunas_tipos.items():
        if coluna not in df.columns:
            logging.warning(f"Coluna '{coluna}' não encontrada no DataFrame. Ignorando.")
            continue

        logging.info(f"Limpando e convertendo coluna '{coluna}' para '{tipo}'...")

        try:
            if isinstance(tipo, type) and (tipo is int or tipo is float):
                # Conversão segura de números
                df.loc[:, coluna] = pd.to_numeric(df[coluna], errors='coerce')

            elif isinstance(tipo, str) and tipo.lower() == "datetime":
                # Conversão para datetime
                df.loc[:, coluna] = pd.to_datetime(df[coluna], errors='coerce')

            elif isinstance(tipo, type) and tipo is str:
                # Conversão para string
                df.loc[:, coluna] = df[coluna].astype(str).str.strip()

            elif isinstance(tipo, type):
                # Qualquer outro tipo válido
                df.loc[:, coluna] = df[coluna].astype(tipo)

            else:
                logging.warning(f"Tipo '{tipo}' para coluna '{coluna}' não é suportado.")
                continue

        except Exception as e:
            logging.error(f"Erro ao converter coluna '{coluna}' para '{tipo}': {e}")
            continue

        # Remove valores nulos após a conversão
        antes = df.shape[0]
        df = df[df[coluna].notna()].copy()
        depois = df.shape[0]
        removidos = antes - depois
        if removidos > 0:
            logging.warning(f"{removidos} registros removidos da coluna '{coluna}' após tentativa de conversão.")

    return df    
# %%
# Lendo o arquivo .csv do REDCap
df = pd.read_csv("../../../../data/SMSAp/ILPI/PerfilEpidemiolgicos_DATA_2025-09-17_1151.csv",
                 sep=";")
df.head()

# %%
##  Checagem dos tipos de variáveis presentes no data frame
df.dtypes
# %%
## -------------------
## Fazendo o ajuste e propagando o CPF, nome e ILPI para as linha necessárias
## -------------------

campos_para_propagar = ["cpf", "full_name", "institution_name"]
df_corrigido = etl_df_redcap(df, campos_para_propagar)
df_corrigido
# %%
# ## - Verificando se o CPF foi propagado corretamente e listando as colunas

print(df_corrigido[df_corrigido["cpf"].isna()])

# %%

# Transformando colunas em int
cols_to_convert = ["record_id","redcap_repeat_instance", "institution_name", "sex", "elder_age", 
       "race", "scholarship", "institut_time_years", "institut_time_months", "family_support", "dependence_degree", 
       "link_type___1", "link_type___2", "link_type___3", "elder_income_source", "taken_daily", "morbidities___1", 
       "morbidities___2", "morbidities___3", "morbidities___4", "morbidities___5", "morbidities___6", "morbidities___7",
       "morbidities___8", "morbidities___9", "morbidities___10", "morbidities___11", "morbidities___12", "morbidities___13", 
       "morbidities___14", "morbidities___15", "morbidities___16", "morbidities___17", "morbidities___18", 
       "morbidities___19", "morbidities___20", "morbidities___21", "health_condition", "elder_visitors", 
       "physical_desabilities___1", "physical_desabilities___2", "physical_desabilities___3", "weight_loss", 
       "amount_weight_loss", "elder_strenght", "elder_hospitalized", "elder_difficulties", "elder_mobility", 
       "basic_activities_diffic", "falls_number"]

df_corrigido[cols_to_convert] = df_corrigido[cols_to_convert].astype("Int64") 

# %%
## - Eliminado colunas que não são necessárias para a análise
cols_to_drop = ["redcap_survey_identifier", "identificao_da_ilpi_f650_timestamp", "institution_type", 
                "identificao_da_ilpi_f650_complete", "dados_sciodemogrficos_timestamp", "name", "surname", 
                "admission_date", "dados_sciodemogrficos_complete", "medicamentos_em_uso_timestamp",
                "medicamentos_em_uso_complete", "morbidades_prvias_timestamp", "morbidities___nan",
                "morbidades_prvias_complete", "estado_de_sade_timestamp", "estado_de_sade_complete", 
                "componentes_de_fragilidade_timestamp", "physical_desabilities___nan", 
                "componentes_de_fragilidade_complete", "responsvel_pelo_preenchimento_timestamp", 
                "responsvel_pelo_preenchimento_complete"]

df_filtered = df_corrigido.drop(columns=cols_to_drop)

# %%
# Gerando o UUIDv5 paracada CPF no DataFrame utilizando apply

df_filtered["uuidv5"] = df_filtered["cpf"].apply(lambda cpf: gerar_uuid_v5(cpf))
df_filtered

# %%
## - Reordenando as colunas 
df_final = df_filtered[["uuidv5", "record_id", "redcap_repeat_instrument", "redcap_repeat_instance", "visit_date", 
                        "latitude", "longitude", "institution_name", "cpf", "full_name", "sex", "date_of_birth", 
                        "elder_age", "race", "scholarship", "institut_time_years", "time_months", "institut_time_months", 
                        "family_support", "dependence_degree", "link_type___1", "link_type___2", "link_type___3", 
                        "elder_income_source", "med_name", "dosage", "recorded", "combination_of_medicines", 
                        "combination_1", "combination_dosage", "combination_2", "combination_dosage_2", "combination_3", 
                        "combination_dosage_3", "combination_4", "combination_dosage_4", "combination_5", 
                        "combination_dosage_5", "combination_6", "combination_dosage_6", "taken_daily", "morbidities___1", 
                        "morbidities___2", "morbidities___3", "morbidities___4", "morbidities___5", "morbidities___6", 
                        "morbidities___7", "morbidities___8", "morbidities___9", "morbidities___10", "morbidities___11", 
                        "morbidities___12", "morbidities___13", "morbidities___14", "morbidities___15", "morbidities___16", 
                        "morbidities___17", "morbidities___18", "morbidities___19", "morbidities___20", "morbidities___21", 
                        "other_morbidities", "health_condition", "elder_visitors", "physical_desabilities___1", "physical_desabilities___2", 
                        "physical_desabilities___3", "weight_loss", "amount_weight_loss", "elder_strenght", "elder_hospitalized", 
                        "elder_difficulties", "elder_mobility", "basic_activities_diffic", "falls_number", "interviewer_name"]]
                        
df_final = df_final.rename(columns={"scholarship":"education"})
df_final

# %%
df_ilpi = df_final.copy()

df_ilpi.rename(columns={"institution_name":"id_institution"}, inplace=True)

ilpi_map = {
    1: "Associaçao Solar das Acácias",
    2: "Abrigo Comendador Walmor",
    3: "Abrigo Aconchego Dona Norma",
    4: "Associação Núcleo Espírita Amigos para Sempre",
    5: "Casa Silvestre Linhares"
}

df_ilpi["institution_name"] = df_ilpi['id_institution'].map(ilpi_map)
df_ilpi

# %%

df_ilpi.to_csv("../../../../data/SMSAp/ILPI/base_perfil_epidemiologico.csv",
                   index=False,
                   sep=";")
print("✅ Arquivo Base Perfil Epidemiológico Residente salvo!!" )
# %%