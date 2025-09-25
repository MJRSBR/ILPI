import pandas as pd
import sqlite3


csv_file_path = "seu_arquivo.csv"  # Caminho para o seu arquivo CSV
db_file_path = "seu_banco_de_dados.db"  # Nome do arquivo do banco de dados SQLite
table_name = "sua_tabela"  # Nome da tabela no banco de dados


connection = sqlite3.connect(db_file_path)


# Para arquivos grandes, você pode usar chunksize para processar em partes
chunk_size = 100000 # Defina um tamanho de chunk apropriado
for chunk in pd.read_csv(csv_file_path, chunksize=chunk_size):
    chunk.to_sql(table_name, connection, if_exists="append", index=False)


connection.close()
print(f"Dados do '{csv_file_path}' foram importados para a tabela '{table_name}' no banco '{db_file_path}'")
