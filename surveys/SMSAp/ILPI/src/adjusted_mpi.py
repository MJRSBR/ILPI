#from typing import Iterable, Optional, Union, Dict, Any
#
#def _sum01(values: Iterable[Optional[Union[int, bool]]], missing_as_zero: bool = True) -> int:
#    """Soma itens codificados em 0/1 (ou False/True). Pode tratar None como 0 ou ignorar."""
#    total = 0
#    for v in values:
#        if v is None:
#            if missing_as_zero:
#                v = 0
#            else:
#                continue
#        total += int(bool(v))
#    return total
#
#def _map_domain(total: int, mapping: str) -> float:
#    """
#    Converte o total do domínio no valor 0 / 0.5 / 1 conforme a tabela Brief-MPI.
#    mapping ∈ {'adl','iadl','mobility','cognitive','nutrition','comorbidity','drugs','cohab'}
#    """
#    if mapping in ('adl', 'iadl'):
#        if total == 3: return 0.0
#        if total in (1, 2): return 0.5
#        return 1.0                           # total == 0
#    elif mapping == 'mobility':
#        if total >= 2: return 0.0            # 3–2
#        if total == 1: return 0.5
#        return 1.0                           # 0
#    elif mapping in ('cognitive', 'nutrition'):
#        if total == 0: return 0.0
#        if total == 1: return 0.5
#        return 1.0                           # 2–3
#    elif mapping == 'comorbidity':
#        if total == 0: return 0.0
#        if total in (1, 2): return 0.5
#        return 1.0                           # ≥3
#    elif mapping == 'drugs':
#        if total <= 3: return 0.0
#        if 4 <= total <= 6: return 0.5
#        return 1.0                           # ≥7
#    elif mapping == 'cohab':
#        # aceita códigos 0/1/2 ou strings
#        if isinstance(total, str):
#            t = total.strip().lower()
#            if t in ('with family', 'family', 'família', 'com família'): return 0.0
#            if t in ('institution', 'instituição'): return 0.5
#            if t in ('alone', 'sozinho', 'sozinha'): return 1.0
#            raise ValueError("cohabitation string não reconhecida")
#        else:
#            # conforme a sua tabela: Alone(0), With Family(1), Institution(2)
#            if total == 1: return 0.0        # With Family
#            if total == 2: return 0.5        # Institution
#            if total == 0: return 1.0        # Alone
#            raise ValueError("cohabitation code deve ser 0, 1 ou 2")
#    else:
#        raise ValueError("mapping desconhecido")
#
#def compute_brief_mpi(
#    adl_items: Iterable[Optional[Union[int, bool]]],
#    iadl_items: Iterable[Optional[Union[int, bool]]],
#    mobility_items: Iterable[Optional[Union[int, bool]]],
#    cognitive_items: Iterable[Optional[Union[int, bool]]],
#    nutritional_items: Iterable[Optional[Union[int, bool]]],
#    comorbidities_count: int,
#    drug_count: int,
#    cohabitation: Union[int, str],
#    missing_as_zero: bool = True,
#    round_ndigits: int = 2
#) -> Dict[str, Any]:
#    """
#    Calcula o Brief-MPI.
#
#    Convenções dos itens:
#      - ADL/IADL/Mobility: 1(True)=capaz/independente; 0(False)=não.
#      - Cognitive/Nutrition: 1(True)=problema/erro/risco presente; 0(False)=ausente.
#      - comorbidities_count: nº de doenças crônicas em tratamento.
#      - drug_count: nº de princípios ativos em uso.
#      - cohabitation: 0=Alone, 1=With Family, 2=Institution, ou string equivalente.
#      - missing_as_zero: se False, None é ignorado na soma (preferível preencher todos os 3 itens).
#
#    Retorna: dicionário com totais dos domínios, valores (0/0.5/1), MPI e classificação.
#    """
#    adl_total = _sum01(adl_items, missing_as_zero)
#    iadl_total = _sum01(iadl_items, missing_as_zero)
#    mobility_total = _sum01(mobility_items, missing_as_zero)
#    cognitive_total = _sum01(cognitive_items, missing_as_zero)
#    nutri_total = _sum01(nutritional_items, missing_as_zero)
#
#    vals = {
#        'ADL_value': _map_domain(adl_total, 'adl'),
#        'IADL_value': _map_domain(iadl_total, 'iadl'),
#        'Mobility_value': _map_domain(mobility_total, 'mobility'),
#        'Cognitive_value': _map_domain(cognitive_total, 'cognitive'),
#        'Nutritional_value': _map_domain(nutri_total, 'nutrition'),
#        'Comorbidity_value': _map_domain(int(comorbidities_count), 'comorbidity'),
#        'Drug_value': _map_domain(int(drug_count), 'drugs'),
#        'Cohabitation_value': _map_domain(cohabitation, 'cohab'),
#    }
#
#    mpi_raw = sum(vals.values()) / 8.0
#    mpi = round(mpi_raw, round_ndigits)
#
#    if mpi <= 0.33:
#        risk = 'Mild (MPI 1)'
#    elif mpi <= 0.66:
#        risk = 'Moderate (MPI 2)'
#        # nota: 0.66 entra em Moderado como na sua legenda
#    else:
#        risk = 'High (MPI 3)'
#
#    return {
#        'totals': {
#            'ADL': adl_total,
#            'IADL': iadl_total,
#            'Mobility': mobility_total,
#            'Cognitive': cognitive_total,
#            'Nutritional': nutri_total,
#            'Comorbidities': int(comorbidities_count),
#            'Drugs': int(drug_count),
#            'Cohabitation': cohabitation,
#        },
#        'values': vals,
#        'MPI': mpi,
#        'MPI_raw': mpi_raw,
#        'risk': risk,
#    }

