
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
df = pd.read_csv("../../../../data/SMSAp/ILPI/base_perfil_epidemiologico.csv",
                 sep=";")
df.head()
# %%
## --------------------
##  - COMPONENTES DE FRAGILIDADE
## --------------------

# fragilidade_dic = {
#     'amount_weight_loss':'Perda de Peso',
#     'elder_strenght':(lambda x: x == 2),
#     'elder_hospitalized':(lambda x: x ==1),
#     'elder_difficulties':(lambda x: x == 1),
#     'elder_mobility':(lambda x: x == 2),
#     'basic_activities_diffic':(lambda x: x ==1),
#     'falls_number':(lambda x: x ==1)
# }

# #amount_weight_loss_dict ={1: "de 1 a 3 kg",2: "mais de 3 kg",}
# #elder_strenght_dict = {1:"Sim",2:"Não"}	
# #elder_hospitalized_dict = {1: "nenhuma", 2: "1 a 2 vezes", 3: "3 vezes", 4: "4 ou mais",}
# #elder_difficulties_dict = {1:"nenhuma", 2: "alguma",3: "não consegue",}
# #elder_mobility_dict = {1: "Sim",2: "Não"}	
# #basic_activities_diffic_dict = 	{1:	"Sim",2: "Não"}	
# #falls_number_dict = {1: " nenhuma", 2: "1 a 3 quedas", 3: "4 e mais",}

# # %%

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
    campos_para_propagacao = ['institution_name', 'full_name', 'cpf']
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
# Fazendo o merge tabelas
# *****************.   PRECISA VERIFICAR AS TABELAS MERGE *************************
# Agrupar tabelas de interesse 

#df_score = df_morbidades(contagem_medic_por_residente, how='rigth')
# %%
df_score = df_morbidades.merge(comp_fragilidade, how='right')
df_score

# %%
#amount_weight_loss_dict ={1: "de 1 a 3 kg",2: "mais de 3 kg",}
#elder_strenght_dict = {1:"Sim",2:"Não"}	
#elder_hospitalized_dict = {1: "nenhuma", 2: "1 a 2 vezes", 3: "3 vezes", 4: "4 ou mais",}
#elder_difficulties_dict = {1:"nenhuma", 2: "alguma",3: "não consegue",}
#elder_mobility_dict = {1: "Sim",2: "Não"}	
#basic_activities_diffic_dict = 	{1:	"Sim",2: "Não"}	
#falls_number_dict = {1: " nenhuma", 2: "1 a 3 quedas", 3: "4 e mais",}

##*********************. EXEMPLO NECESSITA DEFINIR OS PARAMETROS  ************************
condicao_atencao = {
    'amount_weight_loss':(lambda x: x == 1),
    'elder_strenght':(lambda x: x == 2),
    'elder_hospitalized':(lambda x: x ==1),
    'elder_difficulties':(lambda x: x == 1),
    'elder_mobility':(lambda x: x == 2),
    'basic_activities_diffic':(lambda x: x ==1),
    'falls_number':(lambda x: x ==1)
}

condicao_alerta = {
    'amount_weight_loss':(lambda x: x == 1),
    'elder_strenght':(lambda x: x == 1),
    'elder_hospitalized':(lambda x: x in [2, 3] ),
    'elder_difficulties':(lambda x: x == 2),
    'elder_mobility':(lambda x: x == 1),
    'basic_activities_diffic':(lambda x: x == 1),
    'falls_number':(lambda x: x == 2)
}

condicao_critica = {
    'amount_weight_loss':(lambda x: x == 2),
    'elder_strenght':(lambda x: x == 1),
    'elder_hospitalized':(lambda x: x in [3, 4]),
    'elder_difficulties':(lambda x: x == 1),
    'elder_mobility':(lambda x: x == 1),
    'basic_activities_diffic':(lambda x: x ==1),
    'falls_number':(lambda x: x == 3)
}

# %%


# # %%

