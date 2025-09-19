
# %%
import sys
sys.path.append('/Users/mjrs/Library/CloudStorage/OneDrive-Pessoal/UFG/Projeto_VIDAEPAUTA/Códigos/ILPI')

# %%

import pandas as pd


from funcoes.f_plot import salvar_tabela_como_imagem
from funcoes.f_process import classificar_risco
# %%
# ---------------------
# Leitura dos dados
# ---------------------

import pandas as pd
df = pd.read_csv("../../../../data/SMSAp/lake/mpiFinal.csv")#.drop("Unnamed: 0")
df.head()
# %%
## --------------------
##  - COMPONENTES DE FRAGILIDADE
# ## --------------------

# # fragilidade_dic = {
# #     'amount_weight_loss':'Perda de Peso',
# #     'elder_strenght':(lambda x: x == 2),
# #     'elder_hospitalized':(lambda x: x ==1),
# #     'elder_difficulties':(lambda x: x == 1),
# #     'elder_mobility':(lambda x: x == 2),
# #     'basic_activities_diffic':(lambda x: x ==1),
# #     'falls_number':(lambda x: x ==1)
# # }

# # #amount_weight_loss_dict ={1: "de 1 a 3 kg",2: "mais de 3 kg",}
# # #elder_strenght_dict = {1:"Sim",2:"Não"}	
# # #elder_hospitalized_dict = {1: "nenhuma", 2: "1 a 2 vezes", 3: "3 vezes", 4: "4 ou mais",}
# # #elder_difficulties_dict = {1:"nenhuma", 2: "alguma",3: "não consegue",}
# # #elder_mobility_dict = {1: "Sim",2: "Não"}	
# # #basic_activities_diffic_dict = 	{1:	"Sim",2: "Não"}	
# # #falls_number_dict = {1: " nenhuma", 2: "1 a 3 quedas", 3: "4 e mais",}

# # # %%

# def extrair_comp_fragilidade(df, nome_coluna_soma='soma_fragilidades'):
#     """
#     Filtra e retorna os dados de componentes de fragilidade,
#     agrupados por id_institution, full_name, uuidv5.

#     Parâmetros:
#     - df: DataFrame.
#     - fragilidade_dict: dict, mapeamento de código -> texto.
#     - nome_coluna_soma: str, nome da coluna soma (Se None, usa 'soma_morbidities').

#     Retorna:
#     - DataFrame com as morbidades processadas, incluindo:
#       - 'Componentes de Fragilidade': lista de morbidades binárias e textuais.
#       - 'soma_morbidities': soma total de morbidades (binárias + textuais).
#     """
    
#     # # Preenche valores ausentes nas colunas-chave com o valor anterior (forward fill)
#     campos_para_propagacao = ['id_institution', 'uuidv5', 'full_name']
#     for campo in campos_para_propagacao:
#         if campo in df.columns:
#             df[campo] = df[campo].ffill()

#     # Cria colunas de fragilidade binárias com base na lógica de interpretação de cada item
#     df['frag_dependence_degree'] = df['dependence_degree'].apply(lambda x: 1 if x >= 2 else 0)
#     df['frag_amount_weight_loss'] = df['amount_weight_loss'].apply(lambda x: 1 if x == 2 else 0)
#     df['frag_elder_strenght'] = df['elder_strenght'].apply(lambda x: 1 if x == 1 else 0)
#     df['frag_elder_hospitalized'] = df['elder_hospitalized'].apply(lambda x: 1 if x >= 2 else 0)
#     df['frag_elder_difficulties'] = df['elder_difficulties'].apply(lambda x: 1 if x >= 2 else 0)
#     df['frag_elder_mobility'] = df['elder_mobility'].apply(lambda x: 1 if x == 1 else 0)
#     df['frag_basic_activities_diffic'] = df['basic_activities_diffic'].apply(lambda x: 1 if x == 1 else 0)
#     df['frag_falls_number'] = df['falls_number'].apply(lambda x: 1 if x >= 2 else 0)

#     # Lista das colunas binárias de fragilidade
#     frag_cols = [
#         'frag_dependence_degree',
#         'frag_amount_weight_loss',
#         'frag_elder_strenght',
#         'frag_elder_hospitalized',
#         'frag_elder_difficulties',
#         'frag_elder_mobility',
#         'frag_basic_activities_diffic',
#         'frag_falls_number'
#     ]

#     # Mapeia nomes legíveis dos componentes de fragilidade
#     descricao_frag = {
#         'frag_dependence_degree': 'Grau dependência 2 ou 3',
#         'frag_amount_weight_loss': 'Perda de peso > 3kg',
#         'frag_elder_strenght': 'Fraqueza percebida',
#         'frag_elder_hospitalized': 'Internação recente',
#         'frag_elder_difficulties': 'Dificuldade ou incapacidade para levantar',
#         'frag_elder_mobility': 'Caminhada mais lenta',
#         'frag_basic_activities_diffic': 'Dificuldades em atividades diárias',
#         'frag_falls_number': 'Quedas frequentes'
#     }


#     # Soma o total de fragilidades identificadas por linha
#     df['soma_frag'] = df[frag_cols].sum(axis=1)

#     # Gera uma descrição textual dos componentes de fragilidade presentes em cada linha
#     def listar_componentes(row):
#         return ', '.join([descricao_frag[col] for col in frag_cols if row[col] == 1])
#     # Aplica a função acima a cada linha do DataFrame
#     df['Componentes de Fragilidade'] = df.apply(listar_componentes, axis=1)

#     # Função remove espaços extras e divide corretamente, evitando vírgulas sobrando
#     def agrupar_componentes(lista):
#         componentes = set()  # cria um conjunto vazio
#         for item in lista:
#             # Divide a string por vírgula, remove espaços e ignora valores vazios
#             partes = [s.strip() for s in item.split(',') if s.strip()]
#             # adiciona cada pedaço no conjunto
#             for parte in partes:
#                 componentes.add(parte) 
#         # converte o conjunto para lista e junta numa string separada por vírgula
#         return ', '.join(sorted(componentes))

