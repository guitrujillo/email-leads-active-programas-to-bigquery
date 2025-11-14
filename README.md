# ActiveCampaign to BigQuery - Email Leads Pipeline

Pipeline automatizado para extrair leads de email do ActiveCampaign (por tags de campanhas) e carregar no Google BigQuery para análise e acompanhamento de lançamentos de programas.

## Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Manutenção](#manutenção)
- [Troubleshooting](#troubleshooting)

---

## Visão Geral

Este projeto extrai contatos de tags específicas do ActiveCampaign e armazena no Google BigQuery, permitindo:
- Acompanhamento de leads por campanha/tag
- Análise histórica de crescimento de listas
- Integração com ferramentas de BI e analytics
- Backup automatizado de dados de marketing

### Componentes Principais

1. **activecampaign_to_bigquery.py** - Script principal que extrai leads do ActiveCampaign
2. **config_tags.py** - Configuração centralizada de tags e credenciais
3. **load_assinaturas_to_bigquery.py** - Script auxiliar para carregar dados de assinaturas do Excel
4. **verificar_dados.py** - Ferramenta para verificar dados no BigQuery
5. **executar.bat** - Script batch para execução no Windows

---

## Funcionalidades

- Extração automática de contatos por tags do ActiveCampaign
- Paginação automática para grandes volumes de dados
- Detecção e remoção de duplicatas
- Upload incremental para BigQuery (modo APPEND)
- Criação automática de dataset e tabelas se não existirem
- Timestamp de extração para rastreabilidade
- Rate limiting para respeitar limites da API
- Logging detalhado de todo o processo
- Configuração centralizada e fácil de manter

### Tags Suportadas

O sistema é configurado para extrair leads das seguintes tags de campanhas:
- despertar
- em_detalhes
- mercado
- n1, n2
- chico_pinheiro
- espiritualidade
- urgente
- precisamos_conversar
- role

---

## Pré-requisitos

### Software

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conta ActiveCampaign com API habilitada
- Google Cloud Platform com BigQuery habilitado

### Acessos Necessários

1. **ActiveCampaign**
   - API Key com permissões de leitura de contatos
   - Acesso às tags configuradas

2. **Google BigQuery**
   - Service Account com permissões de escrita
   - Dataset criado ou permissões para criar

---

## Instalação

### 1. Clone ou baixe o projeto

```bash
cd "C:\Users\SeuUsuario\Documents\EMAIL LEADS LANCAMENTOS"
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Configuração

### 1. Configurar API Key do ActiveCampaign

Você tem duas opções:

#### Opção A: Variável de Ambiente (Recomendado)

```bash
# Windows (PowerShell)
$env:ACTIVECAMPAIGN_API_KEY = "sua_api_key_aqui"

# Windows (CMD)
set ACTIVECAMPAIGN_API_KEY=sua_api_key_aqui

# Linux/Mac
export ACTIVECAMPAIGN_API_KEY="sua_api_key_aqui"
```

#### Opção B: Usando o script executar.bat (Windows)

Edite o arquivo `executar.bat` e adicione sua API key:

```batch
set ACTIVECAMPAIGN_API_KEY=sua_api_key_aqui
```

### 2. Configurar Tags

Edite o arquivo [config_tags.py](config_tags.py) para adicionar, remover ou modificar tags:

```python
TAG_URLS = {
    "nome_da_tag": "https://SUA_CONTA.api-us1.com/api/3/contacts?tagid=ID_DA_TAG",
    # Adicione mais tags conforme necessário
}
```

**Para encontrar o Tag ID:**
1. Acesse sua conta ActiveCampaign
2. Vá em Contacts > Tags
3. Clique na tag desejada
4. O ID aparece na URL: `.../tags/view/123456`

### 3. Configurar Google Cloud / BigQuery

#### a) Criar Service Account

1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Selecione seu projeto
3. Vá em **IAM & Admin** > **Service Accounts**
4. Clique em **Create Service Account**
5. Dê um nome (ex: "bigquery-activecampaign")
6. Adicione a role: **BigQuery Data Editor**
7. Clique em **Create Key** e escolha JSON
8. Salve o arquivo JSON baixado

#### b) Configurar credenciais

Defina a variável de ambiente apontando para o arquivo JSON:

```bash
# Windows (PowerShell)
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\caminho\para\service-account.json"

# Windows (CMD)
set GOOGLE_APPLICATION_CREDENTIALS=C:\caminho\para\service-account.json

# Linux/Mac
export GOOGLE_APPLICATION_CREDENTIALS="/caminho/para/service-account.json"
```

#### c) Atualizar configurações do BigQuery

Edite [config_tags.py](config_tags.py) se necessário:

```python
PROJECT_ID = "seu-project-id"
DATASET_ID = "active_leads"
TABLE_ID = "emails_inscritos"
```

---

## Uso

### Execução Básica

#### Windows (usando executar.bat)

```batch
executar.bat
```

#### Qualquer plataforma (Python direto)

```bash
python activecampaign_to_bigquery.py
```

### O que o script faz:

1. Valida que a API key está configurada
2. Para cada tag configurada:
   - Busca todos os contatos (com paginação automática)
   - Extrai os emails
   - Remove duplicatas
3. Cria um DataFrame com os dados
4. Conecta ao BigQuery
5. Cria dataset e tabela se não existirem
6. Faz upload dos dados (modo APPEND)
7. Exibe relatório de execução

### Verificar Dados no BigQuery

Use o script auxiliar para verificar os dados inseridos:

```bash
python verificar_dados.py
```

---

## Estrutura do Projeto

```
email-leads-active-programas-to-bigquery/
│
├── activecampaign_to_bigquery.py   # Script principal
├── config_tags.py                   # Configurações de tags e BigQuery
├── load_assinaturas_to_bigquery.py  # Script auxiliar (Excel para BigQuery)
├── verificar_dados.py               # Verificação de dados
├── executar.bat                     # Script de execução Windows
├── requirements.txt                 # Dependências Python
├── .gitignore                       # Arquivos ignorados pelo Git
└── README.md                        # Este arquivo
```

### Schema da Tabela BigQuery

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `data_hora` | TIMESTAMP | Data e hora da extração |
| `tag` | STRING | Nome da tag/campanha |
| `email` | STRING | Email do contato |

---

## Manutenção

### Adicionar Nova Tag

1. Abra [config_tags.py](config_tags.py)
2. Adicione uma nova entrada no dicionário `TAG_URLS`:

```python
TAG_URLS = {
    # Tags existentes...
    "nova_campanha": "https://SUA_CONTA.api-us1.com/api/3/contacts?tagid=NOVO_ID",
}
```

3. Execute o script normalmente

### Atualizar Tag ID (quando uma tag é recriada)

1. Abra [config_tags.py](config_tags.py)
2. Localize a tag desejada
3. Atualize apenas o número após `tagid=`:

```python
# ANTES
"despertar": "...?tagid=1148195",

# DEPOIS
"despertar": "...?tagid=9999999",
```

### Limpar Dados Duplicados no BigQuery

Se necessário remover duplicatas, execute no BigQuery Console:

```sql
-- Visualizar duplicatas
SELECT
  email,
  tag,
  COUNT(*) as count
FROM `seu-project.active_leads.emails_inscritos`
GROUP BY email, tag
HAVING COUNT(*) > 1;

-- Remover duplicatas (mantém apenas o registro mais recente)
DELETE FROM `seu-project.active_leads.emails_inscritos`
WHERE STRUCT(email, tag, data_hora) NOT IN (
  SELECT AS STRUCT email, tag, MAX(data_hora) as data_hora
  FROM `seu-project.active_leads.emails_inscritos`
  GROUP BY email, tag
);
```

---

## Troubleshooting

### Erro: "ACTIVECAMPAIGN_API_KEY não está configurada"

**Solução:**
- Certifique-se de configurar a variável de ambiente antes de executar
- No Windows, use o `executar.bat` que já configura automaticamente

### Erro: "403 Forbidden" ou "Unauthorized"

**Causa:** API Key inválida ou sem permissões.

**Solução:**
1. Verifique se a API key está correta no ActiveCampaign
2. Confirme que a API key tem permissões de leitura de contatos
3. Teste a API key usando curl ou Postman

### Erro: "Could not find Application Default Credentials"

**Causa:** Credenciais do Google Cloud não configuradas.

**Solução:**
1. Baixe o arquivo JSON da Service Account
2. Configure a variável `GOOGLE_APPLICATION_CREDENTIALS`
3. Ou use `gcloud auth application-default login`

### Erro: "Dataset not found"

**Solução:**
O script cria automaticamente o dataset. Se o erro persistir:
1. Verifique se a Service Account tem permissões
2. Ou crie manualmente no BigQuery Console

### Dados não aparecem no BigQuery

**Verificações:**
1. Confira se o script executou sem erros
2. Use `verificar_dados.py` para checar os dados
3. Verifique no BigQuery Console: `projeto.dataset.tabela`
4. Confirme que as tags no ActiveCampaign têm contatos

### Rate Limiting / Too Many Requests

**Solução:**
O script já implementa `time.sleep(0.5)` entre requisições. Se persistir:
- Aumente o sleep em [activecampaign_to_bigquery.py](activecampaign_to_bigquery.py):

```python
time.sleep(1.0)  # Aumentar delay entre requisições
```

---

## Consultas SQL Úteis

### Ver total de leads por tag

```sql
SELECT
  tag,
  COUNT(DISTINCT email) as total_emails,
  MAX(data_hora) as ultima_atualizacao
FROM `seu-project.active_leads.emails_inscritos`
GROUP BY tag
ORDER BY total_emails DESC;
```

### Ver crescimento de leads por data

```sql
SELECT
  DATE(data_hora) as data,
  tag,
  COUNT(DISTINCT email) as novos_emails
FROM `seu-project.active_leads.emails_inscritos`
GROUP BY data, tag
ORDER BY data DESC, tag;
```

### Encontrar emails em múltiplas tags

```sql
SELECT
  email,
  STRING_AGG(tag, ', ') as tags,
  COUNT(DISTINCT tag) as num_tags
FROM `seu-project.active_leads.emails_inscritos`
GROUP BY email
HAVING COUNT(DISTINCT tag) > 1
ORDER BY num_tags DESC;
```

---

## Segurança

**IMPORTANTE:**
- Nunca commit suas API keys ou credenciais no Git
- O `.gitignore` já está configurado para ignorar arquivos sensíveis
- Use variáveis de ambiente para credenciais
- Revise regularmente as permissões das Service Accounts

---

## Autor

Desenvolvido por Guilherme Trujillo

---

## Suporte

Para questões relacionadas ao projeto:
- Consulte a documentação oficial:
  - [ActiveCampaign API](https://developers.activecampaign.com/)
  - [BigQuery Documentation](https://cloud.google.com/bigquery/docs)

---

**Última atualização: 2025**
