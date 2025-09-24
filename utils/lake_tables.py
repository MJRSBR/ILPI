# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')
import re
import pandas as pd
from etl_ilpi import preparar_dados_residentes, limpar_e_converter_colunas
from funcoes.f_process import extrair_morbidades, extrair_medicamentos, extrair_medicamentos_incluindo_vazios
# %%

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
residentes_ILPI
# %%
# --------------------
# Converter colunas para a tabela de residentes e salvar no lake
# --------------------

# colunas_para_converter = {
#     "elder_age": int,
#     "sex": int,
#     "race": int,
#     "education": int
# }
residentes_ILPI = residentes_ILPI[["id_institution", "uuidv5", "full_name", 
                                   "elder_age", "date_of_birth", "sex", "race", "education"]]
#residentes_ILPI = limpar_e_converter_colunas(residentes_ILPI, colunas_para_converter)
residentes_ILPI

# %%
# Salvando tabela residentes_ILPI
residentes_ILPI.to_csv("../../../../data/SMSAp/lake/Residente.csv", index=False)
print("✅Tabela Residentes ILPI foi salva no lake!")

# %%
# --------------------
# Converter colunas para a tabela tempo de instituicao e salvar no lake
# --------------------

colunas_para_converter = {
    "institut_time_years": int,
}

tempo_instituicao = df[["id_institution", "uuidv5", "institut_time_years"]]
tempo_instituicao = limpar_e_converter_colunas(tempo_instituicao, colunas_para_converter)
tempo_instituicao
# %%
# Salvando tabela tempo de instituição 
tempo_instituicao.to_csv("../../../../data/SMSAp/lake/TempoInstituicao.csv", index=False)
print("✅Tabela Tempo Instituíção Residentes ILPI foi salva no lake!")

# %%
# --------------------
# Converter colunas para a tabela grau de dependencia e salvar no lake
# --------------------

colunas_para_converter = {
    "dependence_degree": int
}

grau_dependencia = df[["id_institution", "uuidv5", "dependence_degree"]]
grau_dependencia = limpar_e_converter_colunas(grau_dependencia, colunas_para_converter)
grau_dependencia["dependence_degree"] =  grau_dependencia["dependence_degree"].astype(int)
grau_dependencia
# %%
# Salvando tabela grau de dependencia
grau_dependencia.to_csv("../../../../data/SMSAp/lake/GrauDependencia.csv", index=False)
print("✅Tabela Grau de dependência foi salva no lake!")
# %%
# --------------------
# Converter colunas para a tabela grau estado de saúde e salvar no lake
# --------------------

colunas_para_converter = {
    "health_condition": int
}

estado_saude = df[["id_institution", "uuidv5", "health_condition"]]
estado_saude = limpar_e_converter_colunas(estado_saude, colunas_para_converter)
estado_saude["health_condition"] =  estado_saude["health_condition"].astype(int)
estado_saude
# %%
# Salvando tabela grau de dependencia
estado_saude.to_csv("../../../../data/SMSAp/lake/EstadoSaude.csv", index=False)
print("✅Tabela Grau de dependência foi salva no lake!")
# %%
# --------------------
# Converter colunas para a tabela suporte familiar e salvar no lake
# --------------------

colunas_para_converter = {
    "family_support": int
}

suporte_familiar = df[["id_institution", "uuidv5", "family_support"]]
suporte_familiar = limpar_e_converter_colunas(suporte_familiar, colunas_para_converter)
suporte_familiar["family_support"] =  suporte_familiar["family_support"].astype(int)
suporte_familiar
# %%
# Salvando tabela grau de dependencia
suporte_familiar.to_csv("../../../../data/SMSAp/lake/SuporteFamiliar.csv", index=False)
print("✅Tabela Grau de dependência foi salva no lake!")
# %%
# --------------------
# Converter colunas para a tabela ILPI e salvar no lake
# --------------------

colunas_para_converter = {
    "latitude": float,	
    "longitude": float,
}