# %%
import pandas as pd
#from funcoes.f_process import extrair_medicamentos #, classificar_risco,  extrair_morbidades

# def extrair_medicamentos(df):
#     import pandas as pd
#     """
#     Extrai os medicamentos usados por residente, incluindo combinações, com colunas:
#     med_name, dosage, taken_daily. Cada linha representa 1 medicamento.
#     """
#     tomadas_dia = {
#         "1": "1 x ao dia",
#         "2": "2 x ao dia",
#         "3": "3 x ao dia",
#         "4": "4 x ao dia",
#         "5": "semanalmente",
#         "6": "mensalmente",
#         "7": "quinzenalmente"
#     }

#     # Filtra apenas registros do instrumento medicamentos_em_uso
#     df_meds = df[df['redcap_repeat_instrument'] == 'medicamentos_em_uso'].copy()

#     # Propaga os campos-chave
#     campos_chave = ['institution_name', 'full_name', 'cpf']
#     for campo in campos_chave:
#         if df_meds[campo].dtype == object:
#             df_meds[campo] = df_meds[campo].ffill().str.upper()
#         else:
#             df_meds[campo] = df_meds[campo].ffill()

#     registros = []

#     for _, row in df_meds.iterrows():
#         base_info = {
#             'institution_name': row['institution_name'],
#             'full_name': row['full_name'],
#             'cpf': row['cpf']
#         }

#         # Medicamento principal
#         med_name = str(row.get('med_name')).strip().lower() if pd.notnull(row.get('med_name')) else None
#         if med_name:
#             valor_bruto = row.get('taken_daily')
#             taken_daily = None
#             if pd.notnull(valor_bruto):
#                 chave = str(int(valor_bruto)) if not isinstance(valor_bruto, str) else valor_bruto.strip()
#                 taken_daily = tomadas_dia.get(chave)

#             registros.append({
#                 **base_info,
#                 'med_name': med_name,
#                 'dosage': row.get('dosage'),
#                 'taken_daily': taken_daily
#             })

#         # Combinações
#         for i in range(1, 7):
#             comb_col = f'combination_{i}'
#             dose_col = f'combination_dosage_{i}'

#             comb_value = row.get(comb_col)
#             if pd.notnull(comb_value) and str(comb_value).strip():
#                 registros.append({
#                     **base_info,
#                     'med_name': str(comb_value).strip().lower(),
#                     'dosage': row.get(dose_col),
#                     'taken_daily': None
#                 })

#     # Cria DataFrame final
#     df_resultado = pd.DataFrame(registros)

