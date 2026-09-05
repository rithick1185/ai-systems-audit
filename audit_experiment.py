import tiktoken


# Load the tokenizer
enc = tiktoken.get_encoding("gpt2")


def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def analyze(path):
    lines = read_lines(path)

    total_tokens = 0
    total_words = 0
    total_chars = 0

    for line in lines:
        tokens = enc.encode(line.lower())
        words = line.lower().split()
        chars = len(line.lower())

        total_tokens += len(tokens)
        total_words += len(words)
        total_chars += chars

    # Original method: average of per-line ratios
    fertility_per_line = []
    tpc_per_line = []

    for line in lines:
        text = line.lower()
        tokens = enc.encode(text)
        words = line.lower().split()
        chars = len(text)

        fertility_per_line.append(len(tokens) / len(words))
        tpc_per_line.append(len(tokens) / chars)

    original_fertility = sum(fertility_per_line) / len(fertility_per_line)
    original_tpc = sum(tpc_per_line) / len(tpc_per_line)

    # Alternative method: pooled totals
    pooled_fertility = total_tokens / total_words
    pooled_tpc = total_tokens / total_chars

    return (
        len(lines),
        total_tokens,
        total_words,
        total_chars,
        original_fertility,
        original_tpc,
        pooled_fertility,
        pooled_tpc,
    )


eng = analyze("corpus_sample/eng_sample.txt")
hin = analyze("corpus_sample/hin_sample.txt")

print("Language | Lines | Tokens | Words | Chars | Original tok/word | Pooled tok/word")
print("-" * 85)

for lang, result in [("eng", eng), ("hin", hin)]:
    print(
        f"{lang:8} | {result[0]:5} | {result[1]:6} | "
        f"{result[2]:5} | {result[3]:5} | "
        f"{result[4]:17.3f} | {result[6]:16.3f}"
    )

print()
print("Original Hindi/English ratio:",
      round(hin[4] / eng[4], 3))

print("Pooled Hindi/English ratio:",
      round(hin[6] / eng[6], 3))