#!/usr/bin/env python3
import argparse
from pathlib import Path

import duckdb


def main():
    parser = argparse.ArgumentParser(description="Load synthetic CSV files into DuckDB raw schema.")
    parser.add_argument("--raw-dir", default="data/raw", help="Directory containing users.csv and orders.csv.")
    parser.add_argument("--db-path", default="data/warehouse.duckdb", help="DuckDB database path.")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    users_csv = raw_dir / "users.csv"
    orders_csv = raw_dir / "orders.csv"
    db_path = Path(args.db_path)

    if not users_csv.exists() or not orders_csv.exists():
        raise FileNotFoundError("Expected users.csv and orders.csv in raw directory before loading DuckDB.")

    db_path.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(db_path))
    try:
        con.execute("create schema if not exists raw")

        con.execute(
            """
            create or replace table raw.raw_users as
            select
                cast(user_id as integer) as user_id,
                cast(email as varchar) as email,
                cast(created_at as timestamp) as created_at,
                cast(country as varchar) as country
            from read_csv_auto(?, header=true)
            """,
            [str(users_csv)],
        )

        con.execute(
            """
            create or replace table raw.raw_orders as
            select
                cast(order_id as integer) as order_id,
                cast(user_id as integer) as user_id,
                cast(amount as decimal(18,2)) as amount,
                cast(status as varchar) as status,
                cast(created_at as timestamp) as created_at
            from read_csv_auto(?, header=true)
            """,
            [str(orders_csv)],
        )
    finally:
        con.close()


if __name__ == "__main__":
    main()