#     # Agrupa os dados por indivíduo e instituição e resume os componentes e a soma
#     resultado = df.groupby(['id_institution', 'uuidv5', 'full_name'], as_index=False).agg({
#         'Componentes de Fragilidade': agrupar_componentes,
#         'soma_frag': 'sum'
#     })

#     # Renomeia a coluna de soma, se for fornecido um nome alternativo
#     resultado = resultado.rename(columns={
#         'soma_frag': nome_coluna_soma
#     })

#     # Ordena os resultados por instituição, nome e uuidv5
#     resultado = resultado.sort_values(by=['id_institution', 'uuidv5', 'full_name'])

#     return resultado

# # %%

# # Extrai os componentes de fragilidade dos residentes
# comp_fragilidade = extrair_comp_fragilidade(df)
# comp_fragilidade

# # %%
# # Fazendo o merge tabelas
# # *****************.   PRECISA VERIFICAR AS TABELAS MERGE *************************
# # Agrupar tabelas de interesse 

# #df_score = df_morbidades(contagem_medic_por_residente, how='rigth')
# # %%
# df_score = df_morbidades.merge(comp_fragilidade, how='right')
# df_score

# # %%
# #amount_weight_loss_dict ={1: "de 1 a 3 kg",2: "mais de 3 kg",}
# #elder_strenght_dict = {1:"Sim",2:"Não"}	
# #elder_hospitalized_dict = {1: "nenhuma", 2: "1 a 2 vezes", 3: "3 vezes", 4: "4 ou mais",}
# #elder_difficulties_dict = {1:"nenhuma", 2: "alguma",3: "não consegue",}
# #elder_mobility_dict = {1: "Sim",2: "Não"}	
# #basic_activities_diffic_dict = 	{1:	"Sim",2: "Não"}	
# #falls_number_dict = {1: " nenhuma", 2: "1 a 3 quedas", 3: "4 e mais",}

# ##*********************. EXEMPLO NECESSITA DEFINIR OS PARAMETROS  ************************
# condicao_atencao = {
#     'amount_weight_loss':(lambda x: x == 1),
#     'elder_strenght':(lambda x: x == 2),
#     'elder_hospitalized':(lambda x: x ==1),
#     'elder_difficulties':(lambda x: x == 1),
#     'elder_mobility':(lambda x: x == 2),
#     'basic_activities_diffic':(lambda x: x ==1),
#     'falls_number':(lambda x: x ==1)
# }

# condicao_alerta = {
#     'amount_weight_loss':(lambda x: x == 1),
#     'elder_strenght':(lambda x: x == 1),
#     'elder_hospitalized':(lambda x: x in [2, 3] ),
#     'elder_difficulties':(lambda x: x == 2),
#     'elder_mobility':(lambda x: x == 1),
#     'basic_activities_diffic':(lambda x: x == 1),
#     'falls_number':(lambda x: x == 2)
# }

# condicao_critica = {
#     'amount_weight_loss':(lambda x: x == 2),
#     'elder_strenght':(lambda x: x == 1),
#     'elder_hospitalized':(lambda x: x in [3, 4]),
#     'elder_difficulties':(lambda x: x == 1),
#     'elder_mobility':(lambda x: x == 1),
#     'basic_activities_diffic':(lambda x: x ==1),
#     'falls_number':(lambda x: x == 3)
# }

# # %%


# # # %%

# # #condicao_atencao = {
# # #    'elder_age': (lambda x: x < 70),
# # #    'soma_morbidities': (lambda x: x <= 3),
# # #    'soma_fragilidades': (lambda x: x in [2, 3]),
# # #
# # #}
# # #
# # #condicao_alerta = {
# # #    'elder_age': (lambda x: x > 70 & x < 80),
# # #    'soma_morbidities': (lambda x: x in [4, 5] ),
# # #    'soma_fragilidades': (lambda x: x in [3, 4]),
# # #    
# # #}
# # #
# # #condicao_critica = {
# # #    'elder_age': (lambda x: x >= 81),
# # #    'soma_morbidities': (lambda x: x >= 6),
# # #    'soma_fragilidades': (lambda x: x>= 4),
# # #    
# # #}

# # # %%
# # resultado, resumo = classificar_risco(df, condicao_critica, condicao_alerta, condicao_atencao)

# # # %%
# # from IPython.display import display, HTML

# # # Exibe o resultado com cores
# # display(HTML(resultado.to_html(escape=False)))

# # # Mostra o resumo correto
# # display(HTML(resumo.to_html(escape=False)))

# # # %%
# # salvar_tabela_como_imagem(
# #     resumo,
# #     '../tables/13_tabela_resumo_score_fragilidade.png',
# #     titulo='Score de Fragilidade do Residente por ILPI',
# #     largura_max_coluna=25
# # )
# # # %%
# # df.head()
# # # %%

# from typing import Iterable, Optional, Union, Dict, Any

# def _sum01(values: Iterable[Optional[Union[int, bool]]], missing_as_zero: bool = True) -> int:
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

# # def _map_domain(total: int, mapping: str) -> float:
# #    """
# #    Converte o total do domínio no valor 0 / 0.5 / 1 conforme a tabela Brief-MPI.
# #    mapping ∈ {'adl','iadl','mobility','cognitive','nutrition','comorbidity','drugs','cohab'}
# #    """
# #    if mapping in ('adl', 'iadl'):
# #        if total == 3: return 0.0
# #        if total in (1, 2): return 0.5
# #        return 1.0                           # total == 0
# #    elif mapping == 'mobility':
# #        if total >= 2: return 0.0            # 3–2
# #        if total == 1: return 0.5
# #        return 1.0                           # 0
# #    elif mapping in ('cognitive', 'nutrition'):
# #        if total == 0: return 0.0
# #        if total == 1: return 0.5
# #        return 1.0                           # 2–3
# #    elif mapping == 'comorbidity':
# #        if total == 0: return 0.0
# #        if total in (1, 2): return 0.5
# #        return 1.0                           # ≥3
# #    elif mapping == 'drugs':
# #        if total <= 3: return 0.0
# #        if 4 <= total <= 6: return 0.5
# #        return 1.0                           # ≥7
# # #    elif mapping == 'cohab':
# # #        # aceita códigos 0/1/2 ou strings
# # #        if isinstance(total, str):
# # #            t = total.strip().lower()
# # #            if t in ('with family', 'family', 'família', 'com família'): return 0.0
# # #            if t in ('institution', 'instituição'): return 0.5
# # #            if t in ('alone', 'sozinho', 'sozinha'): return 1.0
# # #            raise ValueError("cohabitation string não reconhecida")
# # #        else:
# # #            # conforme a sua tabela: Alone(0), With Family(1), Institution(2)
# # #            if total == 1: return 0.0        # With Family
# # #            if total == 2: return 0.5        # Institution
# # #            if total == 0: return 1.0        # Alone
# # #            raise ValueError("cohabitation code deve ser 0, 1 ou 2")
# #    else:
# #        raise ValueError("mapping desconhecido")