ILPI = df[["id_institution", "institution_name", "latitude", "longitude"]]
ILPI = ILPI[ILPI["latitude"].notna()].astype({"latitude":float})
ILPI = limpar_e_converter_colunas(ILPI, colunas_para_converter)
ILPI = ILPI.drop_duplicates(subset=["id_institution"]).sort_values(by="id_institution")
ILPI
# %%
# Salvando tabela grau de dependencia
ILPI.to_csv("../../../../data/SMSAp/lake/ILPI.csv", index=False)
print("✅Tabela ILPI foi salva no lake!")
# %%
# --------------------
# Converter colunas para a tabela Qtde Medicamentos e salvar no lake
# --------------------

qtde_medic_vaz = extrair_medicamentos_incluindo_vazios(df)
qtde_medic_vaz

# %%
qtde_medic_vaz = extrair_medicamentos(df)
qtde_medic_vaz["uuidv5"] = qtde_medic_vaz["uuidv5"].str.lower()
qtde_medic_vaz
# %%
qtde_medic_vaz = qtde_medic_vaz.groupby(["id_institution", "uuidv5"]).size().reset_index(name="qtd_medic_vaz")
qtde_medic_vaz
# %%
# Salvando tabela Qtde Medicamento por Residente
qtde_medic_vaz.to_csv('../../../../data/SMSAp/lake/QtdeMedicTot.csv', index=False)
print("✅Tabela Qtde Medicamento foi salva no lake!")
# %%

# --------------------
# Converter colunas para a tabela Morbidades e salvar no lake
# --------------------
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

morb = extrair_morbidades(df, morb_dict)
morb
# %%
morb = morb[["id_institution", "uuidv5", "soma_morbidities"]]
morb
# %%
# Salvando tabela Numero de Morbidades por Residente
morb.to_csv('../../../../data/SMSAp/lake/NumMorbidades.csv', index=False)
print("✅Tabela Numero de Morbidades foi salva no lake!")
# %%

# --------------------
# Converter colunas para a tabela Mobilidade e salvar no lake
# --------------------
colunas_para_converter = {
    "physical_desabilities___1": int,	
    "physical_desabilities___2": int,
    "physical_desabilities___3": int,
    "elder_mobility": int, 
    "elder_difficulties": int,
}
mobility = df[["id_institution", "uuidv5", "physical_desabilities___1",
               "physical_desabilities___2", "physical_desabilities___3",
               "elder_mobility", "elder_difficulties", ]]
mobility = mobility[mobility["elder_mobility"].notna()].astype({"elder_mobility":int})
mobility = limpar_e_converter_colunas(mobility, colunas_para_converter)
mobility
# %%
# Salvando tabela mobilidade
mobility.to_csv("../../../../data/SMSAp/lake/Mobilidade.csv", index=False)
print("✅Tabela ILPI foi salva no lake!")

# %%
# --------------------
# Converter colunas para a tabela Nutricional e salvar no lake
# --------------------

hospitalization = df[["id_institution", "uuidv5", "elder_hospitalized"]]
hospitalization = hospitalization[hospitalization["elder_hospitalized"].notna()].astype({"elder_hospitalized":int})
hospitalization
# %%
# Salvando tabela Estado Nutricional
hospitalization.to_csv("../../../../data/SMSAp/lake/Hospitalizacao.csv", index=False)
print("✅Tabela Estado Nutricional foi salva no lake!")
# %%
# --------------------
# Converter colunas para a tabela Quedas e salvar no lake
# --------------------				

falls = df[["id_institution", "uuidv5", "falls_number"]]
falls = falls.dropna()
falls
# %%
# Salvando tabela Quedas 
falls.to_csv("../../../../data/SMSAp/lake/Quedas.csv", index=False)
print("✅Tabela Quedas foi salva no lake!")
# %%
# -------------------
# Indicadores Sociais
# -------------------

#social = df["sex", "race", "elder_income_source", "education", "elder_visitors"]

