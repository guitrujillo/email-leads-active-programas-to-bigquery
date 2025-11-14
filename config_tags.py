"""
Arquivo de Configuração das Tags - ActiveCampaign

IMPORTANTE: Atualize os TAG IDs mensalmente conforme necessário.

Para adicionar uma nova tag:
1. Adicione uma nova linha no formato:
   "nome_da_tag": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=XXXXX",

Para alterar um TAG ID:
1. Localize a tag desejada
2. Altere apenas o número após "tagid="

Exemplo:
  ANTES: "despertar": "...?tagid=1148195",
  DEPOIS: "despertar": "...?tagid=9999999",
"""

# =============================================================================
# CONFIGURAÇÃO DAS TAGS
# Atualize os TAG IDs aqui conforme necessário
# =============================================================================

TAG_URLS = {
    "despertar": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=1148195",
    "em_detalhes": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=1148196",
    "mercado": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=1148200",
    "n1": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=1148201",
    "n2": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=1148202",
    "chico_pinheiro": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=1148194",
    "espiritualidade": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=1148197",
    "urgente": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=1148199",
    "precisamos_conversar": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=1148203",
    "role": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=1148204",
}


# =============================================================================
# EXEMPLOS DE COMO ADICIONAR NOVAS TAGS
# =============================================================================
#
# Para adicionar uma nova tag, copie a linha abaixo e ajuste:
#
#     "nome_da_nova_tag": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=NOVO_ID",
#
# Exemplo real:
#     "black_friday": "https://institutoliberta.api-us1.com/api/3/contacts?tagid=1234567",
#
# Lembre-se de adicionar uma vírgula no final da linha anterior!
#
# =============================================================================


# =============================================================================
# CONFIGURAÇÕES DO BIGQUERY (NÃO ALTERAR)
# =============================================================================

PROJECT_ID = "projetos-icl"
DATASET_ID = "active_leads"
TABLE_ID = "emails_inscritos"
FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"


# =============================================================================
# API KEY DO ACTIVECAMPAIGN (NÃO ALTERAR - configurada via variável de ambiente)
# =============================================================================

# A API Key é configurada automaticamente via executar.bat
# Ou via variável de ambiente: ACTIVECAMPAIGN_API_KEY
