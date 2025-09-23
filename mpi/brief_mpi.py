# %%
import numpy as np
import pandas as pd
# %%

df = pd.read_csv("../data/SMSAp/lake/mpiFinal.csv")#.drop("Unnamed: 0")
df.head()
# %%
# --------------------------
# Constantes de Classificação
# --------------------------
RISK_LEVEL_1 = "Leve (MPI 1)"
RISK_LEVEL_2 = "Moderado (MPI 2)"
RISK_LEVEL_3 = "Alto (MPI 3)"

RISK_LABELS = {
    1: RISK_LEVEL_1,
    2: RISK_LEVEL_2,
    3: RISK_LEVEL_3
}

# --------------------------
# Funções auxiliares
# --------------------------

def _safe_col(df, name, default=np.nan, dtype=int):
    """Retorna coluna se existir, senão série com valor padrão e tipo desejado."""
    return df[name] if name in df.columns else pd.Series([default] * len(df), index=df.index, dtype=dtype)

def _normalize_score(value, thresholds):
    """Normaliza valor para 0, 0.5 ou 1 com base em thresholds (tupla de 3 valores)."""
    if value >= thresholds[2]:
        return 1.0
    elif value >= thresholds[1]:
        return 0.5
    else:
        return 0.0

# --------------------------
# Função de cálculo vetorizado
# --------------------------
def calcular_brief_mpi(df, keep_raw=False):
    """Calcula MPI normalizado e risco com base nos domínios do Brief MPI adapatado."""
    out = pd.DataFrame(index=df.index)

    # IDs
    for col in ['id_institution', 'uuidv5', 'full_name']:
        out[col] = _safe_col(df, col)

    # Social
    sex = _safe_col(df, "sex").fillna(0).astype(int)
    race = _safe_col(df, "race").fillna(0).astype(int)
    education = _safe_col(df, "education").fillna(0).astype(int)

    score_social_raw = (
        (sex.map({1: 0, 2: 1}).fillna(0)) +
        (race.apply(lambda x: 0 if x in [1, 4] else 1)) +
        (education.apply(lambda x: 1 if x in [1, 2] else 0))
    )
    score_social = score_social_raw.map(lambda x: _normalize_score(x, (0, 1, 3)))

    # ABVD
    basic = _safe_col(df, "basic_activities_diffic").map({1: 0, 2: 1}).fillna(0).astype(int)
    phys1 = _safe_col(df, "physical_desabilities___1").fillna(0).astype(int)
    phys2 = _safe_col(df, "physical_desabilities___2").fillna(0).astype(int)

    physical = ((phys1 == 1) | (phys2 == 1)).astype(int)
    score_abvd_raw = basic + physical
    score_abvd = score_abvd_raw.map(lambda x: _normalize_score(x, (0, 1, 2)))

    # Mobility
    mobility = _safe_col(df, "elder_mobility").map({1: 1, 2: 0}).fillna(0)
    difficulties = _safe_col(df, "elder_difficulties").map({1: 0, 2: 1}).fillna(0)
    score_mobility_raw = mobility + difficulties
    score_mobility = score_mobility_raw.map(lambda x: _normalize_score(x, (0, 1, 2)))

    # Falls
    falls = _safe_col(df, "falls_number").fillna(1).astype(int)
    score_falls_raw = np.select(
        [falls == 1, falls == 2, falls >= 3],
        [0, 1, 2],
        default=0
    )
    score_falls = pd.Series(score_falls_raw).map(lambda x: _normalize_score(x, (0, 1, 2)))

    # Inpatient
    inpatient = _safe_col(df, "elder_hospitalized").fillna(0).astype(int)
    score_inpatient = np.select(
        [inpatient == 0, inpatient == 1, inpatient >= 2],
        [0.0, 0.5, 1.0]
    )

    # Nutrition
    strength = _safe_col(df, "elder_strenght").map({1: 1, 2: 0}).fillna(0)
    weight_loss = _safe_col(df, "weight_loss").map({1: 1, 2: 0}).fillna(0)
    amount_loss = _safe_col(df, "amount_weight_loss").apply(lambda x: 2 if x == 2 else (1 if x == 1 else 0))

    nutrition_raw = strength + weight_loss + amount_loss
    nutrition_raw = np.minimum(nutrition_raw, 2)
    score_nutrition = pd.Series(nutrition_raw).map(lambda x: _normalize_score(x, (0, 1, 2)))

    # Comorbidity
    comorb = _safe_col(df, "soma_morbidities").fillna(0).astype(int)
    score_comorb = np.select(
        [comorb >= 3, comorb >= 1, comorb == 0],
        [1.0, 0.5, 0.0]
    )

    # Drugs
    drugs = _safe_col(df, "qtd_medic_vaz").fillna(0).astype(int)
    score_drugs = np.select(
        [drugs >= 7, drugs >= 4, drugs < 4],
        [1.0, 0.5, 0.0]
    )

    # Nursing Home
    nursing = _safe_col(df, "institut_time_years").fillna(0).astype(float)
    score_nursing = np.select(
        [nursing >= 5, (nursing >= 3) & (nursing < 5), nursing < 3],
        [1.0, 0.5, 0.0]
    )

    # Agrupar scores
    domain_scores = {
        "score_social": score_social,
        "score_abvd": score_abvd,
        "score_mobility": score_mobility,
        "score_falls": score_falls,
        "score_inpatient": score_inpatient,
        "score_nutrition": score_nutrition,
        "score_comorb": score_comorb,
        "score_drugs": score_drugs,
        "score_nursing": score_nursing,
    }

    for key, value in domain_scores.items():
        out[key] = value

    # Calcular MPI
    out["MPI"] = out[list(domain_scores.keys())].mean(axis=1).round(2)

    # Classificação de risco
    out["risk"] = np.select(
        [out["MPI"] <= 0.33, out["MPI"] <= 0.66],
        [RISK_LEVEL_1, RISK_LEVEL_2],
        default=RISK_LEVEL_3
    )

    # Manter valores brutos se solicitado
    if keep_raw:
        out["social_raw"] = score_social_raw
        out["abvd_raw"] = score_abvd_raw
        out["mobility_raw"] = score_mobility_raw
        out["falls_raw"] = score_falls_raw
        out["nutrition_raw"] = nutrition_raw
        out["comorb_raw"] = comorb
        out["drugs_raw"] = drugs
        out["nursing_raw"] = nursing
        out["inpatient_raw"] = inpatient

    return out

# %%

df_score = calcular_brief_mpi(df, keep_raw=True)
# %%
df_score
# %%