# %%
# --------------------
# Converter colunas para a tabela Nutricional e salvar no lake
# --------------------
colunas_para_converter = {
    "elder_strenght": int,	
    "weight_loss": int,
    "amount_weight_loss": int,

}

nutritional = df[["id_institution", "uuidv5", "elder_strenght", "weight_loss", "amount_weight_loss"]]
nutritional = nutritional[nutritional["elder_strenght"].notna()].astype({"elder_strenght":int})
nutritional["amount_weight_loss"] = nutritional["amount_weight_loss"].fillna(0)
nutritional = limpar_e_converter_colunas(nutritional, colunas_para_converter)
nutritional
# %%
# Salvando tabela Estado Nutricional
nutritional.to_csv("../../../../data/SMSAp/lake/EstadoNutricional.csv", index=False)
print("✅Tabela Estado Nutricional foi salva no lake!")
# %%
# --------------------
# Converter colunas para a tabela ABVD e salvar no lake
# --------------------

abvd = df[["id_institution", "uuidv5","basic_activities_diffic"]]
abvd = abvd[abvd["basic_activities_diffic"].notna()].astype({"basic_activities_diffic":int})
abvd
# %%
# Salvando tabela ABVD
abvd.to_csv("../../../../data/SMSAp/lake/ABVD.csv", index=False)
# %%

# %%
mpi_table = (
    residentes_ILPI
    .merge(morb, how="left", on="uuidv5", suffixes=("_left", "_right"))
    .merge(qtde_medic_vaz, how="left", on="uuidv5")
    .merge(grau_dependencia, how="left", on="uuidv5")
    .merge(abvd, how="left", on="uuidv5")
    .reset_index(drop=True)
)

#mpi_table = mpi_table.rename(columns={"id_institution_left": "id_institution"})
# mpi_table["uuidv5"] = mpi_table["uuidv5"].str.lower()
# mpi_table = mpi_table.drop()
# mpi_table

mpi_table.columns

# %%

colunms_to_drop = ["id_institution_right", "id_institution_left", "id_institution_x", "id_institution_y" ]

mpi_table.drop(columns=colunms_to_drop, axis=1, inplace=True)

mpi_table.columns

# %%

mpi_table_1 = (
    mpi_table
    .merge(falls, how="left", on="uuidv5", suffixes=("_left", "_right"))
    .merge(nutritional, how="left", on="uuidv5")
    .merge(mobility, how="left", on="uuidv5")
    # .merge(hospitalization, how="left", on="uuidv5")
    .reset_index(drop=True)
)


mpi_table_1.columns
# %%

colunms_to_drop = ['id_institution_x', 'id_institution_y', "id_institution_right"]
mpi_table_1 = mpi_table_1.rename(columns={"id_institution_left": "id_institution"})
mpi_table_1.drop(columns=colunms_to_drop, axis=1, inplace=True)

mpi_table_1.columns
# %%
mpi_table_final = (
    mpi_table_1
    .merge(hospitalization, how="left", on="uuidv5")
    .merge(tempo_instituicao, how="left", on="uuidv5")
    .reset_index(drop=True)
)

mpi_table_final.columns
# %%
colunms_to_drop = ["id_institution_x", "id_institution_y"]

mpi_table_final.drop(columns=colunms_to_drop, axis=1, inplace=True)
mpi_table_final.columns



# %%

mpi_table_final = mpi_table_final[[
    "id_institution", "uuidv5", "full_name", "elder_age",
    "date_of_birth", "sex", "race", "education", "basic_activities_diffic",
    "physical_desabilities___1", "physical_desabilities___2", 
    "physical_desabilities___3", "elder_mobility", "elder_difficulties", 
    "falls_number", "elder_hospitalized", "elder_strenght", "weight_loss", 
    "amount_weight_loss", "soma_morbidities", "qtd_medic_vaz", "institut_time_years"]]

mpi_table_final
# %%

mpi_table_final.to_csv("../../../../data/SMSAp/lake/mpiFinal.csv", index=False)
print("✅Tabela Tabela Final MPI foi salva no lake!")
# %%
mpi_table_final.columns
# %%
