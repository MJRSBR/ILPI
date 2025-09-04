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
    importar_todos_csvs('Lake')