# #condicao_atencao = {
# #    'elder_age': (lambda x: x < 70),
# #    'soma_morbidities': (lambda x: x <= 3),
# #    'soma_fragilidades': (lambda x: x in [2, 3]),
# #
# #}
# #
# #condicao_alerta = {
# #    'elder_age': (lambda x: x > 70 & x < 80),
# #    'soma_morbidities': (lambda x: x in [4, 5] ),
# #    'soma_fragilidades': (lambda x: x in [3, 4]),
# #    
# #}
# #
# #condicao_critica = {
# #    'elder_age': (lambda x: x >= 81),
# #    'soma_morbidities': (lambda x: x >= 6),
# #    'soma_fragilidades': (lambda x: x>= 4),
# #    
# #}

# # %%
# resultado, resumo = classificar_risco(df, condicao_critica, condicao_alerta, condicao_atencao)

# # %%
# from IPython.display import display, HTML

# # Exibe o resultado com cores
# display(HTML(resultado.to_html(escape=False)))

# # Mostra o resumo correto
# display(HTML(resumo.to_html(escape=False)))

# # %%
# salvar_tabela_como_imagem(
#     resumo,
#     '../tables/13_tabela_resumo_score_fragilidade.png',
#     titulo='Score de Fragilidade do Residente por ILPI',
#     largura_max_coluna=25
# )
# # %%
# df.head()
# # %%

from typing import Iterable, Optional, Union, Dict, Any

def _sum01(values: Iterable[Optional[Union[int, bool]]], missing_as_zero: bool = True) -> int:
   """Soma itens codificados em 0/1 (ou False/True). Pode tratar None como 0 ou ignorar."""
   total = 0
   for v in values:
       if v is None:
           if missing_as_zero:
               v = 0
           else:
               continue
       total += int(bool(v))
   return total

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

def _map_domain(total: int, mapping: str) -> float:
   """
   Converte o total do domínio no valor 0 / 0.5 / 1 conforme a tabela Brief-MPI.
   mapping ∈ {'adl','iadl','mobility','cognitive','nutrition','comorbidity','drugs','cohab'}
   """
   
   if mapping in ('adl', 'iadl'):
       if total == 3: return 0.0
       if total in (1, 2): return 0.5
       return 1.0                           # total == 0
   elif mapping == 'mobility':
       if total >= 2: return 0.0            # 3–2
       if total == 1: return 0.5
       return 1.0                           # 0
   elif mapping in ('cognitive', 'nutrition'):
       if total == 0: return 0.0
       if total == 1: return 0.5
       return 1.0                           # 2–3
   elif mapping == 'comorbidity':
       if total == 0: return 0.0
       if total in (1, 2): return 0.5
       return 1.0                           # ≥3
   elif mapping == 'drugs':
       if total <= 3: return 0.0
       if 4 <= total <= 6: return 0.5
       return 1.0                           # ≥7
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
   else:
       raise ValueError("mapping desconhecido")

def compute_brief_mpi(
   #adl_items: Iterable[Optional[Union[int, bool]]],
   iadl_items: Iterable[Optional[Union[int, bool]]],
   mobility_items: Iterable[Optional[Union[int, bool]]],
   cognitive_items: Iterable[Optional[Union[int, bool]]],
   nutritional_items: Iterable[Optional[Union[int, bool]]],
   comorbidities_count: int,
   drug_count: int,
   #cohabitation: Union[int, str],
   missing_as_zero: bool = True,
   round_ndigits: int = 2
) -> Dict[str, Any]:
   """
   Calcula o Brief-MPI.

   Convenções dos itens:
     - ADL/IADL/Mobility: 1(True)=capaz/independente; 0(False)=não.
     - Cognitive/Nutrition: 1(True)=problema/erro/risco presente; 0(False)=ausente.
     - comorbidities_count: nº de doenças crônicas em tratamento.
     - drug_count: nº de princípios ativos em uso.
     - cohabitation: 0=Alone, 1=With Family, 2=Institution, ou string equivalente.
     - missing_as_zero: se False, None é ignorado na soma (preferível preencher todos os 3 itens).

   Retorna: dicionário com totais dos domínios, valores (0/0.5/1), MPI e classificação.
   """
   adl_total = _sum01(adl_items, missing_as_zero)
   iadl_total = _sum01(iadl_items, missing_as_zero)
   mobility_total = _sum01(mobility_items, missing_as_zero)
   cognitive_total = _sum01(cognitive_items, missing_as_zero)
   nutri_total = _sum01(nutritional_items, missing_as_zero)

   vals = {
       'ADL_value': _map_domain(adl_total, 'adl'),
       'IADL_value': _map_domain(iadl_total, 'iadl'),
       'Mobility_value': _map_domain(mobility_total, 'mobility'),
       'Cognitive_value': _map_domain(cognitive_total, 'cognitive'),
       'Nutritional_value': _map_domain(nutri_total, 'nutrition'),
       'Comorbidity_value': _map_domain(int(comorbidities_count), 'comorbidity'),
       'Drug_value': _map_domain(int(drug_count), 'drugs'),
       'Cohabitation_value': _map_domain(cohabitation, 'cohab'),
   }

   mpi_raw = sum(vals.values()) / 8.0
   mpi = round(mpi_raw, round_ndigits)

   if mpi <= 0.33:
       risk = 'Mild (MPI 1)'
   elif mpi <= 0.66:
       risk = 'Moderate (MPI 2)'
       # nota: 0.66 entra em Moderado como na sua legenda
   else:
       risk = 'High (MPI 3)'

   return {
       'totals': {
           'ADL': adl_total,
           'IADL': iadl_total,
           'Mobility': mobility_total,
           'Cognitive': cognitive_total,
           'Nutritional': nutri_total,
           'Comorbidities': int(comorbidities_count),
           'Drugs': int(drug_count),
           'Cohabitation': cohabitation,
       },
       'values': vals,
       'MPI': mpi,
       'MPI_raw': mpi_raw,
       'risk': risk,
   }




