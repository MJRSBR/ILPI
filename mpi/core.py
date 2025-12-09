# %%

__author__ = "mjrs_br"
__version__ = '0.0.1'


import numpy as np
import pandas as pd
from utils import _safe_col

# %%

# def compute_brief_mpi(
#     social_marks, abvd_items, mobility_items,
#     falls, inpatient, nutritional_items,
#     comorbidities_count, drug_count, nursing_home
# ):
#     sex, race, education = social_marks
#     score_social = (
#         (0 if sex == 1 else 1 if sex == 2 else 0) +
#         (0 if race in [1, 4] else 1) +
#         (1 if education in [1, 2] else 0)
#     )

#     basic_act = 0 if abvd_items[0] == 1 else 1 if abvd_items[0] == 2 else 0
#     phys_disab = sum(1 for i in abvd_items[1:3] if i == 1)
#     score_abvd = basic_act + phys_disab

#     mobility = 1 if mobility_items[0] == 1 else 0
#     difficulties = 0 if mobility_items[1] == 1 else 1 if mobility_items[1] == 2 else 0
#     score_mobility = mobility + difficulties

#     score_falls_ = 0 if falls[0] == 1 else 1 if falls[0] in [2, 3] else 0
#     score_inpatient_ = 0 if inpatient[0] == 1 else 1

#     strength = 1 if nutritional_items[0] == 1 else 0
#     weight_loss = 1 if nutritional_items[1] == 1 else 0
#     amount_loss = 1 if nutritional_items[2] == 1 else 2 if nutritional_items[2] == 2 else 0
#     score_nutrition = strength + weight_loss + amount_loss

#     score_comorb = comorbidities_count
#     score_drugs = drug_count
#     score_nursing = nursing_home

#     total_score = (
#         score_social + score_abvd + score_mobility + score_falls_ +
#         score_inpatient_ + score_nutrition + score_comorb + score_drugs + score_nursing
#     )

#     mpi_raw = total_score / 9.0
#     mpi = round(mpi_raw, 2)
#     if mpi <= 0.33:
#         risk = "Leve (MPI 1)"
#     elif mpi <= 0.66:
#         risk = "Moderado (MPI 2)"
#     else:
#         risk = "Alto (MPI 3)"

#     return {
#         "score_social": score_social,
#         "score_abvd": score_abvd,
#         "score_mobility": score_mobility,
#         "score_falls": score_falls_,
#         "score_inpatient": score_inpatient_,
#         "score_nutrition": score_nutrition,
#         "score_comorb": score_comorb,
#         "score_drugs": score_drugs,
#         "score_nursing": score_nursing,
#         "total_score": total_score,
#         "MPI": mpi,
#         "risk": risk
#     }

# def aplicar_brief_mpi(df):
#     results = []
#     for _, row in df.iterrows():
#         results.append(compute_brief_mpi(
#             [row.get("sex", 0), row.get("race", 0), row.get("education", 0)],
#             [row.get("basic_activities_diffic", 0),
#              row.get("physical_desabilities___1", 0),
#              row.get("physical_desabilities___2", 0),
#              row.get("physical_desabilities___3", 0)],
#             [row.get("elder_mobility", 0), row.get("elder_difficulties", 0)],
#             [row.get("falls_number", 1)],
#             [row.get("elder_hospitalized", 0)],
#             [row.get("elder_strenght", 0), row.get("weight_loss", 0), row.get("amount_weight_loss", 0)],
#             row.get("soma_morbidities", 0),
#             row.get("qtd_medic_vaz", 0),
#             row.get("institut_time_years", 0)
#         ))
#     return pd.concat([df.reset_index(drop=True), pd.DataFrame(results)], axis=1)

# %%