# # %%

# def compute_brief_mpi(
#    social_marks: Iterable[Optional[Union[int, bool]]],
#    abvd_items: Iterable[Optional[Union[int, bool]]],
#    mobility_items: Iterable[Optional[Union[int, bool]]],
#    falls: Iterable[Optional[Union[int, bool]]],
#    inpatient: Iterable[Optional[Union[int, bool]]],
#    nutritional_items: Iterable[Optional[Union[int, bool]]],
#    comorbidities_count: int,
#    drug_count: int,
#    #cohabitation: Union[int, str],
#    nursing_home: int,
#    missing_as_zero: bool = True,
#    round_ndigits: int = 2
# ) -> Dict[str, Any]:
#    """
#    Calcula o Brief-MPI.

#    Convenções dos itens:
#      - ADL/IADL/Mobility: 1(True)=capaz/independente; 0(False)=não.
#      - Cognitive/Nutrition: 1(True)=problema/erro/risco presente; 0(False)=ausente.
#      - comorbidities_count: nº de doenças crônicas em tratamento.
#      - drug_count: nº de princípios ativos em uso.
#      - cohabitation: 0=Alone, 1=With Family, 2=Institution, ou string equivalente.
#      - missing_as_zero: se False, None é ignorado na soma (preferível preencher todos os 3 itens).

#    Retorna: dicionário com totais dos domínios, valores (0/0.5/1), MPI e classificação.
#    """
#    social_marks_total = _sum01(social_marks, missing_as_zero)
#    abvd_total = _sum01(abvd_items, missing_as_zero)
#    mobility_total = _sum01(mobility_items, missing_as_zero)
#    falls_total = _sum01(falls, missing_as_zero)
#    inpatient_total = _sum01(inpatient, missing_as_zero)
#    nutri_total = _sum01(nutritional_items, missing_as_zero)
#    comorbidities =  _sum01(comorbidities_count, missing_as_zero)
#    drugs = _sum01(drug_count, missing_as_zero)
#    nursing = _sum01(nursing_home, missing_as_zero)
 
#    vals = {
#        'Social_value': _map_domain(social_marks_total, 'social'),
#        'ABVD_value': _map_domain(abvd_total, 'abvd'),
#        'Mobility_value': _map_domain(mobility_total, 'mobility'),
#        'Falls_value': _map_domain(falls_total, 'falls'),
#        'Inpatient': _map_domain(inpatient_total, 'inpatient'),
#        'Nutritional_value': _map_domain(nutri_total, 'nutrition'),
#        'Comorbidity_value': _map_domain(int(comorbidities), 'comorbidity'),
#        'Drug_value': _map_domain(int(drugs), 'drugs'),
#        'Nursing_value': _map_domain(int(nursing), 'nursing home'),
#    }

#    mpi_raw = sum(vals.values()) / 9.0
#    mpi = round(mpi_raw, round_ndigits)

#    if mpi <= 0.33:
#        risk = 'Leve (MPI 1)'
#    elif mpi <= 0.66:
#        risk = 'Moderado (MPI 2)'
#        # nota: 0.66 entra em Moderado como na sua legenda
#    else:
#        risk = 'Alto (MPI 3)'

#    return {
#        'totals': {
#            'Social': social_marks_total,
#            'ABVD': abvd_items,
#            'Mobility': mobility_total,
#            'Falls': falls_total,
#            'Nutritional': nutri_total,
#            'Comorbidities': int(comorbidities),
#            'Drugs': int(drugs),
#            'Nursing Home': nursing,
#        },
#        'values': vals,
#        'MPI': mpi,
#        'MPI_raw': mpi_raw,
#        'risk': risk,
#    }




# # %%

# import pandas as pd

# # # Exemplo de dicionário de mapeamento das colunas do REDCap → parâmetros da função
# # COLUMN_MAP = {
# #     "adl_items": ["adl_1", "adl_2", "adl_3"],
# #     "iadl_items": ["iadl_1", "iadl_2", "iadl_3"],
# #     "mobility_items": ["mob_1", "mob_2", "mob_3"],
# #     "cognitive_items": ["cog_1", "cog_2", "cog_3"],
# #     "nutritional_items": ["nutri_1", "nutri_2", "nutri_3"],
# #     "comorbidities_count": "comorb_count",
# #     "drug_count": "drug_count",
# #     "cohabitation": "cohab",
# # }

# # Exemplo de dicionário de mapeamento das colunas do REDCap → parâmetros da função

# ########PAREI AQUI

# COLUMN_MAP = {
#     "social_marks": ["sex", "race", "education"],
#     "abvd_items": ['basic_activities_diffic'],
#     "mobility_items": ["physical_desabilities___1","physical_desabilities___2",
#                        "physical_desabilities___3","elder_mobility","elder_difficulties"],
#     "fall": "falls_number",
#     "#inpatient": "institut_time_years",                  
#     "nutritional_items": ["elder_strenght","weight_loss","amount_weight_loss"],
#     "comorbidities_count": "soma_morbidities",
#     "drug_count": "qtd_medic_vaz",
#     "nursing_home": "institut_time_years"
    
# }


