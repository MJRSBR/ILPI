# # %%
# import sqlite3
# import pandas as pd

# # Criação do banco de dados SQLite
# conn = sqlite3.connect('ilpi.db')
# cursor = conn.cursor()
# # %%
# # Criação das tabelas no banco de dados

# # Tabela ILPI
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS ILPI (
#     id_instituicao INTEGER UNIQUE PRIMARY KEY,              -- Código da Instituíção
#     institution_name VARCHAR(150),                          -- Nome da instituíção
#     latitude FLOAT,                                         -- Coordenada espacial
#     longitude FLOAT                                         -- Coordenada espacial
# )
# ''')
               

# # Tabela Residente
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Residente (
#     id_UUID VARCHAR PRIMARY KEY,                           -- UUID gerado a partir do CPF
#     id_instituicao INTEGER FOREIGN KEY,                    -- Código da instituíção              
#     full_name TEXT,                                        -- Nome completo do paciente
#     cpf INTEGER UNIQUE,                                    -- CPF (deve ser único)
#     date_of_birth DATE,                                    -- Data de nascimento 
#     elder_age INTEGER,                                     -- Idade do residente
#     sex TEXT),                                             -- Genero do paciente
#     FOREIGN KEY (id_instituicao) REFERENCES ILPI(institution_name)
# )
# ''')

# # Tabela de TempoInstituíção
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS TempoInstituicao (
#     id_residente VARCHAR FOREIGN KEY,                  -- UUID gerado a partir do CPF
#     id_instituicao INTEGER PRIMARY KEY,                -- Código da Instituíção
#     institut_time_years FLOAT                          -- Idade do residente em anos 
# )
# ''')

# # Tabela de SuporteFamiliar
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS SuporteFamiliar (
#     id_residente VARCHAR FOREIGN KEY,               -- UUID gerado a partir do CPF
#     id_instituicao INTEGER PRIMARY KEY,             -- Código da Instituíção
#     family_support TEXT,                            -- Suporte da família
# )
# ''')

# # Tabela de GrauDependencia
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS GrauDependencia (
#     id_residente VARCHAR FOREIGN KEY,                               -- UUID gerado a partir do CPF
#     id_instituicao INTEGER PRIMARY KEY,                             -- Código da Instituíção
#     dependence_degree INTEGER,                                      -- Grau de dependência
#     FOREIGN KEY(id_residente) REFERENCES Residente(id_uuid),
#     FOREIGN KEY(id_instituicao) REFERENCES ILPI(institution_name)
# )
# ''')

# # Tabela de QtdeMedicTot
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS QtdeMedicTot (
#     id_residente VARCHAR FOREIGN KEY,                               -- UUID gerado a partir do CPF
#     id_instituicao TEXT,                                            -- Código da Instituíção
#     tot_medicin INTEGER,                                            -- Número de medicamentos tomados pelo residente
#     FOREIGN KEY(id_residente) REFERENCES Residente(id_uuid),
#     FOREIGN KEY(id_instituicao) REFERENCES ILPI(institution_name)
# )
# ''')

# # Tabela de Morbidades
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Morbidades (
#     id_residente VARCHAR FOREIGN KEY,                                 -- UUID gerado a partir do CPF
#     idid_instituicao INTEGER PRIMARY KEY,                             -- Código da Instituíção
#     Mobidades TEXT,                                                   -- Morbidades do residente [será uma lista]
#     other_morbidities TEXT,                                           -- Outras morbidades existentes [será uma lista] 
#     soma_morbidities INTEGER,                                         -- Morbidades somadas     
#     FOREIGN KEY(id_residente) REFERENCES Residente(id_uuid),
#     FOREIGN KEY(id_instituicao) REFERENCES ILPI(institution_name)                         
# )
# ''')

# # Tabela EstadoSaude
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS EstadoSaude (
#     id_residente VARCHAR FOREIGN KEY,                                 -- UUID gerado a partir do CPF
#     idid_instituicao INTEGER PRIMARY KEY,                             -- Código da Instituíção
#     health_condition TEXT,
#     FOREIGN KEY(id_residente) REFERENCES Residente(id_uuid),
#     FOREIGN KEY(id_instituicao) REFERENCES ILPI(institution_name)                                              -- Estado de saúde do residente
# )
# ''')

# # Tabela Emergencia
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Emergencia (
#     id_residente INTEGER PRIMARY KEY,               -- ID residente (único)
#     id_instituicao TEXT,                            -- Código da Instituíção
#     FOREIGN KEY(id_residente) REFERENCES Residente(id_uuid),
#     FOREIGN KEY(id_instituicao) REFERENCES ILPI(institution_name) 
# )
# ''')

# # Tabela Hospitalizacao
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Hospitalizacao (
#     id_residente INTEGER PRIMARY KEY,               -- ID residente (único)
#     id_instituicao TEXT,                            -- Código da Instituíção
#     FOREIGN KEY(id_residente) REFERENCES Residente(id_uuid),
#     FOREIGN KEY(id_instituicao) REFERENCES ILPI(institution_name) 
# )
# ''')

# # Confirma e encerra a conexão
# conn.commit()
# conn.close()

# print("Tabelas criadas com sucesso!!")

# %%
import sqlite3
import pandas as pd
from ingestion import importar_todos_csvs
# Criação do banco de dados SQLite
conn = sqlite3.connect('ilpi.db')
cursor = conn.cursor()

# %%
# Criação das tabelas

# Tabela ILPI
cursor.execute('''
CREATE TABLE IF NOT EXISTS ILPI (
    id_instituicao INTEGER PRIMARY KEY,              -- Código da Instituição
    institution_name VARCHAR(150),                   -- Nome da instituição
    latitude FLOAT,                                   -- Coordenada espacial
    longitude FLOAT                                   -- Coordenada espacial
)
''')

# Tabela Residente
cursor.execute('''
CREATE TABLE IF NOT EXISTS Residente (
    id_UUID VARCHAR PRIMARY KEY,                      -- UUID gerado a partir do CPF
    id_instituicao INTEGER,                           -- Código da instituição
    full_name TEXT,                                   -- Nome completo do paciente
    cpf INTEGER UNIQUE,                               -- CPF (deve ser único)
    date_of_birth DATE,                               -- Data de nascimento 
    elder_age INTEGER,                                -- Idade do residente
    sex TEXT,                                         -- Gênero do paciente
    FOREIGN KEY (id_instituicao) REFERENCES ILPI(id_instituicao)
)
''')

# Tabela TempoInstituicao
cursor.execute('''
CREATE TABLE IF NOT EXISTS TempoInstituicao (
    id_residente VARCHAR,                             -- UUID do residente
    id_instituicao INTEGER,                           -- Código da instituição
    institut_time_years FLOAT,                        -- Tempo na instituição (anos)
    PRIMARY KEY (id_residente, id_instituicao),
    FOREIGN KEY (id_residente) REFERENCES Residente(id_UUID),
    FOREIGN KEY (id_instituicao) REFERENCES ILPI(id_instituicao)
)
''')

# Tabela SuporteFamiliar
cursor.execute('''
CREATE TABLE IF NOT EXISTS SuporteFamiliar (
    id_residente VARCHAR,                             -- UUID do residente
    id_instituicao INTEGER,                           -- Código da instituição
    family_support TEXT,                              -- Suporte da família
    PRIMARY KEY (id_residente, id_instituicao),
    FOREIGN KEY (id_residente) REFERENCES Residente(id_UUID),
    FOREIGN KEY (id_instituicao) REFERENCES ILPI(id_instituicao)
)
''')

# Tabela GrauDependencia
cursor.execute('''
CREATE TABLE IF NOT EXISTS GrauDependencia (
    id_residente VARCHAR,
    id_instituicao INTEGER,
    dependence_degree INTEGER,
    PRIMARY KEY (id_residente, id_instituicao),
    FOREIGN KEY(id_residente) REFERENCES Residente(id_UUID),
    FOREIGN KEY(id_instituicao) REFERENCES ILPI(id_instituicao)
)
''')

# Tabela QtdeMedicTot
cursor.execute('''
CREATE TABLE IF NOT EXISTS QtdeMedicTot (
    id_residente VARCHAR,
    id_instituicao INTEGER,
    tot_medicin INTEGER,
    PRIMARY KEY (id_residente, id_instituicao),
    FOREIGN KEY(id_residente) REFERENCES Residente(id_UUID),
    FOREIGN KEY(id_instituicao) REFERENCES ILPI(id_instituicao)
)
''')

# Tabela Morbidades
cursor.execute('''
CREATE TABLE IF NOT EXISTS Morbidades (
    id_residente VARCHAR,
    id_instituicao INTEGER,
    morbidades TEXT,
    other_morbidities TEXT,
    soma_morbidities INTEGER,
    PRIMARY KEY (id_residente, id_instituicao),
    FOREIGN KEY(id_residente) REFERENCES Residente(id_UUID),
    FOREIGN KEY(id_instituicao) REFERENCES ILPI(id_instituicao)
)
''')

# Tabela EstadoSaude
cursor.execute('''
CREATE TABLE IF NOT EXISTS EstadoSaude (
    id_residente VARCHAR,
    id_instituicao INTEGER,
    health_condition TEXT,
    PRIMARY KEY (id_residente, id_instituicao),
    FOREIGN KEY(id_residente) REFERENCES Residente(id_UUID),
    FOREIGN KEY(id_instituicao) REFERENCES ILPI(id_instituicao)
)
''')

# Tabela Emergencia
cursor.execute('''
CREATE TABLE IF NOT EXISTS Emergencia (
    id_residente VARCHAR,
    id_instituicao INTEGER,
    PRIMARY KEY (id_residente, id_instituicao),
    FOREIGN KEY(id_residente) REFERENCES Residente(id_UUID),
    FOREIGN KEY(id_instituicao) REFERENCES ILPI(id_instituicao)
)
''')

# Tabela Hospitalizacao
cursor.execute('''
CREATE TABLE IF NOT EXISTS Hospitalizacao (
    id_residente VARCHAR,
    id_instituicao INTEGER,
    PRIMARY KEY (id_residente, id_instituicao),
    FOREIGN KEY(id_residente) REFERENCES Residente(id_UUID),
    FOREIGN KEY(id_instituicao) REFERENCES ILPI(id_instituicao)
)
''')

# Confirma e encerra a conexão
conn.commit()
conn.close()

print("Tabelas criadas com sucesso!!")





# %%
# Carregar os dados dos CSVs para DataFrames
residentes_df = pd.read_csv('../Residente.csv').  #### parei aqui
qtd_medic_total_df = pd.read_csv('QtdeMedicTot.csv')
suporte_familiar_df = pd.read_csv('SuporteFamiliar.csv')
estado_saude_df = pd.read_csv('estado_saude_residente.csv')
grau_dependencia_df = pd.read_csv('grau_dependencia_residente.csv')
morbidades_df = pd.read_csv('Morbidades.csv')
tempo_instit_residente_df = pd.read_csv('tempo_instit_residente.csv')

# %%


# Inserir dados nas tabelas

# Inserir dados na tabela de Residente
for _, row in residentes_df.iterrows():
    cursor.execute('''
    INSERT INTO Residente (id_UUID, id_instituicao, full_name, cpf, date_of_birth, elder_age, sex,)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (row['id_UUID'], row['id_instituicao'], row['full_name'], row['cpf'],
          row['date_of_birth'], row['elder_age'], row['sex']))

# Inserir dados na tabela de Tempo de Instituiçao
for _, row in tempo_instit_residente_df.iterrows():
    cursor.execute('''
    INSERT INTO TempoInstituicao (id_residente, id_instituicao, institut_time_years)
    VALUES (?, ?, ?)
    ''', (row['id_residente'], row['id_instituicao'], row['institut_time_years']))

# Inserir dados na tabela de Suporte Familiar
for _, row in suporte_familiar_df.iterrows():
    cursor.execute('''
    INSERT INTO SuporteFamiliar (id_residente, id_instituicao, family_support)
    VALUES (?, ?, ?, ?)
    ''', (row['id_residente'], row['id_instituicao'], row['family_support']))

# Inserir dados na tabela de Grau de Dependencia
for _, row in grau_dependencia_df.iterrows():
    cursor.execute('''
    INSERT INTO GrauDependencia (id_residente, id_instituicao, dependence_degree)
    VALUES (?, ?, ?, ?)
    ''', (row['id_residente'], row['id_instituicao'], row['dependence_degree']))

# Inserir dados na tabela de Qtde Medicamentos
for _, row in qtd_medic_total_df.iterrows():
    cursor.execute('''
    INSERT INTO QtdeMedicTot (id_residente, id_instituicao, tot_medicin)
    VALUES (?, ?, ?)
    ''', (row['id_residente'], row['id_instituicao'], row['tot_medicin']))    

# Inserir dados na tabela de Morbidades
for _, row in morbidades_df.iterrows():
    cursor.execute('''
    INSERT INTO Morbidades (id_residente, id_instituicao, Morbidades, other_morbidities, soma_morbidities)
    VALUES (?, ?, ?, ?, ?)
    ''', (row['id_residente'], row['id_instituicao'], row['Morbidades'], 
          row['other_morbidities'], row['soma_morbidities']))   


# Inserir dados na tabela de Estado de Saúde
for _, row in estado_saude_df.iterrows():
    cursor.execute('''
    INSERT INTO EstadoSaude (id_residente, id_instituicao, health_condition)
    VALUES (?, ?, ?)
    ''', (row['id_residente'], row['id_instituicao'], row['health_condition']))  


# # Inserir dados na tabela de Emergencia
# for _, row in emergencia_df.iterrows():
#     cursor.execute('''
#     INSERT INTO Emergencia (id_residente, id_instituicao)
#     VALUES (?, ?)
#     ''', (row['id_residente'], row['id_instituicao']))    


# # Inserir dados na tabela de hospitalizacao
# for _, row in hospitalizacao_df.iterrows():
#     cursor.execute('''
#     INSERT INTO hospitalizacao (id_residente, id_instituicao)
#     VALUES (?, ?)
#     ''', (row['id_residente'], row['id_instituicao']))  

# Salvar (commit) e fechar a conexão com o banco de dados
conn.commit()

# Fechar a conexão
conn.close()

print("Banco de dados ilpi.db criado e tabelas preenchidas com sucesso!")

# %%

# import os

# DB_NAME = 'ilpi.db'

# def connect_db():
#     return sqlite3.connect(DB_NAME)

# # ---------------- IMPORTAR CSV PARA TABELA ----------------
# def importar_csv_para_tabela(nome_tabela, caminho_csv):
#     conn = connect_db()
#     cursor = conn.cursor()

#     with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
#         leitor = csv.DictReader(csvfile)
#         colunas = leitor.fieldnames
#         placeholders = ', '.join(['?'] * len(colunas))
#         colunas_sql = ', '.join(colunas)

#         for linha in leitor:
#             valores = [linha[col] for col in colunas]
#             try:
#                 cursor.execute(f'''
#                     INSERT INTO {nome_tabela} ({colunas_sql})
#                     VALUES ({placeholders})
#                 ''', valores)
#             except sqlite3.IntegrityError as e:
#                 print(f"Erro ao inserir na tabela {nome_tabela}: {e}")

#     conn.commit()
#     conn.close()
#     print(f"Dados importados para a tabela {nome_tabela} com sucesso.")

# # ---------------- IMPORTAÇÃO PARA TODAS AS TABELAS ----------------

# def importar_todos_csvs(pasta_csv):
#     tabelas = [
#         "ILPI",
#         "Residente",
#         "TempoInstituicao",
#         "SuporteFamiliar",
#         "GrauDependencia",
#         "QtdMedicTot",
#         "Morbidades",
#         "EstadoSaude",
#         "Emergencia",
#         "Hospitalizacao"
#     ]

#     for tabela in tabelas:
#         caminho = os.path.join(pasta_csv, f"{tabela}.csv")
#         if os.path.exists(caminho):
#             importar_csv_para_tabela(tabela, caminho)
#         else:
#             print(f"Arquivo {tabela}.csv não encontrado na pasta {pasta_csv}. Ignorado.")

# %%
import sqlite3
import csv
import os
from datetime import datetime

DB_NAME = 'ilpi.db'
LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'import_log.txt')

# ---------------- FUNÇÃO DE CONEXÃO ----------------
def connect_db():
    return sqlite3.connect(DB_NAME)

# ---------------- INICIAR LOG ----------------
def iniciar_log():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write(f"===== LOG DE IMPORTAÇÃO - {datetime.now()} =====\n\n")

# ---------------- ESCREVER NO LOG ----------------
def log(mensagem):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(mensagem + '\n')
    print(mensagem)

# ---------------- IMPORTAÇÃO DE UM CSV ----------------
def importar_csv_para_tabela(nome_tabela, caminho_csv):
    conn = connect_db()
    cursor = conn.cursor()

    total = 0
    erros = 0

    try:
        with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
            leitor = csv.DictReader(csvfile)
            colunas = leitor.fieldnames
            placeholders = ', '.join(['?'] * len(colunas))
            colunas_sql = ', '.join(colunas)

            for linha in leitor:
                total += 1
                valores = [linha[col] for col in colunas]

                try:
                    cursor.execute(f'''
                        INSERT INTO {nome_tabela} ({colunas_sql})
                        VALUES ({placeholders})
                    ''', valores)

                except sqlite3.IntegrityError as e:
                    log(f"[{nome_tabela}] Linha {total}: ERRO de integridade - {e}")
                    erros += 1

                except sqlite3.OperationalError as e:
                    log(f"[{nome_tabela}] Linha {total}: ERRO operacional - {e}")
                    erros += 1

        conn.commit()
        log(f"[{nome_tabela}] {total - erros}/{total} registros inseridos com sucesso. {erros} erros.")
    
    except FileNotFoundError:
        log(f"[{nome_tabela}] ERRO: Arquivo CSV não encontrado: {caminho_csv}")

    except Exception as e:
        log(f"[{nome_tabela}] ERRO inesperado: {str(e)}")

    finally:
        conn.close()

# ---------------- IMPORTAÇÃO EM LOTE ----------------
def importar_todos_csvs(pasta_csv):
    iniciar_log()

    tabelas = [
        "ILPI",
        "Residente",
        "TempoInstituicao",
        "SuporteFamiliar",
        "GrauDependencia",
        "QtdeMedicTot",
        "Morbidades",
        "EstadoSaude",
        "Emergencia",
        "Hospitalizacao"
    ]

    for tabela in tabelas:
        # caminho = os.path.join(pasta_csv, f"{tabela}.csv")
        # importar_csv_para_tabela(tabela, caminho)
        caminho = os.path.join(pasta_csv, f"{tabela}.csv")
        if os.path.exists(caminho):
            importar_csv_para_tabela(tabela, caminho)
        else:
            print(f"Arquivo {tabela}.csv não encontrado na pasta {pasta_csv}. Ignorado.")

    log("\n===== IMPORTAÇÃO CONCLUÍDA =====")

# ---------------- EXECUÇÃO DIRETA ----------------
if __name__ == "__main__":
    importar_todos_csvs('../../../../data/SMSAp/lake/')
# %%
