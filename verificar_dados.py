"""
Script para verificar os dados na tabela do BigQuery.
"""

from google.cloud import bigquery

# Configurações
PROJECT_ID = "projetos-icl"
DATASET_ID = "active_leads"
TABLE_ID = "emails_inscritos"
FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# Cliente
client = bigquery.Client(project=PROJECT_ID)

# Query para ver os últimos registros
query = f"""
SELECT *
FROM `{FULL_TABLE_ID}`
ORDER BY data_hora DESC
LIMIT 10
"""

print("Consultando dados na tabela...")
print("=" * 80)

try:
    results = client.query(query).result()

    print(f"\nUltimos 10 registros em {FULL_TABLE_ID}:")
    print("-" * 80)

    count = 0
    for row in results:
        print(f"{row.data_hora} | {row.tag:20} | {row.email}")
        count += 1

    if count == 0:
        print("Nenhum registro encontrado.")
    else:
        print("-" * 80)
        print(f"Total exibido: {count} registro(s)")

    # Query para contar por tag
    print("\n" + "=" * 80)
    print("Contagem por tag:")
    print("-" * 80)

    query_count = f"""
    SELECT tag, COUNT(*) as total
    FROM `{FULL_TABLE_ID}`
    GROUP BY tag
    ORDER BY total DESC
    """

    results_count = client.query(query_count).result()

    for row in results_count:
        print(f"{row.tag:20} | {row.total:5} registro(s)")

    print("=" * 80)

except Exception as e:
    print(f"Erro: {e}")