# def aplicar_brief_mpi(df: pd.DataFrame, col_map: dict = COLUMN_MAP) -> pd.DataFrame:
#     """
#     Aplica o cálculo do Brief-MPI linha a linha no DataFrame do REDCap.
#     Retorna um novo DataFrame com as colunas originais + resultados MPI.
#     """
#     resultados = []

#     for _, row in df.iterrows():
#         kwargs = {
#             "social_marks": [row[c] for c in col_map['social_marks']],
#             "abvd_items": [row[c] for c in col_map["abvd_items"]],
#             "mobility_items": [row[c] for c in col_map["mobility_items"]],
#             "falls": [row[c] for c in col_map["fall"]],
#             "inpatient": [row[c] for c in col_map["inpatient"]],
#             "nutritional_items": [row[c] for c in col_map["nutritional_items"]],
#             "comorbidities_count": row[col_map["comorbidities_count"]],
#             "drug_count": row[col_map["drug_count"]],
#             "nurse_home": row[col_map["nurse_home"]],
#         }

#         result = compute_brief_mpi(**kwargs)
#         resultados.append(result)

#     # transformar lista de dicts em DataFrame
#     df_resultados = pd.json_normalize(resultados)

#     # concatenar resultados ao DataFrame original
#     df_final = pd.concat([df.reset_index(drop=True), df_resultados], axis=1)
#     return df_final


# # %%

# def _map_domain(total: int, mapping: str) -> float:
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
# #    elif mapping == 'cohab':
# #        # aceita códigos 0/1/2 ou strings
# #        if isinstance(total, str):
# #            t = total.strip().lower()
# #            if t in ('with family', 'family', 'família', 'com família'): return 0.0
# #            if t in ('institution', 'instituição'): return 0.5
# #            if t in ('alone', 'sozinho', 'sozinha'): return 1.0
# #            raise ValueError("cohabitation string não reconhecida")
# #        else:
# #            # conforme a sua tabela: Alone(0), With Family(1), Institution(2)
# #            if total == 1: return 0.0        # With Family
# #            if total == 2: return 0.5        # Institution
# #            if total == 0: return 1.0        # Alone
# #            raise ValueError("cohabitation code deve ser 0, 1 ou 2")
#    else:
#        raise ValueError("mapping desconhecido")
   


# # %%

# df.columns.tolist()
# # %%
# df['elder_mobility']

# # %%
# def combinar_colunas_dict(df, combinacoes):
#     """
#     Cria novas colunas combinadas mantendo os valores originais das colunas de referência.
#     Cada nova célula será um dicionário {coluna: valor}.
#     """
#     df_resultado = df.copy()

#     for nova_col, cols in combinacoes.items():
#         df_resultado[nova_col] = df_resultado[cols].apply(lambda row: row.to_dict(), axis=1)

#     return df_resultado

# combinacoes = {
#     "mobilidade": [
#         "elder_strenght",
#         "elder_difficulties",
#         "elder_mobility",
#         "basic_activities_diffic",
#         "falls_number"
#     ]
# }

# df_mobil = combinar_colunas_dict(df, combinacoes)
# df_mobil 
# # %%
# df_mobil["mobilidade"]
# # %%


# df_resultado = aplicar_brief_mpi(df)
# print(df_resultado[["MPI", "risk"]])
# # %%

# df_score = compute_brief_mpi(df)
# df_score
# # %%


# def compute_brief_mpi(
#     social_marks: Iterable[Optional[Union[int, bool]]],
#     abvd_items: Iterable[Optional[Union[int, bool]]],
#     mobility_items: Iterable[Optional[Union[int, bool]]],
#     falls: Iterable[Optional[Union[int, bool]]],
#     inpatient: Iterable[Optional[Union[int, bool]]],
#     nutritional_items: Iterable[Optional[Union[int, bool]]],
#     comorbidities_count: int,
#     drug_count: int,
#     nursing_home: int,
#     missing_as_zero: bool = True,
#     round_ndigits: int = 2
# ) -> Dict[str, Any]:
#     """
#     Calcula o Brief-MPI adaptado.
#     """

#     # Somatórios para domínios baseados em itens
#     social_total = _sum01(social_marks, missing_as_zero)
#     abvd_total = _sum01(abvd_items, missing_as_zero)
#     mobility_total = _sum01(mobility_items, missing_as_zero)
#     falls_total = _sum01(falls, missing_as_zero)
#     inpatient_total = _sum01(inpatient, missing_as_zero)
#     nutri_total = _sum01(nutritional_items, missing_as_zero)

#     # Variáveis que já são contagens absolutas
#     comorbidities = int(comorbidities_count)
#     drugs = int(drug_count)
#     nursing = int(nursing_home)

#     vals = {
#         'Social_value': _map_domain(social_total, 'social'),
#         'ABVD_value': _map_domain(abvd_total, 'abvd'),
#         'Mobility_value': _map_domain(mobility_total, 'mobility'),
#         'Falls_value': _map_domain(falls_total, 'falls'),
#         'Inpatient_value': _map_domain(inpatient_total, 'inpatient'),
#         'Nutritional_value': _map_domain(nutri_total, 'nutrition'),
#         'Comorbidity_value': _map_domain(comorbidities, 'comorbidity'),
#         'Drug_value': _map_domain(drugs, 'drugs'),
#         'Nursing_value': _map_domain(nursing, 'nursing home'),
#     }

#     mpi_raw = sum(vals.values()) / 9.0
#     mpi = round(mpi_raw, round_ndigits)

#     if mpi <= 0.33:
#         risk = 'Leve (MPI 1)'
#     elif mpi <= 0.66:
#         risk = 'Moderado (MPI 2)'
#     else:
#         risk = 'Alto (MPI 3)'

#     return {
#         'totals': {
#             'Social': social_total,
#             'ABVD': abvd_total,
#             'Mobility': mobility_total,
#             'Falls': falls_total,
#             'Inpatient': inpatient_total,
#             'Nutritional': nutri_total,
#             'Comorbidities': comorbidities,
#             'Drugs': drugs,
#             'Nursing Home': nursing,
#         },
#         'values': vals,
#         'MPI': mpi,
#         'MPI_raw': mpi_raw,
#         'risk': risk,
#     }

