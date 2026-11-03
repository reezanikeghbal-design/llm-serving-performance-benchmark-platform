import csv
import json
import os
from datetime import datetime, timezone
from app.core.config import settings

def save_report(report: dict) -> dict:
    os.makedirs(settings.reports_dir, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = f"{settings.reports_dir}/{stamp}_{report['experiment_id']}"
    json_path, csv_path = base + ".json", base + ".csv"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        fields = ["experiment_id", "timestamp", "model", "request_count",
                  "successful_requests", "failed_requests", "average_latency_ms",
                  "p95_latency_ms", "average_throughput_tokens_per_second", "success_rate"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for item in report["results"]:
            writer.writerow({"experiment_id": report["experiment_id"],
                             "timestamp": report["timestamp"], **{k: item.get(k) for k in fields[2:]}})
    return {"json": json_path, "csv": csv_path}
