#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

mkdir -p data/raw artifacts artifacts/logs

rm -f data/warehouse.duckdb
rm -rf dbt/target

python scripts/generate_data.py --output-dir data/raw --seed 42
python scripts/load_duckdb.py --raw-dir data/raw --db-path data/warehouse.duckdb

export DBT_PROFILES_DIR="$REPO_ROOT/dbt"
export DBT_DUCKDB_PATH="$REPO_ROOT/data/warehouse.duckdb"

dbt deps --project-dir dbt --profiles-dir dbt --log-path artifacts/logs
dbt seed --project-dir dbt --profiles-dir dbt --log-path artifacts/logs
dbt run --project-dir dbt --profiles-dir dbt --log-path artifacts/logs

set +e
dbt test --project-dir dbt --profiles-dir dbt --log-path artifacts/logs
test_exit_code=$?
set -e

if [ -f dbt/target/run_results.json ]; then
  cp dbt/target/run_results.json artifacts/run_results_test.json
fi

dbt docs generate --project-dir dbt --profiles-dir dbt --log-path artifacts/logs

python scripts/generate_report.py \
  --output artifacts/report.md \
  --manifest dbt/target/manifest.json \
  --run-results artifacts/run_results_test.json \
  --test-exit-code "$test_exit_code"

exit "$test_exit_code"