# %%

import pandas as pd

# ------------------------
# Funções de escore
# ------------------------
def score_sex(value):
    return 0 if value == 1 else 1 if value == 2 else 0

def score_race(value):
    return 0 if value in [1, 4] else 1

def score_education(value):
    return 1 if value in [1, 2] else 0

def score_basic_activities(value):
    return 0 if value == 1 else 1 if value == 2 else 0

def score_physical_disabilities(values):
    score = 0
    if values[0] == 1:  # ___1
        score += 1
    if values[1] == 1:  # ___2
        score += 1
    if values[2] == 1:  # ___3 → sempre 0
        score += 0
    return score

def score_elder_mobility(value):
    return 1 if value == 1 else 0

def score_elder_difficulties(value):
    return 0 if value == 1 else 1 if value == 2 else 0

def score_falls(value):
    if value == 1:
        return 0
    elif value in [2, 3]:
        return 1
    return 0

def score_inpatient(value):
    return 0 if value == 1 else 1

def score_strength(value):
    return 1 if value == 1 else 0

def score_weight_loss(value):
    return 1 if value == 1 else 0

def score_amount_weight_loss(value):
    if value == 1:
        return 1
    elif value == 2:
        return 2
    return 0

# ------------------------
# Função principal
# ------------------------
def compute_brief_mpi(
    social_marks, abvd_items, mobility_items,
    falls, inpatient, nutritional_items,
    comorbidities_count, drug_count, nursing_home
):
    # Social
    sex, race, education = social_marks
    score_social = (
        score_sex(sex) +
        score_race(race) +
        score_education(education)
    )

    # ABVD
    basic_act = score_basic_activities(abvd_items[0])
    phys_disab = score_physical_disabilities(abvd_items[1:4])
    score_abvd = basic_act + phys_disab

    # Mobility
    mobility = score_elder_mobility(mobility_items[0])
    difficulties = score_elder_difficulties(mobility_items[1])
    score_mobility = mobility + difficulties

    # Falls
    score_falls_ = score_falls(falls[0])

    # Inpatient
    score_inpatient_ = score_inpatient(inpatient[0])

    # Nutrition
    strength = score_strength(nutritional_items[0])
    weight_loss = score_weight_loss(nutritional_items[1])
    amount_loss = score_amount_weight_loss(nutritional_items[2])
    score_nutrition = strength + weight_loss + amount_loss

    # Outros domínios (contagens diretas)
    score_comorb = comorbidities_count
    score_drugs = drug_count
    score_nursing = nursing_home

    # Total
    total_score = (
        score_social + score_abvd + score_mobility +
        score_falls_ + score_inpatient_ + score_nutrition +
        score_comorb + score_drugs + score_nursing
    )

    # Classificação de risco baseada no total_score normalizado
    mpi_raw = total_score / 9.0
    mpi = round(mpi_raw, 2)

    if mpi <= 0.33:
        risk = "Leve (MPI 1)"
    elif mpi <= 0.66:
        risk = "Moderado (MPI 2)"
    else:
        risk = "Alto (MPI 3)"

    return {
        "score_social": score_social,
        "score_abvd": score_abvd,
        "score_mobility": score_mobility,
        "score_falls": score_falls_,
        "score_inpatient": score_inpatient_,
        "score_nutrition": score_nutrition,
        "score_comorb": score_comorb,
        "score_drugs": score_drugs,
        "score_nursing": score_nursing,
        "total_score": total_score,
        "MPI": mpi,
        "risk": risk
    }

# ------------------------
# Aplicar ao DataFrame
# ------------------------
def aplicar_brief_mpi(df: pd.DataFrame) -> pd.DataFrame:
    resultados = []

    for _, row in df.iterrows():
        result = compute_brief_mpi(
            social_marks=[row["sex"], row["race"], row["education"]],
            abvd_items=[
                row["basic_activities_diffic"],
                row["physical_desabilities___1"],
                row["physical_desabilities___2"],
                row["physical_desabilities___3"]
            ],
            mobility_items=[row["elder_mobility"], row["elder_difficulties"]],
            falls=[row["falls_number"]],
            inpatient=[row["elder_hospitalized"]],
            nutritional_items=[
                row["elder_strenght"],
                row["weight_loss"],
                row["amount_weight_loss"]
            ],
            comorbidities_count=row["soma_morbidities"],
            drug_count=row["qtd_medic_vaz"],
            nursing_home=row["institut_time_years"]
        )
        resultados.append(result)

    df_resultados = pd.DataFrame(resultados)

    # concat original + resultados
    df_final = pd.concat([df.reset_index(drop=True), df_resultados], axis=1)

    # reordenar colunas: id_institution, uuidv5 primeiro
    cols = ["id_institution", "uuidv5"] + [c for c in df_final.columns if c not in ["id_institution", "uuidv5"]]
    df_final = df_final[cols]

    return df_final

# # %%
# df_out = aplicar_brief_mpi(df)
# print(df_out.head()[["id_institution", "uuidv5", "full_name", "total_score", "MPI", "risk"]])

# # %%
# df_out
# # %%

# import pandas as pd
# import numpy as np

# def calcular_scores(df):
#     df_scores = pd.DataFrame()
    
#     # manter a ordem das duas primeiras colunas
#     df_scores["id_institution"] = df["id_institution"]
#     df_scores["uuidv5"] = df["uuidv5"]
    
#     # =========================
#     # 1. Pontuação bruta
#     # =========================
#     df_scores["sex_score"] = df["sex"].map({1: 0, 2: 1})
#     df_scores["race_score"] = df["race"].apply(lambda x: 0 if x in [1, 4] else 1)
#     df_scores["education_score"] = df["education"].apply(lambda x: 1 if x in [1, 2] else 0)

#     df_scores["basic_activities_score"] = df["basic_activities_diffic"].map({1: 0, 2: 1})

#     df_scores["physical_score"] = (
#         df[["physical_desabilities___1", "physical_desabilities___2"]].notna().any(axis=1).astype(int)
#     )
#     df_scores["physical_score"] = df_scores["physical_score"] - df["physical_desabilities___3"].fillna(0).astype(int)

