#!/usr/bin/env python3
import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


def generate_users(count: int, rng: random.Random):
    countries = ["US", "BR", "CA", "DE", "GB", "FR", "JP", "AU"]
    base_ts = datetime(2023, 1, 1, 8, 0, 0)

    users = []
    for user_id in range(1, count + 1):
        created_at = base_ts + timedelta(days=rng.randint(0, 730), hours=rng.randint(0, 23))
        users.append(
            {
                "user_id": user_id,
                "email": f"user{user_id}@example.com",
                "created_at": created_at.isoformat(sep=" "),
                "country": rng.choice(countries),
            }
        )
    return users


def generate_orders(count: int, users, rng: random.Random):
    statuses = ["created", "paid", "shipped", "canceled"]
    user_lookup = {user["user_id"]: datetime.fromisoformat(user["created_at"]) for user in users}

    orders = []
    for idx in range(count):
        order_id = idx + 1
        user_id = rng.randint(1, len(users))
        user_created_at = user_lookup[user_id]
        order_created_at = user_created_at + timedelta(days=rng.randint(0, 180), hours=rng.randint(0, 23))

        amount = round(rng.uniform(10.0, 500.0), 2)
        orders.append(
            {
                "order_id": order_id,
                "user_id": user_id,
                "amount": amount,
                "status": rng.choices(statuses, weights=[20, 45, 25, 10], k=1)[0],
                "created_at": order_created_at.isoformat(sep=" "),
            }
        )
    return orders


def write_csv(path: Path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate deterministic synthetic users and orders CSV files.")
    parser.add_argument("--output-dir", default="data/raw", help="Directory where CSV files will be generated.")
    parser.add_argument("--users", type=int, default=200, help="Number of synthetic users.")
    parser.add_argument("--orders", type=int, default=1000, help="Number of synthetic orders.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for deterministic generation.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    rng = random.Random(args.seed)

    users = generate_users(args.users, rng)
    orders = generate_orders(args.orders, users, rng)

    write_csv(output_dir / "users.csv", users, ["user_id", "email", "created_at", "country"])
    write_csv(output_dir / "orders.csv", orders, ["order_id", "user_id", "amount", "status", "created_at"])


if __name__ == "__main__":
    main()
