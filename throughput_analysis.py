import csv
from collections import defaultdict

CSV_PATH = "bench/bench_log.csv"

# Read the benchmark results
with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# Group results by batch size
by_batch = defaultdict(list)

for row in rows:
    batch = int(row["batch_size"])
    by_batch[batch].append(row)

print("Throughput analysis")
print("-" * 70)

print(
    f"{'Batch':>6} | {'Best tok/s':>12} | "
    f"{'Prompt':>8} | {'Gen':>6} | {'p50 TTFT':>10}"
)
print("-" * 70)

# Find the highest-throughput run for each batch size
best_results = {}

for batch in sorted(by_batch):
    best = max(
        by_batch[batch],
        key=lambda row: float(row["reported_tok_s"])
    )

    best_results[batch] = best

    print(
        f"{batch:>6} | "
        f"{float(best['reported_tok_s']):>12.2f} | "
        f"{best['prompt_len']:>8} | "
        f"{best['gen_len']:>6} | "
        f"{float(best['ttft_ms_p50']):>10.2f}"
    )

print()
print("Comparison with the batch-48 estimate")
print("-" * 70)

for batch, row in best_results.items():
    measured = float(row["reported_tok_s"])
    estimated = 1600 * batch / 24
    difference = measured - estimated

    print(
        f"Batch {batch}: measured = {measured:.2f} tok/s, "
        f"estimate = {estimated:.2f} tok/s, "
        f"difference = {difference:+.2f} tok/s"
    )