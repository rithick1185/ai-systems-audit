# Tokenizer & Serving Findings (v0) — for the leadership deck

*Status: draft, numbers final. Please don't edit the conclusions,
the deck is already made.*

## 1. Tokenizer fertility

Ran `fertility.py` on our sample corpora with the `gpt2` tokenizer:

| lang | fertility (tok/word) | tok/char |
|---|---|---|
| eng | 1.27 | 0.226 |
| hin | 7.45 | 1.579 |

**Findings:**


1. GPT-2 tokenizes the Hindi sample much less efficiently than English: **7.45 vs 1.27 tokens/word**, a **5.89×** difference.
2. The audit experiment confirms the original result: the pooled Hindi/English ratio is **5.928×**, compared with **5.922×** using the original per-line averaging method.
3. XLM-RoBERTa substantially reduces the difference: **1.42 vs 1.28 tokens/word**, or **1.10×** Hindi/English fertility.

**Recommendation:** For multilingual serving, especially Hindi traffic, evaluate a multilingual tokenizer/model rather than assuming an English-oriented tokenizer is efficient for all languages.

## 2. Serving throughput (see bench/)

From `bench_log.csv`, throughput does not scale linearly with batch
size.

For the long-prompt workload (3584 prompt tokens, 512 generated
tokens), batch 24 achieved **1607 tok/s**, while batch 48 achieved
**1299 tok/s**.

The highest observed throughput was **2267 tok/s** at batch 64,
but this used a shorter 512-token prompt and 256 generated tokens,
so it is not directly comparable to the long-prompt workload.

**Finding:** The original assumption that batch 48 would provide
~3200 tok/s is not validated. Larger batch sizes do not
necessarily produce higher throughput.

**Recommendation:** Use workload-matched benchmark results for
capacity planning rather than assuming linear scaling with batch
size. Investigate the long-prompt batch-48 result before selecting
a production batch size.

## 3. KV-cache capacity analysis

For the assumed 28-layer model with 8 KV heads, 128-dimensional heads, FP16 cache values, and a maximum sequence length of 4096 tokens, the estimated KV-cache requirement is approximately 112 KB per token.

Using an available KV-cache memory budget of 20.48 GB and an estimated memory requirement of 0.438 GB per request, the theoretical maximum concurrency is approximately 46 requests.

This is a planning estimate rather than a measured production limit. Actual concurrency will also depend on runtime overhead, allocator fragmentation, request scheduling, and other GPU memory usage.

## 4. Next steps

- Validate throughput using the same prompt and generation lengths across all batch sizes.
- Measure actual GPU memory usage and production concurrency.
- Benchmark additional multilingual tokenizers and representative application prompts.
- Test quality and latency together before selecting the production tokenizer.
- Add monitoring for tokenization cost, throughput, latency, and GPU memory usage.


The measured results show that throughput does not scale linearly with batch size. Because the prompt and generation lengths differ across some batch sizes, workload-matched benchmarking is required before drawing conclusions about the effect of prompt length.