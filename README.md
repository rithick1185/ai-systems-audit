# AI Systems Audit

This project audits tokenizer behavior, serving capacity, throughput measurements, and deployment recommendations for a multilingual AI system.

## Project Structure

```text
starter_kit/
├── NOTEBOOK.md
├── AI_USAGE.md
├── REPORT_v0.md
├── audit_experiment.py
├── capacity_experiment.py
├── compare_tokenizers.py
├── fertility.py
├── parallel_experiment.py
├── throughput_analysis.py
├── partA/
│   ├── a1_results.md
│   ├── a3_results.md
│   ├── a4_memo.md
│   └── corpus/
│       ├── corpus_notes.md
│       ├── eng_sample.txt
│       ├── hin_sample.txt
│       ├── kan_sample.txt
│       └── tam_sample.txt
├── partB/
│   └── answers.md
└── partC/
    └── memo.md

# AI Systems Audit

This project audits tokenizer efficiency, serving capacity, throughput measurements, and deployment recommendations for a multilingual AI system.

## Project Structure

- `partA/` — Multilingual tokenizer evaluation and recommendation memo
- `partB/` — KV-cache capacity calculations and throughput reconciliation
- `partC/` — Three-week deployment recommendation memo
- `NOTEBOOK.md` — Chronological record of hypotheses, experiments, findings, and corrections
- `REPORT_v0.md` — Original report and corrected findings
- `AI_USAGE.md` — Documentation of AI assistance and verification steps

## Main Findings

- GPT-2 tokenization is substantially less efficient for Hindi, Kannada, and Tamil than for English.
- XLM-RoBERTa provides much better multilingual tokenization efficiency.
- The estimated KV-cache capacity is approximately 46 theoretical concurrent 4096-token requests.
- Throughput does not increase linearly with batch size.
- For the long-context workload, batch 24 achieved 1607.40 tok/s, while batch 48 achieved 1298.50 tok/s.
- A prompt-only approach is recommended for the three-week launch because it has the lowest implementation risk and requires no additional model training.

## Limitations

- The KV-cache concurrency value is a theoretical estimate, not a measured production limit.
- Actual serving capacity may be lower because of memory fragmentation, activations, scheduling overhead, and runtime allocations.
- Tokenizer results depend on the evaluation corpus, preprocessing, tokenizer, and denominator used.
- The benchmark rows are only comparable when prompt length and generation length are the same.
- The prompt-only recommendation requires further evaluation using held-out prompts and native Hindi and Kannada review.
- The results should not be treated as production guarantees without additional validation.

## How to Review the Results

1. Read `NOTEBOOK.md` for the experiment history.
2. Read `REPORT_v0.md` for the original and corrected findings.
3. Read `partA/a1_results.md` and `partA/a3_results.md` for tokenizer results.
4. Read `partB/answers.md` for capacity and throughput calculations.
5. Read `partC/memo.md` for the deployment recommendation.
6. Read `AI_USAGE.md` for the AI assistance and verification record.