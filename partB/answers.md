# Part B — Capacity Reconciliation

## B1. KV-cache calculation

### Given model configuration

- Number of layers: 28
- Number of KV heads: 8
- Head dimension: 128
- Data type: FP16
- Bytes per FP16 value: 2
- Maximum sequence length: 4096 tokens
- GPU memory: 24 GB
- Usable memory fraction: 92%
- Runtime overhead: 1.6 GB

### KV-cache bytes per token

The KV-cache stores both keys and values.

```text
KV-cache bytes/token
= number of layers
  × number of KV heads
  × head dimension
  × 2 for key and value
  × bytes per value

= 28 × 8 × 128 × 2 × 2

= 114,688 bytes/token

Therefore:

```text
KV-cache bytes/token = 114,688 bytes
KV-cache KB/token ≈ 112 KB
### Available KV-cache memory

```text
Usable GPU memory
= 24 GB × 0.92
= 22.08 GB
Available KV memory
= 22.08 GB − 1.6 GB
= 20.48 GB
Memory/request
= 114,688 × 4096 bytes
≈ 0.438 GB
Maximum concurrent requests
= available KV memory / memory per request

= 20.48 / 0.438

≈ 46 requests
46 concurrent 4096-token requests
This is a theoretical estimate, not a measured production concurrency value. Actual concurrency may be lower because of fragmentation, framework-specific memory usage, temporary activations, and other runtime allocations.

## B2. Throughput anomaly

The long-context workload uses:

- Prompt length: 3584 tokens
- Generation length: 512 tokens

The relevant measured rows are:

| Batch size | Throughput |
|---:|---:|
| 4 | 565.40 tok/s |
| 8 | 902.60 tok/s |
| 16 | 1311.40 tok/s |
| 24 | 1607.40 tok/s |
| 48 | 1298.50 tok/s |

These rows are comparable because they use the same long-context workload: a 3584-token prompt and 512 generated tokens.

The anomaly is that throughput increases up to batch 24 but decreases at batch 48.

Batch 24 throughput:
1607.40 tok/s

Batch 48 throughput:

1298.50 tok/s

The throughput decrease from batch 24 to batch 48 is:

1607.40 − 1298.50 = 308.90 tok/s

Relative decrease compared with batch 24:

308.90 / 1607.40 × 100 ≈ 19.2%

Therefore, increasing the batch size from 24 to 48 reduced measured throughput by approximately 19.2% for this long-context workload.

## B3. Misreading in the original report

The original report incorrectly treated the `reported_tok_s` column as generated-token goodput. However, the logged value includes both prompt tokens and generated tokens.

For the batch-24 long-context row:

Batch size = 24
Prompt length = 3584 tokens
Generation length = 512 tokens
Wall-clock time = 61.16 seconds
Reported throughput = 1607.40 tok/s

### Total sequence-token throughput

```text
Total sequence tokens
= batch size × (prompt length + generation length)

= 24 × (3584 + 512)

= 24 × 4096

= 98,304 tokens

Total sequence-token throughput
= total sequence tokens / wall-clock time

= 98,304 / 61.16

≈ 1607.33 tok/s
Generated tokens
= batch size × generation length

= 24 × 512

= 12,288 tokens
Generated-token goodput
= total generated tokens / wall-clock time

= 12,288 / 61.16

≈ 200.92 generated tok/s
Generated-token fraction
= generation length / total sequence length

= 512 / 4096

= 0.125
Generated-token goodput
= reported total-sequence throughput × generated-token fraction

= 1607.40 × 0.125

≈ 200.93 generated tok/s
Actual generated-token goodput ≈ 200.92 generated tok/s
Therefore, the original report should not describe 1607.40 tok/s as generated-token goodput. It is total sequence-token throughput, while the more useful generated-token goodput for this row is approximately 200.92 generated tok/s.

## B4. Metric to confirm the mechanism

The most useful additional metric is peak GPU memory usage during the long-context batch sweep.

If memory pressure is responsible for the batch-48 throughput anomaly, peak GPU memory usage at batch 48 should be higher than at batch 24 and should approach the available GPU memory limit.

Additional supporting metrics include:

- KV-cache allocation
- GPU memory utilization
- GPU compute utilization
- Request queue time
- Scheduler delay
- Out-of-memory or memory-allocation warnings

The expected observation is higher memory usage and increased scheduling or allocation overhead at batch 48 compared with batch 24.