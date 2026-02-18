# analytics-platform-dbt

## English

This project runs a full analytics pipeline with dbt + DuckDB in GitHub Actions.
It generates synthetic data, loads raw tables, builds staging and mart models, runs tests, and generates docs.

Synthetic data is deterministic: with the same seed, the same rows are generated.
Freshness means how recent the data is. A freshness check validates if the latest timestamp is inside an expected time window.

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

1. Add freshness and anomaly tests for marts.
2. Add an incremental model with controlled backfill.
3. Publish dbt docs as static site artifact.

## Português

Este projeto executa um pipeline de dados completo com dbt + DuckDB no GitHub Actions.
Ele gera dados sintéticos, carrega tabelas brutas, cria modelos de staging e marts, roda testes e gera documentação.

Dados sintéticos determinísticos: com a mesma semente, os dados gerados são sempre os mesmos.
Frescor dos dados: mede se a tabela está atualizada. O teste verifica se a data mais recente está dentro de um limite esperado.

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

### Como rodar só os testes

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

### Estrutura do repositório

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

### Limitações

- Execução local exige ambiente Python/dbt compatível.
- Os dados são sintéticos e simplificados.

### Próximos passos

1. Adicionar teste de frescor e anomalia nos marts.
2. Incluir modelo incremental com backfill controlado.
3. Publicar docs do dbt como site estático em artefato.