#     df_scores["mobility_score"] = df["elder_mobility"].map({1: 1, 2: 0})
#     df_scores["difficulties_score"] = df["elder_difficulties"].map({1: 0, 2: 1})

#     df_scores["falls_score"] = df["falls_number"].apply(lambda x: 0 if x == 1 else (1 if x in [2, 3] else np.nan))

#     df_scores["inpatient_score"] = df["elder_hospitalized"].apply(lambda x: 0 if x == 1 else 1)

#     df_scores["strength_score"] = df["elder_strenght"].map({1: 1, 2: 0})
#     df_scores["weight_loss_score"] = df["weight_loss"].map({1: 1, 2: 0})
#     df_scores["amount_weight_loss_score"] = df["amount_weigth_loss"].map({1: 1, 2: 2})

#     # =========================
#     # 2. Normalização por domínio
#     # =========================
#     df_scores["score_social"] = (df_scores["sex_score"] + df_scores["race_score"] + df_scores["education_score"]).apply(
#         lambda x: 1 if x == 3 else (0.5 if x in [1, 2] else 0)
#     )

#     df_scores["score_abvd"] = df_scores["basic_activities_score"].apply(
#         lambda x: 0 if x == 0 else (0.5 if x == 1 else 1)
#     )

#     df_scores["score_mobility"] = df_scores["mobility_score"].apply(
#         lambda x: 0 if x == 0 else (0.5 if x == 1 else 1)
#     )

#     df_scores["score_falls"] = df_scores["falls_score"].apply(
#         lambda x: 0 if x == 0 else (0.5 if x == 1 else 1)
#     )

#     df_scores["score_inpatient"] = df_scores["inpatient_score"].apply(
#         lambda x: 0 if x in [1, 2] else (0.5 if 2 < x < 4 else 1 if x >= 4 else 0)
#     )

#     df_scores["score_nutrition"] = (df_scores["weight_loss_score"] + df_scores["amount_weight_loss_score"]).apply(
#         lambda x: 0 if x == 0 else (0.5 if x == 1 else 1)
#     )

#     df_scores["score_comorb"] = df["comorbidities"].apply(
#         lambda x: 0 if x == 0 else (0.5 if x in [1, 2] else 1)
#     )

#     df_scores["score_drugs"] = df["medications"].apply(
#         lambda x: 0 if x <= 3 else (0.5 if 4 <= x <= 6 else 1)
#     )

#     df_scores["score_nursing_home"] = df["nursing_home"].apply(
#         lambda x: 0 if 0 <= x <= 2 else (0.5 if 3 <= x <= 4 else 1)
#     )

#     return df_scores

# # %%

# teste = calcular_scores(df)
# # %%
# def calcular_scores(df):
#     df_scores = pd.DataFrame()
    
#     # manter a ordem das duas primeiras colunas
#     df_scores["id_institution"] = df["institution_name"]
#     df_scores["uuidv5"] = df["uuidv5"]
    
#     # =========================
#     # 1. Pontuação bruta
#     # =========================
#     df_scores["sex_score"] = df["sex"].map({1: 0, 2: 1})
#     df_scores["race_score"] = df["race"].apply(lambda x: 0 if x in [1, 4] else 1)
#     df_scores["education_score"] = df["education"].apply(lambda x: 1 if x in [1, 2] else 0)

#     df_scores["basic_activities_score"] = df["basic_activities_diffic"].map({1: 0, 2: 1})

#     df_scores["physical_score"] = (
#         df[["physical_desabilities___1", "physical_desabilities___2"]].notna().any(axis=1).astype(int)
#     )
#     df_scores["physical_score"] = df_scores["physical_score"] - df["physical_desabilities___3"].fillna(0).astype(int)

#     df_scores["mobility_score"] = df["elder_mobility"].map({1: 1, 2: 0})
#     df_scores["difficulties_score"] = df["elder_difficulties"].map({1: 0, 2: 1})

#     df_scores["falls_score"] = df["falls_number"].apply(lambda x: 0 if x == 1 else (1 if x in [2, 3] else None))

#     df_scores["inpatient_score"] = df["elder_hospitalized"].apply(lambda x: 0 if x == 1 else 1)

#     df_scores["strength_score"] = df["elder_strenght"].map({1: 1, 2: 0})
#     df_scores["weight_loss_score"] = df["weight_loss"].map({1: 1, 2: 0})
#     df_scores["amount_weight_loss_score"] = df["amount_weigth_loss"].map({1: 1, 2: 2})

#     # =========================
#     # 2. Normalização por domínio
#     # =========================
#     df_scores["score_social"] = (df_scores["sex_score"] + df_scores["race_score"] + df_scores["education_score"]).apply(
#         lambda x: 1 if x == 3 else (0.5 if x in [1, 2] else 0)
#     )

#     df_scores["score_abvd"] = df_scores["basic_activities_score"].apply(
#         lambda x: 0 if x == 0 else (0.5 if x == 1 else 1)
#     )

#     df_scores["score_mobility"] = df_scores["mobility_score"].apply(
#         lambda x: 0 if x == 0 else (0.5 if x == 1 else 1)
#     )

#     df_scores["score_falls"] = df_scores["falls_score"].apply(
#         lambda x: 0 if x == 0 else (0.5 if x == 1 else 1)
#     )

#     df_scores["score_inpatient"] = df["elder_hospitalized"].apply(
#         lambda x: 0 if x in [1, 2] else (0.5 if 3 <= x <= 4 else 1)
#     )

#     df_scores["score_nutrition"] = (df_scores["weight_loss_score"] + df_scores["amount_weight_loss_score"]).apply(
#         lambda x: 0 if x == 0 else (0.5 if x == 1 else 1)
#     )

#     df_scores["score_comorb"] = df["comorbidities"].apply(
#         lambda x: 0 if x == 0 else (0.5 if x in [1, 2] else 1)
#     )

#     df_scores["score_drugs"] = df["medications"].apply(
#         lambda x: 0 if x <= 3 else (0.5 if 4 <= x <= 6 else 1)
#     )

