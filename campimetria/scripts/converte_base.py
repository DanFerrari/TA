
import base64
import os
import pyodbc
print(pyodbc.drivers())


# Configuração do banco de dados
DB_PATH = r"C:\REPOSITORIOS\GIT\SOLARIS\FORMUSERINTERFACE\BIN\DEBUG\DBSOLARIS.MDF"
SERVER = r"(LocalDB)\MSSQLLocalDB"
DATABASE = "DBSOLARIS"  # Nome do banco dentro do MDF
TABLE_NAME = "dbo.NORMALREF"  # Nome completo da tabela
COLUMN_NAME = "ARQUIVO_2"  # Nome da coluna com os dados binários
OUTPUT_DIR = "arquivos_convertidos"

# Criar a pasta de saída se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# String de conexão
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER=(LocalDB)\\mssqllocaldb;"
    f"Integrated Security=True;"
    f"AttachDbFileName={DB_PATH};"
)


# Conectar ao banco de dados
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Selecionar os dados binários da tabela
    query = f"SELECT id, {COLUMN_NAME} FROM {TABLE_NAME}"
    cursor.execute(query)
    
    for row in cursor.fetchall():
        record_id, binary_data = row
        
        # Converter binário para string ASCII
        decoded_data = binary_data.decode("ascii")  # Removido base64 (não parece necessário aqui)
        
        # Gerar nome de arquivo Python
        file_name = os.path.join(OUTPUT_DIR, f"arquivo_{record_id}.py")
        
        # Criar um arquivo Python com os valores
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(f"lista_valores = {decoded_data.split('|')}\n")
        
        print(f"Arquivo criado: {file_name}")

    conn.close()
    print("Processo concluído com sucesso!")

except Exception as e:
    print(f"Erro: {e}")
