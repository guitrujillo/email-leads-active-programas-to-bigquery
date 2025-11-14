"""
Script para extrair e-mails de inscritos do ActiveCampaign e enviar para o BigQuery.

IMPORTANTE: Para alterar tags ou adicionar novas, edite o arquivo config_tags.py

Autor: Assistente de Engenharia de Dados
Data: 2025-11-12
"""

import os
import requests
import pandas as pd
from datetime import datetime
from google.cloud import bigquery
from typing import List, Dict
import time

# Importa configurações do arquivo externo
from config_tags import TAG_URLS, PROJECT_ID, DATASET_ID, TABLE_ID, FULL_TABLE_ID

# API Key do ActiveCampaign (configurada via variável de ambiente)
API_KEY = os.environ.get("ACTIVECAMPAIGN_API_KEY")


def get_activecampaign_headers() -> Dict[str, str]:
    """
    Retorna os headers necessários para autenticação na API do ActiveCampaign.
    """
    if not API_KEY:
        raise ValueError("ACTIVECAMPAIGN_API_KEY não está configurada nas variáveis de ambiente")

    return {
        "Api-Token": API_KEY,
        "Content-Type": "application/json"
    }


def fetch_contacts_from_tag(url: str, tag_name: str) -> List[str]:
    """
    Extrai todos os e-mails de contatos de uma tag específica do ActiveCampaign.
    Lida com paginação automaticamente.

    Args:
        url: URL da API para a tag
        tag_name: Nome da tag para logging

    Returns:
        Lista de e-mails únicos
    """
    headers = get_activecampaign_headers()
    all_emails = []
    offset = 0
    limit = 100  # Limite por página (ajuste conforme necessário)

    print(f"Extraindo contatos da tag '{tag_name}'...")

    while True:
        # Adiciona parâmetros de paginação
        paginated_url = f"{url}&limit={limit}&offset={offset}"

        try:
            response = requests.get(paginated_url, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            contacts = data.get("contacts", [])

            if not contacts:
                break

            # Extrai e-mails dos contatos
            for contact in contacts:
                email = contact.get("email")
                if email:
                    all_emails.append(email)

            print(f"  - Extraídos {len(contacts)} contatos (offset: {offset})")

            # Verifica se há mais páginas
            total = int(data.get("meta", {}).get("total", 0))
            if offset + limit >= total:
                break

            offset += limit
            time.sleep(0.5)  # Respeita rate limits da API

        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar contatos da tag '{tag_name}': {e}")
            break

    # Remove duplicatas
    unique_emails = list(set(all_emails))
    print(f"Total de e-mails únicos extraídos da tag '{tag_name}': {len(unique_emails)}")

    return unique_emails


def extract_all_contacts() -> pd.DataFrame:
    """
    Extrai contatos de todas as tags e retorna um DataFrame.

    Returns:
        DataFrame com colunas: data_hora, tag, email
    """
    all_data = []
    extraction_time = datetime.now()

    print("Iniciando extração de contatos de todas as tags...")
    print("=" * 60)

    for tag_name, url in TAG_URLS.items():
        emails = fetch_contacts_from_tag(url, tag_name)

        # Adiciona os dados ao array
        for email in emails:
            all_data.append({
                "data_hora": extraction_time,
                "tag": tag_name,
                "email": email
            })

        print()

    # Cria DataFrame
    df = pd.DataFrame(all_data)

    print("=" * 60)
    print(f"Extração concluída! Total de registros: {len(df)}")
    print(f"Total de e-mails únicos: {df['email'].nunique()}")

    return df


def create_bigquery_dataset_if_not_exists(client: bigquery.Client):
    """
    Cria o dataset no BigQuery se ele não existir.

    Args:
        client: Cliente do BigQuery
    """
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"

    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_ref} ja existe.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        dataset = client.create_dataset(dataset)
        print(f"Dataset {dataset_ref} criado com sucesso!")


def create_bigquery_table_if_not_exists(client: bigquery.Client):
    """
    Cria a tabela no BigQuery se ela não existir.

    Args:
        client: Cliente do BigQuery
    """
    schema = [
        bigquery.SchemaField("data_hora", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("tag", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
    ]

    table = bigquery.Table(FULL_TABLE_ID, schema=schema)

    try:
        client.get_table(FULL_TABLE_ID)
        print(f"Tabela {FULL_TABLE_ID} ja existe.")
    except Exception:
        table = client.create_table(table)
        print(f"Tabela {FULL_TABLE_ID} criada com sucesso!")


def upload_to_bigquery(df: pd.DataFrame):
    """
    Faz upload dos dados para o BigQuery.

    Args:
        df: DataFrame com os dados a serem enviados
    """
    print("\nIniciando upload para o BigQuery...")

    # Inicializa o cliente do BigQuery
    client = bigquery.Client(project=PROJECT_ID)

    # Cria o dataset se não existir
    create_bigquery_dataset_if_not_exists(client)

    # Cria a tabela se não existir
    create_bigquery_table_if_not_exists(client)

    # Configurações de upload
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema=[
            bigquery.SchemaField("data_hora", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("tag", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
        ]
    )

    # Faz o upload
    try:
        job = client.load_table_from_dataframe(
            df, FULL_TABLE_ID, job_config=job_config
        )
        job.result()  # Aguarda a conclusão

        print(f"Upload concluído com sucesso!")
        print(f"Total de linhas inseridas: {len(df)}")
        print(f"Tabela: {FULL_TABLE_ID}")

    except Exception as e:
        print(f"Erro ao fazer upload para o BigQuery: {e}")
        raise


def main():
    """
    Função principal que orquestra todo o processo.
    """
    print("=" * 60)
    print("EXTRAÇÃO DE E-MAILS DO ACTIVECAMPAIGN PARA BIGQUERY")
    print("=" * 60)
    print()

    try:
        # Valida que a API key está configurada
        if not API_KEY:
            raise ValueError(
                "Configure a variável de ambiente ACTIVECAMPAIGN_API_KEY "
                "antes de executar o script"
            )

        # Extrai contatos
        df = extract_all_contacts()

        if df.empty:
            print("Nenhum dado foi extraído. Verifique as configurações da API.")
            return

        # Exibe preview dos dados
        print("\nPreview dos dados:")
        print(df.head(10))
        print()

        # Upload para BigQuery
        upload_to_bigquery(df)

        print("\n" + "=" * 60)
        print("PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")
        raise


if __name__ == "__main__":
    main()