#     df_scores["score_nursing_home"] = df["nursing_home"].apply(
#         lambda x: 0 if 0 <= x <= 2 else (0.5 if 3 <= x <= 4 else 1)
#     )

#     # =========================
#     # 3. Score total (normalizado)
#     # =========================
#     score_cols = [
#         "score_social", "score_abvd", "score_mobility", "score_falls",
#         "score_inpatient", "score_nutrition", "score_comorb", "score_drugs", "score_nursing_home"
#     ]
#     df_scores["score_total"] = df_scores[score_cols].mean(axis=1)

#     return df_scores

# # Aplicar função
# df_scores = calcular_scores(df)
# # %%
# def calcular_scores(df):
#     df_scores = pd.DataFrame()
    
#     # IDs principais
#     df_scores["id_institution"] = df["id_institution"]
#     df_scores["uuidv5"] = df["uuidv5"]

#     # ---- SOCIAL ----
#     df_scores["sex_score"] = df["sex"].map({1: 0, 2: 1})
#     df_scores["race_score"] = df["race"].apply(lambda x: 0 if x in [1, 4] else 1)
#     df_scores["education_score"] = df["education"].apply(lambda x: 1 if x in [1, 2] else 0)

#     df_scores["score_social_raw"] = (
#         df_scores["sex_score"] +
#         df_scores["race_score"] +
#         df_scores["education_score"]
#     )
#     df_scores["score_social"] = df_scores["score_social_raw"].map(
#         {3: 1, 1: 0.5, 2: 0.5, 0: 0}
#     )

#     # ---- ABVD ----
#     df_scores["abvd_score"] = df["basic_activities_diffic"].map({1: 0, 2: 1})
#     df_scores["score_abvd"] = df_scores["abvd_score"].map({0: 0, 1: 0.5, 2: 1})

#     # ---- MOBILIDADE ----
#     df_scores["mobility_score"] = df["elder_mobility"].map({1: 1, 2: 0})
#     df_scores["difficulties_score"] = df["elder_difficulties"].map({1: 0, 2: 1})

#     df_scores["score_mobility_raw"] = (
#         df_scores["mobility_score"] + df_scores["difficulties_score"]
#     )
#     df_scores["score_mobility"] = df_scores["score_mobility_raw"].map(
#         {0: 0, 1: 0.5, 2: 1}
#     )

#     # ---- INTERNAÇÃO ----
#     df_scores["inpatient_score"] = df["elder_hospitalized"].apply(lambda x: 0 if x == 1 else 1)
#     df_scores["score_inpatient"] = df_scores["inpatient_score"].apply(
#         lambda x: 0 if x == 0 else (0.5 if x == 1 else 1)
#     )

#     # ---- QUEDAS ----
#     df_scores["falls_score"] = df["falls_number"].apply(lambda x: 0 if x == 1 else 1)
#     df_scores["score_falls"] = df_scores["falls_score"].map({0: 0, 1: 0.5, 2: 1})

#     # ---- NUTRIÇÃO ----
#     df_scores["strenght_score"] = df["elder_strenght"].map({1: 1, 2: 0})
#     df_scores["weight_loss_score"] = df["weight_loss"].map({1: 1, 2: 0})
#     df_scores["amount_weight_score"] = df["amount_weight_loss"].map({1: 1, 2: 2})

#     df_scores["score_nutrition_raw"] = (
#         df_scores["strenght_score"] +
#         df_scores["weight_loss_score"] +
#         df_scores["amount_weight_score"]
#     )
#     df_scores["score_nutrition"] = df_scores["score_nutrition_raw"].map(
#         {0: 0, 1: 0.5, 2: 1}
#     )

#     return df_scores

# # %%
# df_scores = calcular_scores(df)
# # %%
# df_scores
# # %%
# import pandas as pd

# def calcular_scores(df):
#     df_scores = pd.DataFrame()

#     # IDs principais
#     df_scores["id_institution"] = df["id_institution"]
#     df_scores["uuidv5"] = df["uuidv5"]

#     # ---- SOCIAL ----
#     df_scores["sex_score"] = df["sex"].map({1: 0, 2: 1})
#     df_scores["race_score"] = df["race"].apply(lambda x: 0 if x in [1, 4] else 1)
#     df_scores["education_score"] = df["education"].apply(lambda x: 1 if x in [1, 2] else 0)

#     df_scores["score_social_raw"] = (
#         df_scores["sex_score"] +
#         df_scores["race_score"] +
#         df_scores["education_score"]
#     )
#     df_scores["score_social"] = df_scores["score_social_raw"].map(
#         {3: 1, 2: 0.5, 1: 0.5, 0: 0}
#     )

#     # ---- ABVD ----
#     df_scores["abvd_score"] = df["basic_activities_diffic"].map({1: 0, 2: 1})
#     df_scores["score_abvd"] = df_scores["abvd_score"].map({0: 0, 1: 0.5})

#     # ---- MOBILIDADE ----
#     df_scores["mobility_score"] = df["elder_mobility"].map({1: 1, 2: 0})
#     df_scores["difficulties_score"] = df["elder_difficulties"].map({1: 0, 2: 1})

#     df_scores["score_mobility_raw"] = (
#         df_scores["mobility_score"] + df_scores["difficulties_score"]
#     )
#     df_scores["score_mobility"] = df_scores["score_mobility_raw"].map(
#         {0: 0, 1: 0.5, 2: 1}
#     )

#     # ---- INTERNAÇÃO ----
#     df_scores["inpatient_score"] = df["elder_hospitalized"].apply(lambda x: 0 if x == 1 else 1)
#     df_scores["score_inpatient"] = df_scores["inpatient_score"].map({0: 0, 1: 0.5})

#     # ---- QUEDAS ----
#     df_scores["falls_score"] = df["falls_number"].apply(lambda x: 0 if x == 1 else 1)
#     df_scores["score_falls"] = df_scores["falls_score"].map({0: 0, 1: 0.5})

