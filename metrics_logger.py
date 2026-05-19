import csv
import os

FILE = "encryption_metrics.csv"

HEADERS = [
    "node",
    "algorithm",
    "operation",
    "data_type",   # NEW COLUMN
    "message_size",
    "time_ms",
    "energy_joule"
]


def log_metric(metric):
    file_exists = os.path.isfile(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(metric)
