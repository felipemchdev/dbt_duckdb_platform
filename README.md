# analytics-platform-dbt

Pipeline de dados com dbt + DuckDB totalmente reprodutível no GitHub Actions.

## CI entrypoint único

```bash
scripts/ci.sh
```

Esse script executa, em ordem:
1. Geração de dados sintéticos (`data/raw/*.csv`)
2. Carga do DuckDB (`data/warehouse.duckdb`)
3. `dbt deps`
4. `dbt seed`
5. `dbt run`
6. `dbt test`
7. `dbt docs generate`
8. Geração de `artifacts/report.md`

O exit code final do script reflete o resultado do `dbt test`.

## Rodar local com Docker

```bash
docker build -t analytics-platform-dbt .
docker run --rm -v "$(pwd):/app" analytics-platform-dbt
```

Ou:

```bash
docker compose up --build --abort-on-container-exit
```

## Onde ver os resultados

- Relatório final: `artifacts/report.md`
- Docs e artefatos dbt: `dbt/target/`
- Logs do dbt: `artifacts/logs/`
- Banco local do pipeline: `data/warehouse.duckdb`

## GitHub Actions

Workflow: `.github/workflows/ci.yml`

Triggers:
- `push` nas branches `dev`, `qa` e `master`
- `pull_request` para `dev`, `qa` e `master`
