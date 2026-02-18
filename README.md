# analytics-platform-dbt

## English

This repository implements a self-contained analytics pipeline with dbt and DuckDB. Each CI run generates deterministic synthetic data, loads raw tables into a local DuckDB file, and builds models in a layered dbt structure (`staging -> marts`).

The main objective is reproducibility without external infrastructure. The pipeline does not depend on cloud warehouses, external credentials, or user-specific local profiles. All steps run in GitHub Actions using a single entrypoint.

The run produces standard outputs for verification and troubleshooting: dbt artifacts (`target/`), logs, the DuckDB warehouse file, and a markdown report with test status and model list.

### Architecture Overview

```text
scripts/generate_data.py
        |
        v
    data/raw/*.csv
        |
        v
 scripts/load_duckdb.py
        |
        v
data/warehouse.duckdb (schema: raw)
        |
        v
      dbt run/test/docs
        |
        v
 dbt/target + artifacts/report.md + artifacts/logs
```

### How To Run (One Command)

```bash
scripts/ci.sh
```

Alternative one-command path with Docker:

```bash
docker compose up --build --abort-on-container-exit
```

### How To Run Tests

```bash
dbt test --project-dir dbt --profiles-dir dbt
```

### Example Commands And Output Snippets

```bash
scripts/ci.sh
```

```text
... 
Finished running 1 project hook, 5 models, 16 tests in 0:00:XX
Completed successfully
```

```bash
cat artifacts/report.md
```

```text
# CI Data Pipeline Report
- Test status: PASS
- Total tests executed: 16
```

### Repo Structure (Deliverables)

```text
.
|-- .github/workflows/ci.yml
|-- artifacts/
|-- data/
|   |-- raw/
|-- dbt/
|   |-- models/
|   |   |-- staging/
|   |   |-- marts/
|   |-- tests/
|   |-- dbt_project.yml
|   |-- profiles.yml
|-- scripts/
|   |-- ci.sh
|   |-- generate_data.py
|   |-- load_duckdb.py
|   |-- generate_report.py
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
```

### Limitations

- Local execution requires a dbt-compatible Python environment.
- Synthetic data is deterministic, so scenario variety is limited.
- The current scope is CI validation and analytics modeling, not production-scale ingestion.

### Next Steps

1. Add freshness and anomaly tests for marts.
2. Add an incremental model example with controlled backfill.
3. Publish dbt docs as a static artifact site.

## Português

Este repositório implementa um pipeline analítico completo com dbt e DuckDB. Em cada execução do CI, os dados sintéticos são gerados de forma determinística, carregados em tabelas brutas no DuckDB e transformados no projeto dbt em camadas (`staging -> marts`).

O objetivo principal é garantir reprodutibilidade sem infraestrutura externa. O fluxo não depende de banco em nuvem, credenciais ou perfil local do usuário. Tudo roda no GitHub Actions a partir de um único ponto de entrada.

A execução gera artefatos para validação e suporte: `dbt/target`, logs, arquivo do warehouse (`data/warehouse.duckdb`) e relatório em markdown com resultado dos testes e lista de modelos.

### Visão da Arquitetura

```text
scripts/generate_data.py
        |
        v
    data/raw/*.csv
        |
        v
 scripts/load_duckdb.py
        |
        v
data/warehouse.duckdb (schema: raw)
        |
        v
      dbt run/test/docs
        |
        v
 dbt/target + artifacts/report.md + artifacts/logs
```

### Como Executar (Um Comando)

```bash
scripts/ci.sh
```

Alternativa com Docker em um comando:

```bash
docker compose up --build --abort-on-container-exit
```

### Como Rodar os Testes

```bash
dbt test --project-dir dbt --profiles-dir dbt
```

### Exemplos de Comandos e Saídas

```bash
scripts/ci.sh
```

```text
... 
Finished running 1 project hook, 5 models, 16 tests in 0:00:XX
Completed successfully
```

```bash
cat artifacts/report.md
```

```text
# CI Data Pipeline Report
- Test status: PASS
- Total tests executed: 16
```

### Estrutura do Repositório (Entregáveis)

```text
.
|-- .github/workflows/ci.yml
|-- artifacts/
|-- data/
|   |-- raw/
|-- dbt/
|   |-- models/
|   |   |-- staging/
|   |   |-- marts/
|   |-- tests/
|   |-- dbt_project.yml
|   |-- profiles.yml
|-- scripts/
|   |-- ci.sh
|   |-- generate_data.py
|   |-- load_duckdb.py
|   |-- generate_report.py
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
```

### Limitações

- A execução local exige ambiente Python compatível com dbt.
- Os dados sintéticos são determinísticos e cobrem menos variações de cenário.
- O escopo atual é validação de CI e modelagem analítica, não ingestão de produção em larga escala.

### Próximos Passos

1. Adicionar testes de frescor e anomalia nas tabelas analíticas.
2. Incluir exemplo de modelo incremental com backfill controlado.
3. Publicar a documentação do dbt como site estático em artefato.