#     # Ordena para melhor leitura
#     df_resultado = df_resultado.sort_values(by=['institution_name', 'full_name', 'cpf'])

#     # # Renomear colunas
#     # df_resultado = df_resultado.rename(columns={
#     #     "institution_name": "ILPI",
#     #     "full_name": "Nome Completo",	
#     #     "cpf": "CPF",	
#     #     "med_name": "Medicamento",	
#     #     "dosage": "Dose",	
#     #     "taken_daily": "Tomadas ao dia"
#     # })

#     return df_resultado

def extrair_medicamentos(df):
    """
    Extrai os medicamentos usados por residentes, com base no instrumento repetido 'medicamentos_em_uso'.
    Retorna um DataFrame com colunas: institution_name, full_name, uuidv5, med_name, dosage, taken_daily.

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
    campos_chave = ['institution_name', 'full_name', 'uuidv5']
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
            'institution_name': row['institution_name'],
            'full_name': row['full_name'],
            'uuidv5': row['uuidv5']
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
    df_resultado = df_resultado.sort_values(by=['institution_name', 'full_name', 'uuidv5'])

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

    campos_chave = ['institution_name', 'full_name', 'uuidv5']
    for campo in campos_chave:
        if df_meds[campo].dtype == object:
            df_meds[campo] = df_meds[campo].ffill().str.upper()
        else:
            df_meds[campo] = df_meds[campo].ffill()

    registros = []
    record_ids_extraidos = set()

    for _, row in df_meds.iterrows():
        base_info = {
            'institution_name': row['institution_name'],
            'full_name': row['full_name'],
            'uuidv5': row['uuidv5']
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
    df_resultado = df_resultado.sort_values(by=['institution_name', 'full_name', 'uuidv5'])

    print("🔍 Estatísticas da extração (incluindo registros vazios):")
    total_record_ids = df[df['redcap_repeat_instrument'] == 'medicamentos_em_uso']['record_id'].nunique()
    print(f"Total de record_id com instrumento: {total_record_ids}")
    print(f"Total de record_id com medicamentos extraídos: {len(record_ids_extraidos)}")
    print(f"Record_ids incluídos: {sorted(record_ids_extraidos)}")

    return df_resultado


df = pd.read_csv("../../../../data/SMSAp/ILPI/base_perfil_epidemiologico.csv",sep=";")

df.head()
# %%
df.shape
# %%

# df_filter = df[df['redcap_repeat_instrument'].isna()]
# df_filter
# %%

# Usar a funçao para montar uma tabela com os medicamentos
medic = extrair_medicamentos(df)

# Gerando tabela dos registros perdidos
ids_perdidos = [3, 130, 152, 169]
df[df['record_id'].isin(ids_perdidos) & (df['redcap_repeat_instrument'] == 'medicamentos_em_uso')]
# %%
medic
# %%
medic_vaz = extrair_medicamentos_incluindo_vazios(df)
# %%
medic_vaz
#%%
qtd_medic = medic.groupby(["institution_name", "full_name", "uuidv5"]).size().reset_index(name="qtd_medic")
qtd_medic
# %%
qtd_medic_vaz = medic_vaz.groupby(["institution_name", "full_name", "uuidv5"]).size().reset_index(name="qtd_medic_vaz")
qtd_medic_vaz
# %%

qtd_medic_vaz.to_csv('../../../../data/SMSAp/lake/QtdeMedicTot.csv')

# %%

residente = pd.read_csv("../../../../data/SMSAp/lake/Residente.csv")
mobilidade = pd.read_csv("../../../../data/SMSAp/lake/grau_dependencia.csv")
nutricional = pd.read_csv("../../../../data/SMSAp/lake/****.csv")
comorbidades = pd.read_csv("../../../../data/SMSAp/lake/Morbidades.csv")
medicamentos = pd.read_csv("../../../../data/SMSAp/lake/QtdeMedicTot.csv")


# %%
tabela = (
    residente
    .merge(residente, how='left', on='uuidv5')
    .merge(mobilidade, how='left', on='uuidv5')
    .merge(nutricional, how='left', on='uuidv5')
    .merge(comorbidades, how='left', on='uuidv5')
    .reset_index(drop=True)
)
# %%
