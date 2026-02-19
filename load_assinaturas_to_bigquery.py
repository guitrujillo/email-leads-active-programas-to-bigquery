import os
import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import sys

# Configurações
excel_file = os.getenv("EXCEL_FILE_PATH")
if not excel_file:
    raise ValueError("EXCEL_FILE_PATH não definida. Defina a variável de ambiente com o caminho do arquivo Excel.")
project_id = os.getenv("BIGQUERY_PROJECT_ID")
if not project_id:
    raise ValueError("BIGQUERY_PROJECT_ID não definida no ambiente.")
dataset_id = os.getenv("BIGQUERY_DATASET_ID", "hotmart")
table_id = os.getenv("BIGQUERY_TABLE_ID", "assinaturas")
full_table_id = f"{project_id}.{dataset_id}.{table_id}"

def main():
    try:
        # Ler o arquivo Excel
        print(f"Lendo arquivo Excel: {excel_file}")
        df = pd.read_excel(excel_file)

        # Mostrar informações sobre o arquivo
        print(f"\nArquivo lido com sucesso!")
        print(f"Número de linhas: {len(df)}")
        print(f"Número de colunas: {len(df.columns)}")
        print(f"\nColunas encontradas:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col} (tipo: {df[col].dtype})")

        print(f"\nPrimeiras linhas do arquivo:")
        print(df.head())

        # Converter colunas 'object' que podem ter tipos mistos para string
        print(f"\nConvertendo colunas com tipos mistos para string...")
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str)

        # Inicializar cliente BigQuery
        print(f"\n\nConectando ao BigQuery...")
        client = bigquery.Client(project=project_id)

        # Verificar se o dataset existe
        try:
            client.get_dataset(f"{project_id}.{dataset_id}")
            print(f"Dataset '{dataset_id}' encontrado.")
        except NotFound:
            print(f"ERRO: Dataset '{dataset_id}' não encontrado!")
            sys.exit(1)

        # Criar schema baseado no DataFrame
        print(f"\nCriando schema da tabela...")

        # Mapear tipos pandas para tipos BigQuery
        type_mapping = {
            'int64': 'INTEGER',
            'float64': 'FLOAT',
            'object': 'STRING',
            'bool': 'BOOLEAN',
            'datetime64[ns]': 'TIMESTAMP',
            'date': 'DATE'
        }

        schema = []
        for column in df.columns:
            dtype = str(df[column].dtype)
            bq_type = type_mapping.get(dtype, 'STRING')
            schema.append(bigquery.SchemaField(column, bq_type, mode='NULLABLE'))

        print(f"\nSchema criado:")
        for field in schema:
            print(f"  - {field.name}: {field.field_type}")

        # Criar a tabela
        print(f"\nCriando tabela '{full_table_id}'...")
        table = bigquery.Table(full_table_id, schema=schema)

        try:
            table = client.create_table(table)
            print(f"Tabela '{full_table_id}' criada com sucesso!")
        except Exception as e:
            if "Already Exists" in str(e):
                print(f"Tabela '{full_table_id}' já existe.")
                # Pegar a tabela existente
                table = client.get_table(full_table_id)
            else:
                raise e

        # Carregar dados
        print(f"\nCarregando {len(df)} linhas para a tabela...")

        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        job = client.load_table_from_dataframe(df, full_table_id, job_config=job_config)
        job.result()  # Aguardar conclusão

        print(f"\nDados carregados com sucesso!")

        # Verificar resultado
        table = client.get_table(full_table_id)
        print(f"\nResumo:")
        print(f"  - Tabela: {full_table_id}")
        print(f"  - Total de linhas na tabela: {table.num_rows}")
        print(f"  - Tamanho: {table.num_bytes / (1024*1024):.2f} MB")

    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado: {excel_file}")
        sys.exit(1)
    except Exception as e:
        print(f"ERRO: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
