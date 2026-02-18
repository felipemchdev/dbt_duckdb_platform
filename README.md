# analytics-platform-dbt

## English

This project runs a complete analytics pipeline with dbt + DuckDB in GitHub Actions.
It generates synthetic data, loads raw tables, builds staging and mart models, runs tests, and generates documentation.

The synthetic data is repeatable: with the same seed, each run creates the same rows.
Data update checks validate whether the latest timestamp is within an expected window.

### Architecture

```text
generate_data.py -> data/raw/*.csv -> load_duckdb.py -> data/warehouse.duckdb (raw)
                                                       -> dbt run/test/docs
                                                       -> dbt/target + artifacts/report.md
```

### Run (one command)

```bash
scripts/ci.sh
```

### Run tests only

```bash
dbt test --project-dir dbt --profiles-dir dbt
```

### Example

```bash
scripts/ci.sh
```

```text
Finished running models and tests
Test status: PASS
```

### Repo structure

```text
.github/workflows/ci.yml
artifacts/
data/
dbt/
scripts/
Dockerfile
docker-compose.yml
requirements.txt
```

### Limitations

- Local run needs a Python/dbt compatible environment.
- Data is synthetic and simplified.

### Next steps

1. Add data update and anomaly tests for marts.
2. Add an incremental model with controlled backfill.
3. Publish dbt docs as a static site artifact.

## Portugues

Este projeto executa um pipeline de dados completo com dbt + DuckDB no GitHub Actions.
Ele gera dados sinteticos, carrega tabelas brutas, cria modelos de staging e marts, roda testes e gera documentacao.

Os dados sinteticos sao repetiveis: com a mesma semente, toda execucao gera os mesmos registros.
O teste de atualizacao verifica se a data mais recente da tabela esta dentro do limite esperado.

### Arquitetura

```text
generate_data.py -> data/raw/*.csv -> load_duckdb.py -> data/warehouse.duckdb (raw)
                                                       -> dbt run/test/docs
                                                       -> dbt/target + artifacts/report.md
```

### Como rodar (um comando)

```bash
scripts/ci.sh
```

### Como rodar so os testes

```bash
dbt test --project-dir dbt --profiles-dir dbt
```

### Exemplo

```bash
scripts/ci.sh
```

```text
Finished running models and tests
Test status: PASS
```

### Estrutura do repositorio

```text
.github/workflows/ci.yml
artifacts/
data/
dbt/
scripts/
Dockerfile
docker-compose.yml
requirements.txt
```

### Limitacoes

- Execucao local exige ambiente Python/dbt compativel.
- Os dados sao sinteticos e simplificados.

### Proximos passos

1. Adicionar teste de atualizacao e anomalia nos marts.
2. Incluir modelo incremental com backfill controlado.
3. Publicar docs do dbt como site estatico em artefato.