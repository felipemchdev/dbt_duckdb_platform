#!/usr/bin/env python3
import argparse
import json
import platform
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def read_json(path: Path):
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_dbt_version_text():
    try:
        return subprocess.check_output(["dbt", "--version"], text=True).strip()
    except Exception:
        return "dbt version unavailable"


def summarize_tests(run_results):
    results = run_results.get("results", [])
    test_results = [r for r in results if str(r.get("unique_id", "")).startswith("test.")]
    counts = Counter(r.get("status", "unknown") for r in test_results)
    return test_results, counts


def get_models(manifest):
    nodes = manifest.get("nodes", {})
    models = []
    for node in nodes.values():
        if node.get("resource_type") == "model" and node.get("package_name") == "analytics_platform":
            models.append(node.get("name", "unknown_model"))
    return sorted(set(models))


def main():
    parser = argparse.ArgumentParser(description="Generate markdown report for CI execution.")
    parser.add_argument("--output", default="artifacts/report.md")
    parser.add_argument("--manifest", default="dbt/target/manifest.json")
    parser.add_argument("--run-results", default="artifacts/run_results_test.json")
    parser.add_argument("--test-exit-code", type=int, default=1)
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = read_json(Path(args.manifest))
    run_results = read_json(Path(args.run_results))

    test_results, test_counts = summarize_tests(run_results)
    failed_count = test_counts.get("fail", 0) + test_counts.get("error", 0)
    test_status = "PASS" if args.test_exit_code == 0 and failed_count == 0 else "FAIL"

    models = get_models(manifest)
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    status_lines = []
    for status in ["pass", "warn", "fail", "error", "skipped", "unknown"]:
        if test_counts.get(status, 0) > 0:
            status_lines.append(f"- {status}: {test_counts[status]}")

    if not status_lines:
        status_lines.append("- no test results found")

    model_lines = [f"- {model}" for model in models] if models else ["- no models found in manifest"]

    report = "\n".join(
        [
            "# CI Data Pipeline Report",
            "",
            f"- Run timestamp (UTC): {timestamp}",
            f"- Test status: {test_status}",
            f"- Test exit code: {args.test_exit_code}",
            f"- Total tests executed: {len(test_results)}",
            "",
            "## Runtime Versions",
            "",
            f"- Python: {platform.python_version()}",
            "- dbt:",
            "```text",
            get_dbt_version_text(),
            "```",
            "",
            "## dbt Test Summary",
            "",
            *status_lines,
            "",
            "## Models in Manifest",
            "",
            *model_lines,
            "",
        ]
    )

    output_path.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