def aplicar_brief_mpi(df, keep_raw=False):
    """
    Retorna DataFrame com colunas por domínio normalizadas (0, 0.5, 1),
    MPI normalizado (0..1) e classificação de risco.
    keep_raw=True inclui colunas intermediárias (brutas).
    """
    # preparar saída
    out = pd.DataFrame(index=df.index)

    # ids
    out["id_institution"] = _safe_col(df, "id_institution")
    out["uuidv5"] = _safe_col(df, "uuidv5")
    if "full_name" in df.columns:
        out["full_name"] = _safe_col(df, "full_name")

    # --- valores de entrada (com fallback) ---
    sex = _safe_col(df, "sex").fillna(0).astype(int)
    race = _safe_col(df, "race").fillna(0).astype(int)
    education = _safe_col(df, "education").fillna(0).astype(int)

    basic_act = _safe_col(df, "basic_activities_diffic").fillna(0).astype(int)
    phys1 = _safe_col(df, "physical_desabilities___1").fillna(0).astype(int)
    phys2 = _safe_col(df, "physical_desabilities___2").fillna(0).astype(int)
    phys3 = _safe_col(df, "physical_desabilities___3").fillna(0).astype(int)

    elder_mobility = _safe_col(df, "elder_mobility").fillna(0).astype(int)
    elder_difficulties = _safe_col(df, "elder_difficulties").fillna(0).astype(int)

    falls_number = _safe_col(df, "falls_number").fillna(1).astype(int)  # assume code 1 = no
    elder_hospitalized = _safe_col(df, "elder_hospitalized").fillna(0).astype(int)

    elder_strenght = _safe_col(df, "elder_strenght").fillna(0).astype(int)
    weight_loss = _safe_col(df, "weight_loss").fillna(0).astype(int)
    amount_weight_loss = _safe_col(df, "amount_weight_loss").fillna(0).astype(int)

    comorbidities = _safe_col(df, "soma_morbidities").fillna(0).astype(int)
    drugs = _safe_col(df, "qtd_medic_vaz").fillna(0).astype(int)
    nursing_time = _safe_col(df, "institut_time_years").fillna(0).astype(float)

    # -----------------------
    # 1) Scores brutos (0/1 ou pequeno inteiro)
    # -----------------------
    # Social: combina sex, race, education
    sex_score = sex.map({1: 0, 2: 1}).fillna(0).astype(int)
    race_score = race.apply(lambda x: 0 if x in [1, 4] else 1).astype(int)
    education_score = education.apply(lambda x: 1 if x in [1, 2] else 0).astype(int)
    social_raw = sex_score + race_score + education_score

    # ABVD: basic + physical (physical = 1 se phys1 or phys2 presente; phys3 ignorado)
    basic_score = basic_act.map({1: 0, 2: 1}).fillna(0).astype(int)
    physical_score = ((phys1 == 1) | (phys2 == 1)).astype(int)
    abvd_raw = basic_score + physical_score
    
    # Mobility: elder_mobility (1->1, 2->0) + elder_difficulties (1->0, 2->1)
    mobility_comp = elder_mobility.map({1: 1, 2: 0}).fillna(0).astype(int)
    difficulties_comp = elder_difficulties.map({1: 0, 2: 1}).fillna(0).astype(int)
    mobility_raw = mobility_comp + difficulties_comp

    # Falls: interpretacao comum: code 1=no, 2=one, >=3=multiplo
    falls_raw = np.where(falls_number == 1, 0,
                         np.where(falls_number == 2, 1,
                                  np.where(falls_number >= 3, 2, 0))).astype(int)

    # Inpatient: usar número/flag de internações (se 0->0, 1->0.5, >=2->1 depois)
    inpatient_raw = elder_hospitalized.astype(int)

    # Nutrition: combina strength, weight_loss, amount_weight_loss
    strength_score = elder_strenght.map({1: 1, 2: 0}).fillna(0).astype(int)
    weightloss_score = weight_loss.map({1: 1, 2: 0}).fillna(0).astype(int)

    # amount_weight_loss: code 1 -> 1, 2 -> 2   
    amount_score = amount_weight_loss.apply(lambda x: 1 if x == 1 else (2 if x == 2 else 0)).astype(int)

    # raw nutrition => cap at 2 (map 0->0, 1->0.5, >=2->1)    
    nutrition_raw = (strength_score + weightloss_score + amount_score)
    nutrition_raw = np.minimum(nutrition_raw, 2).astype(int)

    # Comorbidity, drugs e nursing time (map to 0/0.5/1 usando as regras)
    comorb_raw = comorbidities.astype(int)      # 0,1,2,3...
    drugs_raw = drugs.astype(int)               # qtde de drogas
    nursing_raw = nursing_time.astype(float)    # anos de instituíção

    # mantém raw columns para possível uso depois
    if keep_raw:
        out["social_raw"] = social_raw
        out["abvd_raw"] = abvd_raw
        out["mobility_raw"] = mobility_raw
        out["falls_raw"] = falls_raw
        out["inpatient_raw"] = inpatient_raw
        out["nutrition_raw"] = nutrition_raw
        out["comorb_raw"] = comorb_raw
        out["drugs_raw"] = drugs_raw
        out["nursing_raw"] = nursing_raw

    # -----------------------
    # 2) Normalizar cada domínio para {0, 0.5, 1}
    # -----------------------
    # social: 3->1, 1/2->0.5, 0->0
    score_social = np.where(social_raw == 3, 1.0,
                            np.where(social_raw >= 1, 0.5, 0.0))

    # ABVD: raw 0->0, 1->0.5, 2->1
    score_abvd = np.where(abvd_raw == 2, 1.0, np.where(abvd_raw == 1, 0.5, 0.0))

    # mobility: raw 0->0,1->0.5,2->1
    score_mobility = np.where(mobility_raw == 2, 1.0, np.where(mobility_raw == 1, 0.5, 0.0))

    # falls: raw 0->0,1->0.5,2->1    
    score_falls = np.where(falls_raw == 2, 1.0, np.where(falls_raw == 1, 0.5, 0.0))

    # inpatient: 0->0, 1->0.5, >=2->1    
    score_inpatient = np.where(inpatient_raw >= 2, 1.0, np.where(inpatient_raw == 1, 0.5, 0.0))

    # nutrition: 0->0, 1->0.5, >=2->1 (limita nutritional_raw em 2 para opçoes de maior perda de peso)    
    score_nutrition = np.where(nutrition_raw >= 2, 1.0, np.where(nutrition_raw == 1, 0.5, 0.0))

    # comorbidity: 0->0, 1-2->0.5, >=3->1
    score_comorb = np.where(comorb_raw >= 3, 1.0, np.where(comorb_raw >= 1, 0.5, 0.0))

    # drugs: 0-3->0, 4-6->0.5, >=7->1   
    score_drugs = np.where(drugs_raw >= 7, 1.0, np.where(drugs_raw >= 4, 0.5, 0.0))

    # nursing_time (institut_time_years): 0-2 -> 0, 3-4 -> 0.5, >=5 -> 1    
    score_nursing = np.where(nursing_raw >= 5, 1.0,
                             np.where((nursing_raw >= 3) & (nursing_raw <= 4), 0.5, 0.0))
    
    # -----------------------
    # 3) Construir saída (cada domínio e MPI normalizado)
    # -----------------------    
    out["score_social"] = score_social
    out["score_abvd"] = score_abvd
    out["score_mobility"] = score_mobility
    out["score_falls"] = score_falls
    out["score_inpatient"] = score_inpatient
    out["score_nutrition"] = score_nutrition
    out["score_comorb"] = score_comorb
    out["score_drugs"] = score_drugs
    out["score_nursing"] = score_nursing

    # MPI normalizado: média dos 9 domínios (0..1)
    domain_cols = [
        "score_social", "score_abvd", "score_mobility", "score_falls",
        "score_inpatient", "score_nutrition", "score_comorb", "score_drugs", "score_nursing"
    ]
    out["MPI"] = round(out[domain_cols].mean(axis=1), 2)

    # classificação conforme suas faixas
    out["risk"] = np.where(out["MPI"] <= 0.33, "Leve (MPI 1)",
                           np.where(out["MPI"] <= 0.66, "Moderado (MPI 2)", "Alto (MPI 3)"))

    # reordenar colunas: id_institution, uuidv5, full_name (se presente), depois domínios, MPI, risk
    cols_after_id = []
    if "full_name" in out.columns:
        cols_after_id.append("full_name")
    cols_after_id += domain_cols + ["MPI", "risk"]
    
    final_cols = ["id_institution", "uuidv5"] + cols_after_id

    return out[final_cols]



# %%