#     # ---- NUTRIÇÃO ----
#     df_scores["strength_score"] = df["elder_strenght"].map({1: 1, 2: 0})
#     df_scores["weight_loss_score"] = df["weight_loss"].map({1: 1, 2: 0})
#     df_scores["amount_weight_loss_score"] = df["amount_weight_loss"].map({1: 1, 2: 2})

#     df_scores["score_nutrition_raw"] = (
#         df_scores["strength_score"] +
#         df_scores["weight_loss_score"] +
#         df_scores["amount_weight_loss_score"]
#     )
#     df_scores["score_nutrition"] = df_scores["score_nutrition_raw"].map(
#         {0: 0, 1: 0.5, 2: 1, 3: 1}
#     )

#     # ---- COMORBIDADES ----
#     df_scores["comorbidity_score"] = df["soma_morbidities"].apply(
#         lambda x: 0 if x == 0 else (0.5 if x in [1, 2] else 1)
#     )
#     df_scores["score_comorbidity"] = df_scores["comorbidity_score"]

#     # ---- POLIFARMÁCIA ----
#     df_scores["drugs_score"] = df["qtd_medic_vaz"].apply(
#         lambda x: 0 if x <= 3 else (0.5 if 4 <= x <= 6 else 1)
#     )
#     df_scores["score_drugs"] = df_scores["drugs_score"]

#     # ---- TEMPO DE INSTITUIÇÃO ----
#     df_scores["nursing_score"] = df["institut_time_years"].apply(
#         lambda x: 0 if x < 12 else (0.5 if 12 <= x < 24 else 1)
#     )
#     df_scores["score_nursing_home"] = df_scores["nursing_score"]

#     return df_scores


# def aplicar_brief_mpi(df):
#     df_scores = calcular_scores(df)

#     # estrutura organizada por domínios
#     dominios = [
#         "score_social",
#         "score_abvd",
#         "score_mobility",
#         "score_inpatient",
#         "score_falls",
#         "score_nutrition",
#         "score_comorbidity",
#         "score_drugs",
#         "score_nursing_home",
#     ]

#     df_scores["brief_mpi_total"] = df_scores[dominios].sum(axis=1)

#     # retornar só colunas finais (mas mantemos ids)
#     cols_saida = ["id_institution", "uuidv5"] + dominios + ["brief_mpi_total"]
#     return df_scores[cols_saida]

# teste = aplicar_brief_mpi(df)
# # %%

# teste["score_nursing_home"].max()
# %%





import numpy as np

def _safe_col(df, name):
    """Retorna coluna se existir, senão série de NaN com mesmo index."""
    return df[name] if name in df.columns else pd.Series([np.nan]*len(df), index=df.index)

def calcular_scores(df, keep_raw=False):
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
    # Social: sex, race, education
    sex_score = sex.map({1: 0, 2: 1}).fillna(0).astype(int)
    race_score = race.apply(lambda x: 0 if x in [1, 4] else 1).astype(int)
    education_score = education.apply(lambda x: 1 if x in [1, 2] else 0).astype(int)
    social_raw = sex_score + race_score + education_score   # 0..3

    # ABVD: basic + physical (physical = 1 if phys1 or phys2 present; phys3 ignored)
    basic_score = basic_act.map({1: 0, 2: 1}).fillna(0).astype(int)
    physical_score = ((phys1 == 1) | (phys2 == 1)).astype(int)   # 0/1
    abvd_raw = basic_score + physical_score   # 0..2

    # Mobility: elder_mobility (1->1, 2->0) + elder_difficulties (1->0, 2->1)
    mobility_comp = elder_mobility.map({1: 1, 2: 0}).fillna(0).astype(int)
    difficulties_comp = elder_difficulties.map({1: 0, 2: 1}).fillna(0).astype(int)
    mobility_raw = mobility_comp + difficulties_comp   # 0..2

    # Falls: interpretacao comum: code 1=no, 2=one, >=3=multiple
    falls_raw = np.where(falls_number == 1, 0,
                         np.where(falls_number == 2, 1,
                                  np.where(falls_number >= 3, 2, 0))).astype(int)

    # Inpatient: usar número/flag de internações (se 0->0, 1->0.5, >=2->1 depois)
    inpatient_raw = elder_hospitalized.astype(int)  # 0,1,2,...

    # Nutrition: combine strength, weight_loss, amount_weight_loss
    strength_score = elder_strenght.map({1: 1, 2: 0}).fillna(0).astype(int)
    weightloss_score = weight_loss.map({1: 1, 2: 0}).fillna(0).astype(int)
    # amount_weight_loss: code 1 -> 1, 2 -> 2
    amount_score = amount_weight_loss.apply(lambda x: 1 if x == 1 else (2 if x == 2 else 0)).astype(int)
    # raw nutrition => cap at 2 (we map 0->0, 1->0.5, >=2->1)
    nutrition_raw = (strength_score + weightloss_score + amount_score)
    nutrition_raw = np.minimum(nutrition_raw, 2).astype(int)

    # Comorbidity and drugs and nursing time (we will map to 0/0.5/1 using your rules)
    comorb_raw = comorbidities.astype(int)   # 0,1,2,3...
    drugs_raw = drugs.astype(int)            # number of active principles
    nursing_raw = nursing_time.astype(float) # years (or numeric) as you provided

    # keep raw columns if user wants them later
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
    score_inpatient = np.where(inpatient_raw >= 2, 1.0,
                               np.where(inpatient_raw == 1, 0.5, 0.0))

    # nutrition: 0->0, 1->0.5, >=2->1 (we capped nutritional_raw at 2)
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

def aplicar_brief_mpi(df, keep_raw=False):
    """Wrapper — retorna o DataFrame final com domínios normalizados e MPI."""
    return calcular_scores(df, keep_raw=keep_raw)


df_score = aplicar_brief_mpi(df)
# %%
df_score
# %%

####### PAREI AQUI
df_score.head(10)[["id_institution", "uuidv5", "full_name", "MPI", "risk"]]
df_score.sort_values(by="MPI", ascending=False)

# %%

# Salvando a tabela Score para o lake

df_score.to_csv("../../../../data/SMSAp/lake/mpiScore.csv", index=False)
print("✅Tabela MPI Score foi salva no lake!")
# %%
