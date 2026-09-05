# A2 — Audit of the Original Analysis

## A2.1 Code bug: the original tokenizer comparison omitted Kannada and Tamil

### Problem

The original `compare_tokenizers.py` compared only English and Hindi. Therefore, the original benchmark did not satisfy the multilingual evaluation requirement because it did not measure Kannada or Tamil.

This is a code/data coverage bug rather than a tokenizer bug.

### Original command

```powershell
python compare_tokenizers.py
Original result
Running GPT-2 benchmark...

tokenizer: gpt2

lang    fertility (tok/word)    tok/char
----------------------------------------
eng              1.27             0.226
hin              7.45             1.579

hin is 5.89x the fertility of eng

## A2.2 Conceptual problem: the denominator was not language-neutral

### Problem

The original metric used whitespace-separated words as the denominator:

```text
fertility = number of tokenizer tokens / number of whitespace-separated words


Original GPT-2 results
Language    Fertility (tokens/word)    Tokens/character
-------------------------------------------------------
English             1.27                    0.226
Hindi               7.45                    1.579
Kannada            25.10                    2.737
Tamil              26.07                    2.782

Second-denominator check

The analysis also used token-per-character as a second denominator:

tokens per character = number of tokenizer tokens / number of characters

The token-per-character metric is also not perfect, but it is less dependent on whitespace word segmentation.

For Hindi and English:

Hindi/English ratio using token-per-word
= 7.45 / 1.27
≈ 5.89x

Using token-per-character:

Hindi/English ratio using token-per-character
= 1.579 / 0.226
≈ 6.99x

The multiplier changes when the denominator changes. This shows that the reported ratio depends on the measurement definition.

Pooled denominator check

The pooled analysis produced the following values:

Original whitespace-based ratio ≈ 5.922x
Pooled whitespace-based ratio   ≈ 5.928x

The difference was:

5.928 - 5.922 = 0.006x

## A2.3 Suspicious-looking result that is actually correct

### Suspicious result

The GPT-2 fertility values for Kannada and Tamil were much higher than the English value:

```text
English     1.27 tokens/word
Hindi       7.45 tokens/word
Kannada    25.10 tokens/word
Tamil      26.07 tokens/word
XLM-RoBERTa result
tokenizer: hf:xlm-roberta-base

lang    fertility (tok/word)    tok/char
----------------------------------------
eng              1.28             0.228
hin              1.42             0.303
kan              2.18             0.239
tam              2.04             0.219
Hindi is 1.10x the fertility of English
Kannada is 1.70x the fertility of English
Tamil is approximately 1.59x the fertility of English
Kannada calculation

GPT-2 Kannada fertility:

25.10 tokens/word

XLM-RoBERTa Kannada fertility:

2.18 tokens/word

Absolute reduction:

25.10 - 2.18
= 22.92 tokens/word

Percentage reduction:

(22.92 / 25.10) × 100
≈ 91.3%

Therefore, XLM-RoBERTa reduced Kannada fertility by approximately 91.3% compared with GPT-2.

Tamil calculation

GPT-2 Tamil fertility:

26.07 tokens/word

XLM-RoBERTa Tamil fertility:

2.04 tokens/word

Absolute reduction:

26.07 - 2.04
= 24.03 tokens/word

Percentage reduction:

(24.03 / 26.07) × 100
≈ 92.2%

Therefore, XLM-RoBERTa reduced Tamil fertility by approximately 92.2% compared with GPT-2.

Hindi-to-English comparison

For GPT-2:

Hindi/English ratio
= 7.45 / 1.27
≈ 5.89x

For XLM-RoBERTa:

Hindi/English ratio
= 1.42 / 1.28
≈ 1.10x

The ratio decreased from approximately 5.89x to 1.10x.
A2.4 Suspicious-looking result that is actually correct

The Kannada and Tamil GPT-2 fertility values are much higher than the English and Hindi values:

English = 1.27 tok/word
Hindi   = 7.45 tok/word
Kannada = 25.10 tok/word
Tamil   = 26.07 tok/word

At first, the Kannada and Tamil values appear suspicious because they are approximately 20 times higher than English. However, the result is plausible for GPT-2 because its tokenizer was primarily developed for text using Latin-script vocabulary. Kannada and Tamil use different writing systems, so GPT-2 often splits their words into many smaller subword or byte-level tokens.

The corrected GPT-2 comparison shows:

Hindi fertility   = 7.45 / 1.27 = 5.89× English
Kannada fertility = 25.10 / 1.27 = 19.84× English
Tamil fertility   = 26.07 / 1.27 = 20.60× English

The result is therefore not automatically a code error. It reflects poor vocabulary coverage for these scripts in GPT-2.

The XLM-RoBERTa comparison provides supporting evidence:

English = 1.28 tok/word
Hindi   = 1.42 tok/word
Kannada = 2.18 tok/word
Tamil   = 2.04 tok/word

Compared with English:

Hindi   = 1.42 / 1.28 = 1.10×
Kannada = 2.18 / 1.28 = 1.70×
Tamil   = 2.04 / 1.28 = 1.59×