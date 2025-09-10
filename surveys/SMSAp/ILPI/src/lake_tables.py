# %%
import pandas as pd
from etl_ilpi import preparar_dados_residentes, limpar_e_converter_colunas

# ---------------------
# Leitura dos dados
# ---------------------
df = pd.read_csv("../../../../data/SMSAp/ILPI/base_perfil_epidemiologico.csv",
                 sep=";",
                 decimal= ".")
df.head()
# %%
df.columns

# %%

df.dtypes


# %%
# --------------------
# Gerar data frame Registros Duplicados e  Residentes
# --------------------

residentes_ILPI, duplicados_ILPI = preparar_dados_residentes(df)

# Inspecionar duplicados
duplicados_ILPI

# %%
# --------------------
# Converter colunas para a tabela de residentes e salvar no lake
# --------------------

colunas_para_converter = {
    "elder_age": int,
    "sex": int,
    "race": int,
    "education": int
}
residentes_ILPI = residentes_ILPI[["institution_name", "uuidv5", "full_name", 
                                   "elder_age", "date_of_birth", "sex", "race", "education"]]
residentes_ILPI = limpar_e_converter_colunas(residentes_ILPI, colunas_para_converter)
residentes_ILPI

# %%
# Salvando tabela residentes_ILPI
residentes_ILPI.to_csv("../../../../data/SMSAp/lake/Residente.csv")
print("✅Tabela Residentes ILPI foi salva no lake!")

# %%
# --------------------
# Converter colunas para a tabela tempo de instituicao e salvar no lake
# --------------------

colunas_para_converter = {
    "institut_time_years": int,
}

tempo_instituicao = df[["institution_name", "uuidv5", "institut_time_years"]]
tempo_instituicao = limpar_e_converter_colunas(tempo_instituicao, colunas_para_converter)
tempo_instituicao
# %%
# Salvando tabela tempo de instituição 
tempo_instituicao.to_csv("../../../../data/SMSAp/lake/Residente.csv")
print("✅Tabela Tempo Instituíção Residentes ILPI foi salva no lake!")

# %%
# --------------------
# Converter colunas para a tabela grau de dependencia e salvar no lake
# --------------------

colunas_para_converter = {
    "dependence_degree": int
}

grau_dependencia = df[["institution_name", "uuidv5", "dependence_degree"]]
grau_dependencia = limpar_e_converter_colunas(grau_dependencia, colunas_para_converter)
grau_dependencia["dependence_degree"] =  grau_dependencia["dependence_degree"].astype(int)
grau_dependencia
# %%
# Salvando tabela grau de dependencia
grau_dependencia.to_csv("../../../../data/SMSAp/lake/GrauDependencia.csv")
print("✅Tabela Grau de dependência foi salva no lake!")
# %%
# --------------------
# Converter colunas para a tabela grau estado de saúde e salvar no lake
# --------------------

colunas_para_converter = {
    "health_condition": int
}

estado_saude = df[["institution_name", "uuidv5", "health_condition"]]
estado_saude = limpar_e_converter_colunas(estado_saude, colunas_para_converter)
estado_saude["health_condition"] =  estado_saude["health_condition"].astype(int)
estado_saude
# %%
# Salvando tabela grau de dependencia
estado_saude.to_csv("../../../../data/SMSAp/lake/EstadoSaude.csv")
print("✅Tabela Grau de dependência foi salva no lake!")
# %%
# --------------------
# Converter colunas para a tabela suporte familiar e salvar no lake
# --------------------

colunas_para_converter = {
    "family_support": int
}

suporte_familiar = df[["institution_name", "uuidv5", "family_support"]]
suporte_familiar = limpar_e_converter_colunas(suporte_familiar, colunas_para_converter)
suporte_familiar["family_support"] =  suporte_familiar["family_support"].astype(int)
suporte_familiar
# %%
# Salvando tabela grau de dependencia
suporte_familiar.to_csv("../../../../data/SMSAp/lake/SuporteFamiliar.csv")
print("✅Tabela Grau de dependência foi salva no lake!")
# %%
# --------------------
# Converter colunas para a tabela ILPI e salvar no lake
# --------------------
df_ilpi = df.copy()

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
colunas_para_converter = {
    "id_institution": int
}

ILPI = df_ilpi[["id_institution", "institution_name", "latitude", "longitude"]]
ILPI = ILPI[ILPI["latitude"].notna()].astype({"latitude":float})
ILPI = limpar_e_converter_colunas(ILPI, colunas_para_converter)
ILPI = ILPI.drop_duplicates(subset=["id_institution"]).sort_values(by="id_institution")
ILPI
# %%
# Salvando tabela grau de dependencia
ILPI.to_csv("../../../../data/SMSAp/lake/ILPI.csv")
print("✅Tabela ILPI foi salva no lake!")
# %%
