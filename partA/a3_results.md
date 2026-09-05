# A3. Corrected Multilingual Tokenizer Analysis

## GPT-2 results

| Language | Fertility (tok/word) | Tokens/character |
|---|---:|---:|
| English | 1.27 | 0.226 |
| Hindi | 7.45 | 1.579 |
| Kannada | 25.10 | 2.737 |
| Tamil | 26.07 | 2.782 |

## XLM-RoBERTa results

| Language | Fertility (tok/word) | Tokens/character |
|---|---:|---:|
| English | 1.28 | 0.228 |
| Hindi | 1.42 | 0.303 |
| Kannada | 2.18 | 0.239 |
| Tamil | 2.04 | 0.219 |

## Comparison using tokens per word

### GPT-2

### GPT-2

The ratios below are calculated from the displayed rounded values. The original script may produce slightly different ratios when using unrounded measurements.

Hindi / English

= 7.45 / 1.27

≈ 5.87×

Kannada / English

= 25.10 / 1.27

≈ 19.76×

Tamil / English

= 26.07 / 1.27

≈ 20.53×

XLM-RoBERTa tokens-per-word calculations
Hindi / English
= 1.42 / 1.28
≈ 1.11×

Kannada / English
= 2.18 / 1.28
≈ 1.70×

Tamil / English
= 2.04 / 1.28
≈ 1.59×

## Denominator choice and recommendation

Tokens per word is the primary denominator for routing and cost estimation because serving cost and context usage depend on the number of tokens processed. Tokens per character is reported as a secondary measure because word boundaries differ across languages and can affect tokens-per-word comparisons.

The corrected results show that GPT-2 has a very large tokenization overhead for Hindi, Kannada, and Tamil, especially Kannada and Tamil. XLM-RoBERTa greatly reduces this multilingual gap. Therefore, XLM-RoBERTa or another multilingual tokenizer is more suitable for multilingual routing and cost planning.

These results are based on a small evaluation corpus and should be confirmed using a larger production-like corpus before final deployment.