# %%

import pandas as pd

# # Exemplo de dicionário de mapeamento das colunas do REDCap → parâmetros da função
# COLUMN_MAP = {
#     "adl_items": ["adl_1", "adl_2", "adl_3"],
#     "iadl_items": ["iadl_1", "iadl_2", "iadl_3"],
#     "mobility_items": ["mob_1", "mob_2", "mob_3"],
#     "cognitive_items": ["cog_1", "cog_2", "cog_3"],
#     "nutritional_items": ["nutri_1", "nutri_2", "nutri_3"],
#     "comorbidities_count": "comorb_count",
#     "drug_count": "drug_count",
#     "cohabitation": "cohab",
# }

# Exemplo de dicionário de mapeamento das colunas do REDCap → parâmetros da função



COLUMN_MAP = {
    "adl_items": ["adl_1", "adl_2", "adl_3"],
    "iadl_items": ["iadl_1", "iadl_2", "iadl_3"],
    "mobility_items": ["elder_difficulties", "mob_2", "mob_3"],
    "cognitive_items": ["cog_1", "cog_2", "cog_3"],
    "nutritional_items": ["nutri_1", "nutri_2", "nutri_3"],
    "comorbidities_count": "comorb_count",
    "drug_count": "drug_count",
    "cohabitation": "cohab",
}

def aplicar_brief_mpi(df: pd.DataFrame, col_map: dict = COLUMN_MAP) -> pd.DataFrame:
    """
    Aplica o cálculo do Brief-MPI linha a linha no DataFrame do REDCap.
    Retorna um novo DataFrame com as colunas originais + resultados MPI.
    """
    resultados = []

    for _, row in df.iterrows():
        kwargs = {
            "adl_items": [row[c] for c in col_map["adl_items"]],
            "iadl_items": [row[c] for c in col_map["iadl_items"]],
            "mobility_items": [row[c] for c in col_map["mobility_items"]],
            "cognitive_items": [row[c] for c in col_map["cognitive_items"]],
            "nutritional_items": [row[c] for c in col_map["nutritional_items"]],
            "comorbidities_count": row[col_map["comorbidities_count"]],
            "drug_count": row[col_map["drug_count"]],
            "cohabitation": row[col_map["cohabitation"]],
        }

        result = compute_brief_mpi(**kwargs)
        resultados.append(result)

    # transformar lista de dicts em DataFrame
    df_resultados = pd.json_normalize(resultados)

    # concatenar resultados ao DataFrame original
    df_final = pd.concat([df.reset_index(drop=True), df_resultados], axis=1)
    return df_final
# %%

df.columns.tolist()
# %%
df['elder_mobility']

# %%
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

df_mobil = combinar_colunas_dict(df, combinacoes)
df_mobil 
# %%
df_mobil["mobilidade"]
# %%
